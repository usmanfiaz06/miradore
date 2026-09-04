#!/usr/bin/env python3
"""Generate Miradore company stamp + signature PNGs (transparent) for quotations."""

import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

TEAL = (15, 105, 115)
INK_BLUE = (24, 42, 110)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ------------------------------------------------------------------ stamp
S = 640
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
cx = cy = S // 2

def ring(radius, width, alpha=225):
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              outline=TEAL + (alpha,), width=width)

ring(300, 10)
ring(284, 3)
ring(196, 3)

def arc_text(text, radius, start, end, size, top=True, alpha=235):
    font = ImageFont.truetype(FONT_BOLD, size)
    n = len(text)
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        ang = start + (end - start) * (i / max(1, n - 1))
        ch_img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        cd = ImageDraw.Draw(ch_img)
        cd.text((60, 60), ch, font=font, fill=TEAL + (alpha,), anchor="mm")
        rot = (270 - ang) if top else (90 - ang)
        ch_img = ch_img.rotate(rot, resample=Image.BICUBIC)
        x = cx + radius * math.cos(math.radians(ang)) - 60
        y = cy + radius * math.sin(math.radians(ang)) - 60
        img.alpha_composite(ch_img, (int(round(x)), int(round(y))))

# top arc (reading over the top), bottom arc (reading along the bottom)
arc_text("MIRADORE EXPERIENCES", 240, 168, 372, 46, top=True)
arc_text("RIYADH  •  KSA", 238, 148, 32, 42, top=False)

# stars separating arcs
star_font = ImageFont.truetype(FONT_BOLD, 40)
for ang in (158, 22):
    x = cx + 242 * math.cos(math.radians(ang))
    y = cy + 242 * math.sin(math.radians(ang))
    d.text((x, y), "★", font=star_font, fill=TEAL + (235,), anchor="mm")

# center
f1 = ImageFont.truetype(FONT_BOLD, 62)
f2 = ImageFont.truetype(FONT_BOLD, 26)
d.text((cx, cy - 34), "MIRADORE", font=f1, fill=TEAL + (240,), anchor="mm")
d.text((cx, cy + 16), "EXPERIENCES", font=f2, fill=TEAL + (240,), anchor="mm")
d.line([cx - 140, cy + 46, cx + 140, cy + 46], fill=TEAL + (230,), width=4)
d.text((cx, cy + 78), "EVENTS  &  ENTERTAINMENT", font=ImageFont.truetype(FONT_BOLD, 22),
       fill=TEAL + (235,), anchor="mm")

# ink texture: speckle erosion for a genuine stamped look
import random
random.seed(7)
px = img.load()
for _ in range(26000):
    x = random.randrange(S)
    y = random.randrange(S)
    r_, g_, b_, a_ = px[x, y]
    if a_ > 0:
        px[x, y] = (r_, g_, b_, max(0, a_ - random.randrange(60, 220)))
img = img.rotate(-8, resample=Image.BICUBIC, expand=False)
img = img.filter(ImageFilter.GaussianBlur(0.6))
img.save("/home/user/miradore/miradore_stamp.png")

# ------------------------------------------------------------------ signature
W, H = 900, 320
sig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sig)

def bezier(pts, n=140):
    # de Casteljau for arbitrary-degree bezier
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

# flowing initial loop
stroke([(90, 240), (40, 90), (200, 20), (250, 150), (230, 250), (180, 240)], 7)
# connected middle flourish (piecewise to keep the peaks)
stroke([(230, 245), (300, 55), (360, 225)], 7)
stroke([(360, 225), (420, 70), (475, 215)], 6)
stroke([(475, 215), (540, 95), (600, 200)], 6)
# trailing tail
stroke([(600, 200), (680, 250), (780, 150), (860, 120)], 5)
# underline swoosh
stroke([(120, 285), (400, 320), (700, 260), (830, 230)], 4)
# dot accent
sd.ellipse([640, 100, 656, 116], fill=INK_BLUE + (235,))

sig = sig.filter(ImageFilter.GaussianBlur(0.8))
sig.save("/home/user/miradore/miradore_signature.png")
print("saved miradore_stamp.png + miradore_signature.png")
