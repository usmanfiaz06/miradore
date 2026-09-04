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
# "Adeel Ahmad" in a flowing script hand with a flourish underline
W, H = 900, 320
sig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sig)

script = ImageFont.truetype("/home/user/miradore/fonts/GreatVibes-Regular.ttf", 148)
sd.text((450, 140), "Adeel Ahmad", font=script, fill=INK_BLUE + (238,), anchor="mm")

def bezier(pts, n=140):
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

def stroke(pts, width):
    path = bezier(pts)
    for a, b in zip(path, path[1:]):
        sd.line([a, b], fill=INK_BLUE + (235,), width=width)
        sd.ellipse([b[0] - width / 2, b[1] - width / 2, b[0] + width / 2, b[1] + width / 2],
                   fill=INK_BLUE + (235,))

# flourish underline
stroke([(150, 250), (420, 292), (700, 240), (810, 212)], 4)

sig = sig.rotate(-3, resample=Image.BICUBIC, expand=False)
sig = sig.filter(ImageFilter.GaussianBlur(0.6))
sig.save("/home/user/miradore/miradore_signature.png")
print("saved miradore_stamp.png + miradore_signature.png")
