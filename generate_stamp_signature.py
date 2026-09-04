#!/usr/bin/env python3
"""Generate Miradore company stamp + signature PNGs (transparent) for quotations."""

import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

TEAL = (15, 105, 115)
INK_BLUE = (24, 42, 110)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ------------------------------------------------------------------ stamp
# Official rectangular company stamp: rasterized from the registered stamp PDF
# (Miradore_Stamp_Rectangular_Riyadh_v2.1.pdf), white background made transparent.
import subprocess
import tempfile, os

OFFICIAL = "/home/user/miradore/Miradore_Stamp_Rectangular_Riyadh_v2.1.pdf"
tmp = tempfile.mkdtemp()
subprocess.run(["pdftoppm", "-png", "-r", "300", OFFICIAL, os.path.join(tmp, "stamp")], check=True)
img = Image.open(os.path.join(tmp, "stamp-1.png")).convert("RGBA")
gray = img.convert("L")
img = img.crop(gray.point(lambda v: 255 if v < 245 else 0).getbbox())
px = img.load()
for y in range(img.height):
    for x in range(img.width):
        r, g, b, a = px[x, y]
        lum = (r + g + b) / 3
        alpha = max(0, min(255, int((255 - lum) * 1.6)))
        px[x, y] = (r, g, b, min(a, alpha) if alpha < 255 else a)
img = img.rotate(-5, resample=Image.BICUBIC, expand=True)
img.save("/home/user/miradore/miradore_stamp.png")

# ------------------------------------------------------------------ signature
# Hand-drawn signature traced from the Director's provided specimen
INK = (28, 28, 30)
GRAY = (125, 125, 125)
W, H = 900, 400
sig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sig)

def bezier(pts, n=180):
    out = []
    for t_i in range(n + 1):
        t = t_i / n
        p = [list(pt) for pt in pts]
        k = len(p)
        for lvl in range(1, k):
            for i in range(k - lvl):
                p[i][0] = p[i][0] * (1 - t) + p[i + 1][0] * t
                p[i][1] = p[i][1] * (1 - t) + p[i + 1][1] * t
        out.append((p[0][0], p[0][1]))
    return out

def stroke(pts, width, color=INK, alpha=242):
    path = bezier(pts)
    for a, b in zip(path, path[1:]):
        sd.line([a, b], fill=color + (alpha,), width=width)
        sd.ellipse([b[0]-width/2, b[1]-width/2, b[0]+width/2, b[1]+width/2], fill=color + (alpha,))

# first letter: big closed loop (D-belly), crossing itself
stroke([(212, 258), (196, 175), (204, 112), (248, 116), (256, 178), (232, 232), (206, 252)], 7)
# connected rounded double-hump (dd) flowing from the first letter
stroke([(206, 252), (238, 246), (252, 178), (262, 246), (250, 254)], 6)
stroke([(250, 254), (282, 244), (296, 174), (308, 244), (296, 254)], 6)
# tall ascender with a top loop, crossing back down
stroke([(296, 254), (330, 240), (336, 140), (326, 112), (352, 118), (356, 196), (346, 256)], 6)
# big rounded open bowl, connected
stroke([(346, 256), (420, 246), (444, 150), (400, 138), (372, 196), (392, 250), (438, 252)], 7)
# soft wave cluster (uuu), rounder
stroke([(438, 252), (452, 208), (468, 248), (484, 206), (500, 246), (516, 204), (534, 246)], 6)
# final letter: closed loop then out
stroke([(596, 248), (610, 160), (604, 128), (636, 134), (646, 200), (636, 252)], 6)
# tail right, then long slanted strike-through sweeping back left over the letters
stroke([(636, 252), (696, 258), (752, 214)], 6)
stroke([(752, 214), (570, 152), (300, 172), (140, 216), (60, 238)], 4)
# gray underline swoosh
stroke([(115, 318), (430, 340), (700, 312), (782, 296)], 5, GRAY, 210)

sig = sig.filter(ImageFilter.GaussianBlur(0.8))
sig.save("/home/user/miradore/miradore_signature.png")
print("ok")
