#!/usr/bin/env python3
"""Turns a portrait into a neon ASCII / dot-matrix image (photo_neon.png).
usage: python neon.py photo_src.jpg"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

src = sys.argv[1] if len(sys.argv) > 1 else "photo_src.jpg"
OUT_W, OUT_H = 524, 536            # 2x of the 262x268 card slot
CELL_W, CELL_H = 4, 7
RAMP = " .'`^,:;-~+=*x%#@"         # dark -> bright
BG = (7, 26, 45)
DARK, LIGHT = (18, 76, 140), (150, 232, 255)

im = Image.open(src).convert("RGB")
w, h = im.size
# crop to the card's aspect ratio, keeping head + shoulders
ch = int(w * OUT_H / OUT_W)
top = 25
im = im.crop((0, top, w, min(h, top + ch))).resize((OUT_W, OUT_H), Image.LANCZOS)

gray = ImageOps.grayscale(im)
gray = ImageOps.autocontrast(gray, cutoff=1)
gray = ImageOps.equalize(gray) if False else gray
arr = np.asarray(gray).astype(np.float32) / 255.0
blur = np.asarray(Image.fromarray((arr * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255.0
arr = np.clip(0.55 * arr + 1.1 * (arr - blur) + 0.12, 0, 1) ** 0.65

# soft mask: keep the person, fade the blurred background
yy, xx = np.mgrid[0:OUT_H, 0:OUT_W].astype(np.float32)
mk = Image.new("L", (OUT_W, OUT_H), 0)
md = ImageDraw.Draw(mk)
md.ellipse([OUT_W*0.45 - OUT_W*0.27, OUT_H*0.01, OUT_W*0.45 + OUT_W*0.27, OUT_H*0.80], fill=255)
md.polygon([(0, OUT_H*0.93), (OUT_W*0.24, OUT_H*0.85), (OUT_W*0.30, OUT_H*0.70), (OUT_W*0.62, OUT_H*0.68),
            (OUT_W*0.72, OUT_H*0.79), (OUT_W, OUT_H*0.88), (OUT_W, OUT_H), (0, OUT_H)], fill=255)
mask = mk.filter(ImageFilter.GaussianBlur(14))
m = np.asarray(mask).astype(np.float32) / 255.0
arr = arr * (0.04 + 0.96 * m)

# edge-fade at the borders
edge = np.minimum.reduce([xx, yy, OUT_W - 1 - xx, OUT_H - 1 - yy]) / 28.0
arr *= np.clip(edge, 0, 1)

cols, rows = OUT_W // CELL_W, OUT_H // CELL_H
small = np.asarray(Image.fromarray((arr * 255).astype(np.uint8)).resize((cols, rows), Image.BOX)).astype(np.float32) / 255.0

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 8)
layer = Image.new("RGB", (OUT_W, OUT_H), (0, 0, 0))
d = ImageDraw.Draw(layer)
for r in range(rows):
    for c in range(cols):
        v = small[r, c]
        if v < 0.08:
            continue
        ch_ = RAMP[min(len(RAMP) - 1, int(v * (len(RAMP) - 1) + 0.5))]
        if ch_ == " ":
            continue
        t = v ** 0.8
        col = tuple(int(DARK[i] + (LIGHT[i] - DARK[i]) * t) for i in range(3))
        d.text((c * CELL_W, r * CELL_H - 1), ch_, font=font, fill=col)

glow = layer.filter(ImageFilter.GaussianBlur(3))
out = Image.new("RGB", (OUT_W, OUT_H), BG)
bgarr = np.asarray(out).astype(np.float32)
res = bgarr + np.asarray(layer).astype(np.float32) + 0.55 * np.asarray(glow).astype(np.float32)
res = Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))
res.save("photo_neon.png", optimize=True)
res.quantize(96, dither=Image.NONE).save("photo_neon.png", optimize=True)
print("saved photo_neon.png")
