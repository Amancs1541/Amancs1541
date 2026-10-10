#!/usr/bin/env python3
"""Generates profile.svg (README-ready), index.html (preview) and README snippet.
Edit the DATA section, run `python build.py`, commit profile.svg.
Optional: put a portrait at photo.jpg / photo.png next to this script to embed it."""
import base64, html, json, os, random, re

# ----------------------------- DATA ---------------------------------
NAME = "Aman Varma"
NAV = ["Secure Identities", "Automate Access", "Build Solutions", "Always Learning"]
INFO = [
    ("OS", "Security Enthusiast"),
    ("ROLE", "Identity & Access Management"),
    ("FOCUS", "IGA | Entra ID | Active Directory"),
    ("AUTOMATION", "Python | PowerShell | Microsoft Graph"),
    ("SECURITY", "SSO | MFA | PIM | Conditional Access"),
    ("CLOUD", "Azure | Microsoft 365"),
    ("LANGUAGES", "Python, PowerShell, SQL, JavaScript"),
    ("TOOLS", "Git, Docker, VS Code, FastAPI, React"),
    ("INTERESTS", "Identity Security, AI, Automation"),
    ("LOCATION", "Germany"),
    ("STATUS", "Always Learning, Always Building..."),
]
STATS = {"Repositories": "53", "Contributions": "129", "Lines of Code": "440,298"}
STATS_RIGHT = {"Stars": "342", "Followers": "180"}
_DATA = json.load(open("stats.json")) if os.path.exists("stats.json") else {}
STATS = _DATA.get("stats", STATS)
STATS_RIGHT = _DATA.get("stats_right", STATS_RIGHT)
USERNAME = (_DATA.get("user") or "aman").lower()
QUOTE = ["Turning", "Identity & Security", "concepts into", "practical solutions."]

SKILLS = [
    ("ID", "Identity & Access", ["Entra ID", "Active Directory", "IGA", "RBAC", "SSO", "MFA", "PIM"]),
    ("</>", "Programming", ["Python", "PowerShell", "SQL", "Java", "JavaScript", "TypeScript"]),
    ("{}", "Frameworks & Tools", ["FastAPI", "React", "Docker", "Git", "VS Code", "Postman"]),
    ("SEC", "Security & Cloud", ["Microsoft 365", "Azure", "Microsoft Graph", "Defender"]),
    ("DB", "Databases", ["MySQL", "PostgreSQL", "SQL Server"]),
]
CERTS = [
    ("ms", "Microsoft Certified", ["Identity and Access Administrator Associate (SC-300)",
                                   "Issued: 23 Jun 2026  |  Valid: 24 Jun 2027"], "Verified"),
    ("sp", "SailPoint", ["Identity Security Leader Credential", "Issued: 13 Sep 2026"], "Verified"),
    ("cisco", "Cisco Networking Academy", ["Python Essentials 1 | Ethical Hacker | Network Defense",
                                           "Introduction to Cybersecurity | Packet Tracer"], "Completed"),
]
PROJECTS = [
    ("AccessPilot", ["Identity Governance Platform", "for access requests, approvals", "and role-based access control."],
     ["Python", "FastAPI", "React"]),
    ("IAM Anomaly Detection", ["ML-based detection of anomalous", "identity activity using audit", "logs and behaviour analysis."],
     ["Python", "ML", "Scikit-learn"]),
    ("Active Directory Lab", ["Hands-on AD setup with users,", "groups, GPO and identity", "administration."],
     ["PowerShell", "Windows", "AD"]),
]
# ---------------------------------------------------------------------

BG, PANEL, LINE = "#06121e", "#081a2b", "#1d4468"
ACC, TXT, DIM, CYAN, GREEN = "#3aa0ff", "#cfe0ef", "#7f98b0", "#38d6f5", "#2fd08a"
W, H = 888, 656
esc = html.escape
o = []
a = o.append


def txt(x, y, s, cls="t", extra=""):
    a(f'<text x="{x}" y="{y}" class="{cls}" {extra}>{esc(s)}</text>')


def panel(x, y, w, h, title, idx):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{PANEL}" stroke="{LINE}"/>')
    a(f'<text x="{x+12}" y="{y+19}" class="t sm"><tspan fill="{ACC}">&gt;_</tspan> <tspan fill="{CYAN}">{esc(title)}</tspan></text>')
    a(f'<text x="{x+w-12}" y="{y+19}" class="t sm" text-anchor="end" fill="{DIM}">{idx}</text>')
    a(f'<line x1="{x+1}" y1="{y+28}" x2="{x+w-1}" y2="{y+28}" stroke="{LINE}" stroke-opacity=".6"/>')


