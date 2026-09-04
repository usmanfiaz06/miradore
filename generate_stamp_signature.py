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
# Genuine director signature: rasterized from the signed invoice PDF in this repo
# (SECOND TRANCHE ADVANCE INVOICE...), white background made transparent.
SIG_SRC = "/home/user/miradore/SECOND TRANCHE ADVANCE INVOICE FOR EVENT AT RIYADH DIGITAL CITY.pdf"
tmp2 = tempfile.mkdtemp()
subprocess.run(["pdftoppm", "-png", "-r", "300", "-f", "1", "-l", "1", SIG_SRC, os.path.join(tmp2, "inv")], check=True)
page = Image.open(os.path.join(tmp2, "inv-1.png")).convert("RGB")
crop = page.crop((120, 2800, 790, 3062))  # signature + underline swoosh; stamp excluded

sig = Image.new("RGBA", crop.size, (0, 0, 0, 0))
po, pi = sig.load(), crop.load()
for y in range(crop.height):
    for x in range(crop.width):
        r, g, b = pi[x, y]
        lum = (r + g + b) / 3
        a = max(0.0, min(1.0, (245 - lum) / 160))
        po[x, y] = (r, g, b, int(a * 255))
sig = sig.crop(sig.getchannel("A").point(lambda v: 255 if v > 25 else 0).getbbox())
sig.save("/home/user/miradore/miradore_signature.png")
print("saved miradore_stamp.png + miradore_signature.png")
