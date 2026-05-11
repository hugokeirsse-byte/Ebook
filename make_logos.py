"""Generate 3 Mirabilia logo concepts."""
from PIL import Image, ImageDraw, ImageFont
import math, os

GOLD  = (168, 138, 82)
DARK  = (38,  32,  24)
CREAM = (252, 249, 242)
LGOLD = (210, 185, 130)

FC_REG  = "/home/user/Ebook/fonts/CormorantGaramond-Regular.ttf"
FC_BOLD = "/home/user/Ebook/fonts/CormorantGaramond-Bold.ttf"
FC_ITAL = "/home/user/Ebook/fonts/CormorantGaramond-Italic.ttf"
FP_BOLD = "/home/user/Ebook/fonts/PlayfairDisplay-Bold.ttf"
FP_ITAL = "/home/user/Ebook/fonts/PlayfairDisplay-Italic.ttf"
OUT     = "/home/user/Ebook"


def spaced(text, spacing=4):
    return (" " * spacing).join(text)


def draw_star4(d, cx, cy, r_out, r_in, fill, angle_offset=-45):
    """Draw a 4-pointed star (✦ shape) as a polygon."""
    pts = []
    for i in range(8):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(angle_offset + i * 45)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


# ── LOGO A — Typographic Star ─────────────────────────────────────────────────
def logo_a():
    W, H = 1100, 340
    img  = Image.new("RGB", (W, H), CREAM)
    d    = ImageDraw.Draw(img)
    cx   = W // 2

    # 4-pointed star
    draw_star4(d, cx, 56, 38, 12, GOLD)

    # Rule
    d.rectangle([cx-240, 106, cx+240, 107], fill=GOLD)

    # MIRABILIA
    fn_title = ImageFont.truetype(FC_BOLD, 86)
    d.text((cx, 114), spaced("MIRABILIA", 2), fill=DARK, font=fn_title, anchor="mt")

    # Rule
    d.rectangle([cx-240, 218, cx+240, 219], fill=GOLD)

    # Tagline
    fn_tag = ImageFont.truetype(FC_REG, 33)
    d.text((cx, 230), spaced("365  DAYS  OF  WONDER", 2),
           fill=GOLD, font=fn_tag, anchor="mt")

    img.save(os.path.join(OUT, "logo_a.png"))
    print("✓ logo_a.png")


# ── LOGO B — Orbital Monogram ─────────────────────────────────────────────────
def logo_b():
    W, H = 560, 520
    img  = Image.new("RGB", (W, H), CREAM)
    d    = ImageDraw.Draw(img)
    cx, cy = W // 2, 220

    # Concentric circles
    for r, lw in [(168, 2), (138, 1), (108, 1)]:
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=GOLD, width=lw)

    # Decorative dots on outer ring
    for i in range(16):
        angle = math.radians(i * 22.5)
        x = cx + 168 * math.cos(angle)
        y = cy + 168 * math.sin(angle)
        d.ellipse([x-3, y-3, x+3, y+3], fill=GOLD)

    # 4-pointed stars at cardinal points on outer ring
    for angle_deg in [0, 90, 180, 270]:
        angle = math.radians(angle_deg)
        sx = cx + 168 * math.cos(angle)
        sy = cy + 168 * math.sin(angle)
        draw_star4(d, sx, sy, 8, 3, GOLD)

    # M monogram
    fn_m = ImageFont.truetype(FP_BOLD, 148)
    d.text((cx, cy), "M", fill=DARK, font=fn_m, anchor="mm")

    # Thin rule
    d.rectangle([cx-185, cy+185, cx+185, cy+186], fill=GOLD)

    # MIRABILIA
    fn_title = ImageFont.truetype(FC_BOLD, 44)
    d.text((cx, cy+196), spaced("MIRABILIA", 3), fill=DARK, font=fn_title, anchor="mt")

    # ÉDITIONS
    fn_tag = ImageFont.truetype(FC_REG, 23)
    d.text((cx, cy+254), spaced("É D I T I O N S", 1), fill=GOLD, font=fn_tag, anchor="mt")

    img.save(os.path.join(OUT, "logo_b.png"))
    print("✓ logo_b.png")


# ── LOGO C — Armillary Sphere ─────────────────────────────────────────────────
def logo_c():
    W, H = 560, 580
    img  = Image.new("RGB", (W, H), CREAM)
    d    = ImageDraw.Draw(img)
    cx, cy = W // 2, 230

    R = 155  # outer radius

    # Outer equatorial circle
    d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=DARK, width=3)

    # Tilted ring 1 (30° tilt → ellipse with ry = R*sin(30°))
    ry1 = round(R * 0.5)
    d.ellipse([cx-R, cy-ry1, cx+R, cy+ry1], outline=GOLD, width=2)

    # Tilted ring 2 (60° tilt → ellipse with ry = R*sin(60°))
    ry2 = round(R * 0.87)
    rx2 = round(R * 0.5)
    d.ellipse([cx-rx2, cy-ry2, cx+rx2, cy+ry2], outline=GOLD, width=2)

    # Vertical ring (polar axis circle — thin ellipse)
    d.ellipse([cx-22, cy-R, cx+22, cy+R], outline=DARK, width=1)

    # Center star (drawn, not emoji)
    draw_star4(d, cx, cy, 18, 6, GOLD)

    # Outer circle again on top (clean border)
    d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=DARK, width=3)

    # Rule
    d.rectangle([cx-175, cy+R+24, cx+175, cy+R+25], fill=GOLD)

    # MIRABILIA
    fn_title = ImageFont.truetype(FC_BOLD, 52)
    d.text((cx, cy + R + 32), spaced("MIRABILIA", 2),
           fill=DARK, font=fn_title, anchor="mt")

    # Tagline
    fn_tag = ImageFont.truetype(FC_ITAL, 28)
    d.text((cx, cy + R + 96), "365 Days of Wonder",
           fill=GOLD, font=fn_tag, anchor="mt")

    img.save(os.path.join(OUT, "logo_c.png"))
    print("✓ logo_c.png")


logo_a()
logo_b()
logo_c()
