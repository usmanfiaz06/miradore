#!/usr/bin/env python3
"""
Compose the cover background: a night highway seen head-on, long exposure.

Generated rather than sourced, so it carries no third-party branding and no
licence obligations. It is a placeholder - drop a Marsal fleet photograph in
at assets/cover.jpg (portrait, at least 1600 x 2200) and the cover picks it
up with no CSS changes. The page applies a heavy teal duotone over it, so
what reads through is form and light rather than photographic detail.

    python3 make_cover.py
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1654, 2339          # A4 at ~200 dpi
HORIZON = int(H * 0.40)
VP = (int(W * 0.5), HORIZON)   # vanishing point

random.seed(20260810)      # deterministic output


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def ground():
    """Night sky above the horizon, dark road plane below."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    sky_top, sky_low = (8, 22, 30), (26, 62, 66)
    for y in range(HORIZON):
        d.line([(0, y), (W, y)], fill=lerp(sky_top, sky_low, (y / HORIZON) ** 1.7))

    road_far, road_near = (20, 34, 38), (7, 11, 13)
    for y in range(HORIZON, H):
        t = (y - HORIZON) / (H - HORIZON)
        d.line([(0, y), (W, y)], fill=lerp(road_far, road_near, t ** 0.55))
    return img


def glow(img):
    """Warm haze sitting on the horizon."""
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    for r, c in ((760, (44, 92, 92)), (470, (78, 118, 108)), (250, (128, 142, 108))):
        d.ellipse([VP[0] - r * 1.7, HORIZON - r * 0.52,
                   VP[0] + r * 1.7, HORIZON + r * 0.52], fill=c)
    layer = layer.filter(ImageFilter.GaussianBlur(150))
    return Image.blend(img, Image.eval(img, lambda p: p), 0) if False else add(img, layer)


def add(base, layer, factor=1.0):
    """Additive composite, clamped."""
    b, l = base.split(), layer.split()
    out = []
    for i in range(3):
        out.append(Image.eval(b[i], lambda p: p).point(lambda p: p))
    merged = Image.merge("RGB", b)
    px_b, px_l = merged.load(), layer.load()
    for y in range(0, H):
        for x in range(0, W):
            r1, g1, b1 = px_b[x, y]
            r2, g2, b2 = px_l[x, y]
            px_b[x, y] = (min(255, int(r1 + r2 * factor)),
                          min(255, int(g1 + g2 * factor)),
                          min(255, int(b1 + b2 * factor)))
    return merged


def trail(layer, x_near, x_far, width_near, color, feather):
    """One light streak running from the foreground to the vanishing point."""
    d = ImageDraw.Draw(layer, "RGB")
    steps = 150
    for i in range(steps):
        t = i / steps
        y0 = H - (H - HORIZON) * (t ** 1.5)
        y1 = H - (H - HORIZON) * (((i + 1) / steps) ** 1.5)
        x0 = x_near + (x_far - x_near) * (1 - (y0 - HORIZON) / (H - HORIZON))
        x1 = x_near + (x_far - x_near) * (1 - (y1 - HORIZON) / (H - HORIZON))
        w = max(1, width_near * (1 - t) ** 1.25)
        fade = (1 - t) ** 0.45
        c = tuple(int(v * fade) for v in color)
        d.line([(x0, y0), (x1, y1)], fill=c, width=int(w))
    return layer.filter(ImageFilter.GaussianBlur(feather))


def lane_markings(layer):
    """Dashed centre line and edge lines, converging on the vanishing point."""
    d = ImageDraw.Draw(layer)
    for x_near, col in ((W * 0.5, (70, 78, 70)),
                        (W * 0.06, (44, 52, 52)), (W * 0.94, (44, 52, 52))):
        seg = 0
        i = 0.0
        while i < 1.0:
            t0, t1 = i, min(1.0, i + 0.028)
            y0 = H - (H - HORIZON) * (t0 ** 1.5)
            y1 = H - (H - HORIZON) * (t1 ** 1.5)
            x0 = x_near + (VP[0] - x_near) * (1 - (y0 - HORIZON) / (H - HORIZON))
            x1 = x_near + (VP[0] - x_near) * (1 - (y1 - HORIZON) / (H - HORIZON))
            if seg % 2 == 0:
                w = max(1, int(11 * (1 - t0) ** 1.3))
                f = (1 - t0) ** 0.7
                d.line([(x0, y0), (x1, y1)],
                       fill=tuple(int(v * f) for v in col), width=w)
            i += 0.028
            seg += 1
    return layer


def soften_horizon(img):
    """Blend the sky/road seam so the horizon reads as haze, not an edge."""
    band = 190
    top, bot = HORIZON - band, HORIZON + band
    strip = img.crop((0, top, W, bot)).filter(ImageFilter.GaussianBlur(34))
    mask = Image.new("L", (W, bot - top), 0)
    md = ImageDraw.Draw(mask)
    h = bot - top
    for y in range(h):
        a = 1.0 - abs(y - h / 2) / (h / 2)
        md.line([(0, y), (W, y)], fill=int(235 * (a ** 0.75)))
    img.paste(strip, (0, top), mask)
    return img


def grain_and_vignette(img):
    px = img.load()
    for y in range(H):
        dy = (y - H * 0.42) / (H * 0.72)
        for x in range(0, W):
            dx = (x - W * 0.5) / (W * 0.62)
            v = 1.0 - 0.72 * min(1.0, (dx * dx + dy * dy) ** 0.85)
            n = random.randint(-5, 5)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, int(r * v) + n)),
                        max(0, min(255, int(g * v) + n)),
                        max(0, min(255, int(b * v) + n)))
    return img


def build():
    img = ground()
    img = glow(img)

    lights = Image.new("RGB", (W, H), (0, 0, 0))
    lane_markings(lights)

    # Oncoming lane, cool. Outbound lane, warm - picking up the brand orange.
    for x_near, x_far, w, col, blur in (
        (W * 0.20, VP[0] - 26, 28, (196, 232, 236), 13),
        (W * 0.31, VP[0] - 16, 16, (150, 194, 202), 9),
        (W * 0.79, VP[0] + 24, 32, (246, 140, 62), 15),
        (W * 0.70, VP[0] + 14, 17, (196, 102, 44), 10),
        (W * 0.86, VP[0] + 34, 13, (158, 82, 38), 8),
    ):
        lights = add(lights, trail(Image.new("RGB", (W, H), (0, 0, 0)),
                                   x_near, x_far, w, col, blur))

    img = add(img, lights, 0.95)
    img = soften_horizon(img)
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    img = grain_and_vignette(img)
    img = ImageEnhance.Brightness(img).enhance(1.34)
    img = ImageEnhance.Contrast(img).enhance(1.18)
    img = ImageEnhance.Color(img).enhance(1.12)

    out = os.path.join(HERE, "cover.jpg")
    img.save(out, quality=88, optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    build()
