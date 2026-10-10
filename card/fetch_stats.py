#!/usr/bin/env python3
"""Fetches real GitHub numbers for the profile card and writes stats.json.

Env:
  GH_USER   GitHub username (defaults to GITHUB_REPOSITORY_OWNER inside Actions)
  GH_TOKEN  token (falls back to GITHUB_TOKEN). A classic PAT with `repo` + `read:user`
            also counts PRIVATE repos/contributions; the built-in token sees public data only.
  SKIP_LOC  set to 1 to skip the (slow) lines-of-code calculation
No third-party packages needed.
"""
import json, os, sys, time, urllib.error, urllib.request

USER = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
API = "https://api.github.com"
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

QUERY = """
query($login:String!, $after:String){
  user(login:$login){
    followers{ totalCount }
    allRepos: repositories(ownerAffiliations:OWNER){ totalCount }
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount contributionLevel } }
      }
    }
    repositories(first:100, ownerAffiliations:OWNER, after:$after, orderBy:{field:PUSHED_AT, direction:DESC}){
      nodes{ nameWithOwner stargazerCount isFork }
      pageInfo{ hasNextPage endCursor }
    }
  }
}"""


def request(url, payload=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-card"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=40) as resp:
        body = resp.read()
        return resp.status, (json.loads(body) if body else None)


def graphql(variables):
    status, body = request(f"{API}/graphql", {"query": QUERY, "variables": variables})
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]["user"]


def fetch_user():
    """First page carries followers / calendar / counts; later pages only add repos."""
    node = graphql({"login": USER, "after": None})
    repos = list(node["repositories"]["nodes"])
    page = node["repositories"]["pageInfo"]
    while page["hasNextPage"]:
        more = graphql({"login": USER, "after": page["endCursor"]})["repositories"]
        repos += more["nodes"]
        page = more["pageInfo"]
    return node, repos


def lines_of_code(repos, budget_s=240):
    """Net lines (additions - deletions) authored by USER, via /stats/contributors."""
    total, start = 0, time.time()
    for r in repos:
        if r["isFork"] or time.time() - start > budget_s:
            continue
        url = f"{API}/repos/{r['nameWithOwner']}/stats/contributors"
        for _ in range(4):                       # GitHub answers 202 while it computes
            try:
                status, body = request(url)
            except urllib.error.HTTPError:
                break
            if status == 200 and body:
                for c in body:
                    if (c.get("author") or {}).get("login", "").lower() == USER.lower():
                        total += sum(w["a"] - w["d"] for w in c["weeks"])
                break
            time.sleep(3)
    return total


def build_stats(node, repos, loc, previous=None):
    cal = node["contributionsCollection"]["contributionCalendar"]
    weeks = [[(d["date"], LEVELS.get(d["contributionLevel"], 0)) for d in w["contributionDays"]]
             for w in cal["weeks"]]
    if not loc and previous:                      # keep the last good value if the calc came back empty
        loc = int(previous.get("loc_raw", 0))
    return {
        "user": USER,
        "stats": {
            "Repositories": f"{node['allRepos']['totalCount']:,}",
            "Contributions": f"{cal['totalContributions']:,}",
            "Lines of Code": f"{loc:,}",
        },
        "stats_right": {
            "Stars": f"{sum(r['stargazerCount'] for r in repos):,}",
            "Followers": f"{node['followers']['totalCount']:,}",
        },
        "loc_raw": loc,
        "calendar": weeks,
    }


def main():
    if not USER:
        sys.exit("Set GH_USER (or run inside GitHub Actions).")
    previous = None
    if os.path.exists("stats.json"):
        previous = json.load(open("stats.json"))
    node, repos = fetch_user()
    loc = 0 if os.environ.get("SKIP_LOC") == "1" else lines_of_code(repos)
    out = build_stats(node, repos, loc, previous)
    json.dump(out, open("stats.json", "w"), indent=1)
    print("stats:", out["stats"], out["stats_right"])


if __name__ == "__main__":
    main()