def chip_w(label, fs=7.5):
    return len(label) * fs * 0.62 + 9


def chip(x, y, label, fs=7.5, h=15):
    w = chip_w(label, fs)
    a(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="4" fill="#0d2339" stroke="#23496c"/>')
    a(f'<text x="{x+w/2:.1f}" y="{y+h-4.5}" class="t" font-size="{fs}" text-anchor="middle">{esc(label)}</text>')
    return w + 4


# ---- header / defs
a(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(NAME)} profile card">')
a('''<defs>
<style>
.t{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;fill:#cfe0ef}
.name{font-weight:700;fill:#3aa0ff;letter-spacing:1px}
.k{fill:#5db4ff}
.cur{animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.pulse{animation:pulse 3s ease-in-out infinite}
@keyframes pulse{50%{opacity:.45}}
</style>
<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#2d8cff"/><stop offset="1" stop-color="#38d6f5"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#2d8cff" stop-opacity=".22"/><stop offset="1" stop-color="#2d8cff" stop-opacity="0"/></radialGradient>
<filter id="duo"><feColorMatrix type="matrix" values="0.2 0.5 0.1 0 0  0.3 0.6 0.2 0 0.04  0.5 0.9 0.3 0 0.1  0 0 0 1 0"/></filter>
<clipPath id="pc"><rect x="14" y="58" width="262" height="268" rx="6"/></clipPath>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# ---- top bar
a(f'<text x="12" y="30" class="t" font-size="12.5"><tspan fill="{GREEN}">{esc(USERNAME)}@github</tspan><tspan fill="{DIM}">:~$</tspan> neofetch<tspan class="cur" fill="{ACC}"> ▌</tspan></text>')
nx = W - 14
for i, n in enumerate(reversed(NAV)):
    nx -= len(n) * 6.6
    a(f'<text x="{nx:.1f}" y="30" class="t sm" fill="#8fb4d6">{esc(n)}</text>')
    nx -= 10
    if i < len(NAV) - 1:
        a(f'<text x="{nx-2:.1f}" y="30" class="t sm" fill="{LINE}">|</text>')
        nx -= 10
a(f'<line x1="0" y1="42" x2="{W}" y2="42" stroke="{LINE}" stroke-opacity=".5"/>')

# ---- hero panel
a(f'<rect x="3" y="48" width="{W-6}" height="288" rx="8" fill="{PANEL}" stroke="{LINE}"/>')

# globe (dot matrix)
random.seed(7)
gx, gy, gr = 805, 150, 92
a(f'<circle cx="{gx}" cy="{gy}" r="{gr+20}" fill="url(#glow)"/>')
for yy in range(gy - gr, gy + gr, 6):
    for xx in range(gx - gr, gx + gr, 6):
        d = ((xx - gx) ** 2 + (yy - gy) ** 2) ** .5
        if d < gr and random.random() < .5 + .25 * (1 - d / gr) and xx > 690:
            a(f'<circle cx="{xx}" cy="{yy}" r="1.5" fill="#4ea8ff" opacity="{random.uniform(.25,.8):.2f}"/>')

# portrait
photo = next((p for p in ("photo_neon.png", "photo.jpg", "photo.jpeg", "photo.png") if os.path.exists(p)), None)
a(f'<g clip-path="url(#pc)">')
a('<rect x="14" y="58" width="262" height="268" fill="#071a2d"/>')
if photo:
    mime = "image/png" if photo.endswith("png") else "image/jpeg"
    b64 = base64.b64encode(open(photo, "rb").read()).decode()
    flt = '' if photo == "photo_neon.png" else ' filter="url(#duo)"'
    a(f'<image x="14" y="58" width="262" height="268" preserveAspectRatio="xMidYMid slice"{flt} href="data:{mime};base64,{b64}"/>')
else:
    a(f'<circle cx="145" cy="150" r="48" fill="#0d2f4d" stroke="{ACC}" stroke-opacity=".5"/>')
    a(f'<path d="M50 326 C60 236 230 236 240 326Z" fill="#0d2f4d" stroke="{ACC}" stroke-opacity=".5"/>')
    a(f'<text x="145" y="290" class="t sm" text-anchor="middle" fill="{DIM}">run neon.py on your photo, then rebuild</text>')
a('</g>')
a(f'<rect x="14" y="58" width="262" height="268" rx="6" fill="none" stroke="{LINE}"/>')

# info
txt(294, 78, NAME, "t name")
a(f'<line x1="294" y1="86" x2="615" y2="86" stroke="{LINE}" stroke-dasharray="3 3"/>')
y = 108
for k, v in INFO:
    a(f'<text x="294" y="{y}" class="t"><tspan class="k">{esc(k)}</tspan></text>')
    a(f'<text x="372" y="{y}" class="t" fill="{DIM}">:</text>')
    a(f'<text x="386" y="{y}" class="t">{esc(v)}</text>')
    y += 14.6
txt(294, 272, "GitHub Stats", "t sm", f'fill="{ACC}"')
a(f'<line x1="372" y1="268" x2="615" y2="268" stroke="{LINE}" stroke-dasharray="3 3"/>')
sy = 289
for k, v in STATS.items():
    a(f'<text x="294" y="{sy}" class="t">{esc(k)}</text><text x="372" y="{sy}" class="t" fill="{DIM}">:</text>')
    a(f'<text x="386" y="{sy}" class="t" fill="{CYAN}">{esc(v)}</text>')
    sy += 15
sy = 289
for k, v in STATS_RIGHT.items():
    a(f'<text x="464" y="{sy}" class="t" fill="{ACC}" font-weight="700">{esc(k)}</text>')
    a(f'<text x="520" y="{sy}" class="t" fill="{DIM}">:</text><text x="534" y="{sy}" class="t" fill="{CYAN}">{esc(v)}</text>')
    sy += 15
for i in range(11):
    a(f'<rect x="{464+i*14}" y="314" width="11" height="8" fill="{ACC}" class="pulse" style="animation-delay:{i*0.15:.2f}s"/>')
a(f'<rect x="{464+11*14}" y="314" width="{14*5}" height="8" fill="#0d2339"/>')

# quote
a(f'<rect x="730" y="232" width="146" height="98" rx="6" fill="#071a2d" stroke="{ACC}" stroke-opacity=".7"/>')
a(f'<text x="742" y="256" fill="{ACC}" font-size="22" font-family="Georgia,serif" font-weight="700">“</text>')
for i, l in enumerate(QUOTE):
    a(f'<text x="742" y="{266+i*13}" class="t" font-size="10.5">{esc(l)}</text>')
a(f'<rect x="742" y="319" width="18" height="2" fill="{ACC}"/>')

# ---- skills
panel(3, 348, 438, 192, "skills --list", "01")
ry = 382
CHIP_X0, CHIP_LIMIT = 158, 432
for icon, cat, chips in SKILLS:
    # lay chips out first so a long row can wrap to a second line
    pos, cx, line = [], CHIP_X0, 0
    for c in chips:
        w = chip_w(c)
        if cx + w > CHIP_LIMIT:
            cx, line = CHIP_X0, line + 1
        pos.append((c, cx, line))
        cx += w + 4
    lines = line + 1
    rh = 18 * lines + 7
    mid = ry + (18 * lines) / 2
    a(f'<rect x="14" y="{mid-12:.1f}" width="30" height="24" rx="6" fill="#0d2339" stroke="#23496c"/>')
    a(f'<text x="29" y="{mid+3.5:.1f}" class="t" font-size="9" text-anchor="middle" fill="{CYAN}">{esc(icon)}</text>')
    a(f'<text x="52" y="{mid+3.5:.1f}" class="t" font-size="9" fill="{CYAN}">{esc(cat)}</text>')
    for c, x_, ln in pos:
        chip(x_, ry + ln * 18, c)
    ry += rh

# ---- certifications
panel(449, 348, 436, 192, "certifications --list", "02")
cy = 390
for logo, title, lines, status in CERTS:
    lx = 462
    if logo == "ms":
        for i, c in enumerate(["#f25022", "#7fba00", "#00a4ef", "#ffb900"]):
            a(f'<rect x="{lx+(i%2)*15}" y="{cy+4+(i//2)*15}" width="13" height="13" fill="{c}"/>')
    elif logo == "sp":
        a(f'<path d="M{lx+14} {cy+2} L{lx+30} {cy+32} L{lx} {cy+32}Z" fill="#c2185b"/><path d="M{lx+14} {cy+2} L{lx+30} {cy+32} L{lx+14} {cy+22}Z" fill="#5b3fd1"/>')
    else:
        for i, hh in enumerate([8, 14, 20, 14, 8]):
            a(f'<rect x="{lx+i*7}" y="{cy+22-hh}" width="4" height="{hh}" fill="#1ba0d7"/>')
        a(f'<text x="{lx}" y="{cy+34}" class="t" font-size="10" fill="#cfe0ef" letter-spacing="2">CISCO</text>')
    a(f'<text x="512" y="{cy+8}" class="t" font-size="12" font-weight="700">{esc(title)}</text>')
    for i, l in enumerate(lines):
        a(f'<text x="512" y="{cy+22+i*12}" class="t" font-size="8.3" fill="#9bb4cc">{esc(l)}</text>')
    pw = 74 if status == "Verified" else 72
    col = GREEN if status == "Verified" else ACC
    px = 449 + 436 - 12 - pw
    a(f'<rect x="{px}" y="{cy+(4 if status!="Completed" else 4)}" width="{pw}" height="20" rx="10" fill="none" stroke="{col}"/>')
    if status == "Verified":
        a(f'<circle cx="{px+13}" cy="{cy+14}" r="3" fill="{col}"/>')
        a(f'<text x="{px+22}" y="{cy+18}" class="t" font-size="10" fill="{col}">{status}</text>')
    else:
        a(f'<text x="{px+pw/2}" y="{cy+18}" class="t" font-size="10" fill="{col}" text-anchor="middle">{status}</text>')
    cy += 49
    if cy < 500:
        a(f'<line x1="452" y1="{cy-8}" x2="882" y2="{cy-8}" stroke="{LINE}" stroke-opacity=".6"/>')

# ---- projects
panel(3, 550, 618, 102, "projects --list", "03")
pxs = [14, 214, 418]
for (title, desc, tags), px in zip(PROJECTS, pxs):
    a(f'<rect x="{px}" y="584" width="22" height="22" rx="5" fill="none" stroke="{ACC}"/>')
    a(f'<circle cx="{px+11}" cy="595" r="4" fill="none" stroke="{ACC}"/>')
    a(f'<text x="{px+32}" y="599" class="t" font-size="10.5" font-weight="700" fill="#5db4ff">{esc(title)}</text>')
    for i, l in enumerate(desc):
        a(f'<text x="{px}" y="{615+i*9.5}" class="t" font-size="7.8" fill="#9bb4cc">{esc(l)}</text>')
    cx = px
    for tg in tags:
        cx += chip(cx, 636, tg, 7.5, 13)

# ---- activity graph
panel(629, 550, 256, 102, "activity --graph", "04")
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
shades = ["#0d2339", "#12365a", "#1a5190", "#2878d4", "#3aa0ff"]
GX, GY, PX, PY, WEEKS = 640, 598, 6.9, 6.2, 34
cal = (_DATA.get("calendar") or [])[-WEEKS:]
if not cal:                                  # placeholder until stats.json exists
    random.seed(42)
    cal = [[("2000-%02d-01" % (1 + c * 12 // WEEKS), random.choices(range(5), weights=[3, 3, 3, 2, 1])[0])
            for _ in range(7)] for c in range(WEEKS)]
prev_m, last_lbl = None, -9
for ci, week in enumerate(cal):
    m = int(week[0][0][5:7])
    if m != prev_m and ci - last_lbl >= 4 and GX + ci * PX < 845:
        a(f'<text x="{GX + ci * PX:.1f}" y="591" class="t" font-size="7" fill="{DIM}">{MONTHS[m - 1]}</text>')
        last_lbl = ci
    prev_m = m
    for ri, (date, lvl) in enumerate(week):
        a(f'<rect x="{GX + ci * PX:.1f}" y="{GY + ri * PY:.1f}" width="5.6" height="5.2" rx="1" fill="{shades[lvl]}"/>')

a('</svg>')
svg = "\n".join(o)
def _fs(m):
    tag = m.group(0)
    if "font-size=" in tag:
        return tag
    size = "26" if 'class="t name"' in tag else ("11" if "t sm" in tag else "11.5")
    return tag[:-1] + f' font-size="{size}">'
svg = re.sub(r"<text [^>]*>", _fs, svg)
open("profile.svg", "w", encoding="utf-8").write(svg)

open("index.html", "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(NAME)} - profile card preview</title>
<style>body{{margin:0;background:#010409;display:grid;place-items:center;min-height:100vh}}
svg{{max-width:100%;height:auto}}</style></head>
<body>
{svg}
</body></html>""")

open("README_snippet.md", "w", encoding="utf-8").write("""<p align="center">
  <img src="profile.svg" alt="Profile card" width="100%"/>
</p>
""")
print("ok", len(svg) // 1024, "KB")
