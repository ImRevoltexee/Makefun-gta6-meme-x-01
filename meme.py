#!/usr/bin/env python3
"""GTA 6 meme for make.fun bounty gta6-meme-x-01.

Draws (in code, Pillow only — no AI images, no copied GTA art):
Vice City sunset, the make.fun ghost driving a convertible, GTA-style
"MISSION PASSED / NUNGGU 13 TAHUN" — the 13-year wait since GTA V.
Ghost is the OFFICIAL mark from https://make.fun/press/mark-1024.png.
Output: 1200x675 JPEG, X-friendly, legible when shrunk to 768x480.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 675
OUT = "/home/hatch/workspace/makefun/meme-x/gta6-meme.jpg"
GHOST = "/home/hatch/workspace/makefun/meme-x/assets/ghost-clean.png"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img, "RGBA")

# ---------- sky gradient (Vice City sunset) ----------
stops = [
    (0.00, (29, 11, 56)),    # deep purple top
    (0.28, (123, 30, 122)),  # magenta
    (0.50, (232, 67, 147)),  # hot pink
    (0.68, (255, 123, 57)),  # orange
    (0.80, (255, 201, 60)),  # gold horizon
]
sky_bottom = 445
for y in range(sky_bottom):
    t = y / sky_bottom
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / max(t1 - t0, 1e-6)
            col = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
            break
    else:
        col = stops[-1][1]
    d.line([(0, y), (W, y)], fill=col)

# ---------- sun + glow ----------
sun_cx, sun_cy, sun_r = 600, 400, 88
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([sun_cx - sun_r - 55, sun_cy - sun_r - 55,
            sun_cx + sun_r + 55, sun_cy + sun_r + 55],
           fill=(255, 220, 120, 90))
glow = glow.filter(ImageFilter.GaussianBlur(30))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")
d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
          fill=(255, 243, 176))
# sun stripes (retro synthwave cut) — subtle, bottom of the sun
for i, yy in enumerate(range(sun_cy + 18, sun_cy + sun_r, 14)):
    half = int(math.sqrt(max(sun_r ** 2 - (yy - sun_cy) ** 2, 0)))
    d.line([(sun_cx - half, yy), (sun_cx + half, yy)],
           fill=(232, 67, 147), width=5)

# ---------- skyline silhouettes ----------
import random
random.seed(6)
SKYLINE = (42, 10, 61)
y_base = sky_bottom
x = -10
while x < W:
    bw = random.randint(45, 110)
    bh = random.randint(40, 150)
    d.rectangle([x, y_base - bh, x + bw, y_base], fill=SKYLINE)
    # antenna on some
    if random.random() < 0.35:
        d.line([(x + bw // 2, y_base - bh), (x + bw // 2, y_base - bh - 22)],
               fill=SKYLINE, width=4)
        d.ellipse([x + bw // 2 - 3, y_base - bh - 28, x + bw // 2 + 3, y_base - bh - 22],
                  fill=(255, 80, 120))
    # lit windows
    for _ in range(random.randint(2, 7)):
        wx = x + random.randint(6, max(bw - 8, 7))
        wy = y_base - random.randint(10, max(bh - 8, 11))
        d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 209, 102))
    x += bw + random.randint(2, 14)

# ---------- ocean band with sun reflection ----------
for y in range(sky_bottom, 520):
    t = (y - sky_bottom) / (520 - sky_bottom)
    col = tuple(int((59, 29, 94)[j] + ((29, 43, 74)[j] - (59, 29, 94)[j]) * t)
                for j in range(3))
    d.line([(0, y), (W, y)], fill=col)
for i, yy in enumerate(range(452, 518, 9)):
    wdt = random.randint(60, 220)
    xx = sun_cx - wdt // 2 + random.randint(-40, 40)
    alpha = 150 - i * 12
    d.line([(xx, yy), (xx + wdt, yy)], fill=(255, 200, 90, max(alpha, 40)), width=3)

# ---------- road / foreground ----------
d.rectangle([0, 520, W, H], fill=(18, 8, 31))
# road edge line
d.line([(0, 522), (W, 522)], fill=(255, 46, 136), width=3)


def star(cx, cy, r, fill, outline=None, width=2):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=outline)
    if outline:
        d.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def palm(x, y, s, lean=1):
    """Simple black palm silhouette, base at (x, y), scale s."""
    trunk_top = (x + 18 * lean * s, y - 150 * s)
    pts = []
    for t in [i / 12 for i in range(13)]:
        px = x + (trunk_top[0] - x) * t + 6 * s * math.sin(t * math.pi)
        py = y - 150 * s * t
        pts.append((px, py))
    for wdt in (10, 7, 4):
        d.line(pts, fill=(16, 6, 28), width=int(wdt * s), joint="curve")
    cx, cy = trunk_top
    for ang_deg in (-160, -125, -95, -65, -30, -10, 20):
        a = math.radians(ang_deg)
        ex = cx + 95 * s * math.cos(a) * lean
        ey = cy + 55 * s * math.sin(a) + 28 * s
        mx = cx + 55 * s * math.cos(a) * lean
        my = cy + 18 * s * math.sin(a) - 22 * s
        d.line([trunk_top, (mx, my), (ex, ey)], fill=(16, 6, 28),
               width=int(9 * s), joint="curve")


# palms framing the scene
palm(60, 530, 1.05, lean=1)
palm(1140, 532, 0.95, lean=-1)
palm(105, 528, 0.6, lean=1)

# ---------- ghost driver (official mark, disc removed so it reads as a
# character in the scene, not a pasted logo badge; pasted BEFORE the car
# so the car body covers its base and it looks seated) ----------
ghost = Image.open(GHOST).convert("RGBA")
GHOST_H = 340
ghost = ghost.resize((GHOST_H, GHOST_H), Image.LANCZOS)
ghost_x, ghost_top = 470, 340
img.paste(ghost, (ghost_x, ghost_top), ghost)
d = ImageDraw.Draw(img, "RGBA")

# ---------- convertible sports car silhouette (facing right) ----------
CAR = (13, 6, 22)
body = [(395, 596), (430, 566), (520, 556), (600, 552), (660, 552),
        (730, 558), (800, 570), (828, 592), (820, 612), (800, 622),
        (410, 622), (392, 612)]
d.polygon(body, fill=CAR)
# magenta rim light along the top edge
d.line([(430, 566), (520, 556), (600, 552), (660, 552), (730, 558), (800, 570)],
       fill=(255, 46, 136), width=4, joint="curve")
# side skirt highlight
d.line([(410, 622), (800, 622)], fill=(60, 20, 70), width=3)
# windshield hint
d.polygon([(600, 554), (655, 554), (640, 576), (610, 576)], fill=(90, 40, 110))
# headlight
d.ellipse([806, 584, 826, 598], fill=(255, 240, 180))
d.ellipse([810, 588, 822, 594], fill=(255, 255, 255))


def wheel(cx, cy, r=30):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(5, 3, 10),
              outline=(120, 60, 110), width=3)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(70, 60, 80))


wheel(485, 618)
wheel(730, 618)

# ---------- text ----------
def fit_font(text, max_w, start, font_path=FONT_BOLD):
    size = start
    while size > 20:
        f = ImageFont.truetype(font_path, size)
        if d.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(font_path, 20)


def text_center(y, text, font, fill, stroke=5, stroke_fill=(0, 0, 0)):
    bb = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    tw = bb[2] - bb[0]
    d.text(((W - tw) / 2 - bb[0], y), text, font=font, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)


# top-left location tag + top-right wanted stars
f_small = ImageFont.truetype(FONT_BOLD, 30)
d.text((30, 26), "VICE CITY", font=f_small, fill=(255, 255, 255),
       stroke_width=4, stroke_fill=(0, 0, 0))
for i in range(5):
    star(1050 + i * 34, 44, 15, fill=(255, 215, 0), outline=(0, 0, 0), width=2)

# headline
f_head = fit_font("MISSION PASSED", 1080, 108)
text_center(78, "MISSION PASSED", f_head, (255, 255, 255), stroke=7)
f_sub = fit_font("NUNGGU 13 TAHUN", 900, 56)
text_center(196, "NUNGGU 13 TAHUN", f_sub, (255, 209, 102), stroke=5)

# bottom corners
f_bot = ImageFont.truetype(FONT_BOLD, 30)
d.text((30, 628), "2013  →  2026", font=f_bot, fill=(255, 255, 255),
       stroke_width=4, stroke_fill=(0, 0, 0))
f_brand = ImageFont.truetype(FONT_BOLD, 38)
bb = d.textbbox((0, 0), "make.fun", font=f_brand, stroke_width=4)
d.text((W - 30 - (bb[2] - bb[0]), 622), "make.fun", font=f_brand,
       fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))

img.save(OUT, "JPEG", quality=92)
print("saved", OUT, img.size)
