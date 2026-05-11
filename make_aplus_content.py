from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os

FONT_XB  = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
FONT_B   = "/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf"
FONT_SB  = "/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf"
FONT_REG = "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf"

# ── Source images ────────────────────────────────────────────────────────────
COVER_PATH   = "/root/.claude/uploads/e3aa924e-cb08-4062-b172-e0c76fa72e62/61afefb5-1000008430.png"
BANNER_IMG   = "/root/.claude/uploads/447c523b-8610-4a2b-97da-9625e3b823f9/ab67d2b9-1000008639.png"
ICONS_IMG    = "/root/.claude/uploads/447c523b-8610-4a2b-97da-9625e3b823f9/e715fc2d-1000008638.png"
PAGES_DIR    = "/home/user/Ebook/pages"
OUT_DIR      = "/home/user/Ebook/aplus"
os.makedirs(OUT_DIR, exist_ok=True)

# ── Brand colors ─────────────────────────────────────────────────────────────
RAINBOW = [(255,60,60),(255,160,0),(255,230,0),(60,200,80),(40,130,255),(160,60,255)]
BRAND_PURPLE = (90,  40, 160)
BRAND_DARK   = (28,  24,  48)
LIGHT_BG     = (252, 251, 255)
MID_GRAY     = (148, 140, 165)

def rainbow_color(t):
    n = len(RAINBOW) - 1
    pos = t * n
    i = min(int(pos), n - 1)
    f = pos - i
    c1, c2 = RAINBOW[i], RAINBOW[i+1]
    return tuple(round(c1[j] + (c2[j]-c1[j])*f) for j in range(3))

def rainbow_stripe(draw, y, x1, x2, h=10):
    for x in range(x1, x2):
        col = rainbow_color((x-x1) / max(x2-x1-1, 1))
        draw.line([(x,y),(x,y+h-1)], fill=col)

def drop_shadow(img, blur=14, offset=(10,10), color=(185,178,205)):
    pad = blur * 2
    W = img.width  + abs(offset[0]) + pad
    H = img.height + abs(offset[1]) + pad
    out = Image.new("RGB", (W, H), (255,255,255))
    sh  = Image.new("RGB", (img.width, img.height), color)
    out.paste(sh, (pad//2+offset[0], pad//2+offset[1]))
    out = out.filter(ImageFilter.GaussianBlur(blur))
    out.paste(img, (pad//2, pad//2))
    return out

def ld_logo(size=90, ring_w=8):
    """Small circular Lumi Doodle logo: rainbow ring + 'LD' in purple."""
    img  = Image.new("RGB", (size+ring_w*2+4, size+ring_w*2+4), (255,255,255))
    draw = ImageDraw.Draw(img)
    cx = cy = img.width // 2
    r  = size // 2
    # Rainbow ring
    steps = 720
    for i in range(steps):
        angle = 2*np.pi * i / steps
        col   = rainbow_color(i / steps)
        for rr in range(r, r+ring_w):
            x = round(cx + rr * np.cos(angle))
            y = round(cy + rr * np.sin(angle))
            if 0 <= x < img.width and 0 <= y < img.height:
                img.putpixel((x, y), col)
    # White fill inside
    draw.ellipse([cx-r+1, cy-r+1, cx+r-1, cy+r-1], fill=(255,255,255))
    # "LD" text
    fn = ImageFont.truetype(FONT_XB, round(size * 0.42))
    draw.text((cx, cy), "LD", fill=BRAND_PURPLE, font=fn, anchor="mm")
    return img


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 1 — Brand Banner  (970 × 380)
# ═════════════════════════════════════════════════════════════════════════════
def make_banner():
    W, H = 970, 380
    img  = Image.new("RGB", (W, H), (255,255,255))
    draw = ImageDraw.Draw(img)

    # ── Top strip: white bg + brand text ─────────────────────────────────────
    strip_h = 130
    # Subtle lavender gradient for top strip
    for y in range(strip_h):
        t = y / strip_h
        r = round(255 - t*14); g = round(255 - t*20); b = round(255 - t*8)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

    rainbow_stripe(draw, 0, 0, W, h=14)

    # LD logo
    logo = ld_logo(size=78, ring_w=7)
    logo_x = 32
    logo_y = (strip_h - logo.height) // 2 + 4
    img.paste(logo, (logo_x, logo_y))

    # Brand name
    fn_brand = ImageFont.truetype(FONT_XB, 74)
    draw.text((logo_x + logo.width + 22, strip_h//2 + 4),
              "LUMI DOODLE", fill=BRAND_PURPLE, font=fn_brand, anchor="lm")

    # Tagline right-aligned
    fn_tag = ImageFont.truetype(FONT_REG, 26)
    draw.text((W-28, strip_h//2 + 4),
              "Kawaii Coloring Books", fill=MID_GRAY, font=fn_tag, anchor="rm")

    rainbow_stripe(draw, strip_h-4, 0, W, h=4)

    # ── Bottom part: character banner image ──────────────────────────────────
    banner_h = H - strip_h
    banner = Image.open(BANNER_IMG).convert("RGB")
    # Crop to wide 970×banner_h keeping center
    bw, bh = banner.size
    scale  = max(W/bw, banner_h/bh)
    nb_w   = round(bw*scale); nb_h = round(bh*scale)
    banner = banner.resize((nb_w, nb_h), Image.LANCZOS)
    ox = (nb_w - W)  // 2
    oy = (nb_h - banner_h) // 2
    banner = banner.crop((ox, oy, ox+W, oy+banner_h))
    img.paste(banner, (0, strip_h))

    rainbow_stripe(draw, H-10, 0, W, h=10)

    img.save(os.path.join(OUT_DIR, "aplus_1_banner.png"))
    print("✓ Banner")


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 2 — Book Showcase  (970 × 420)
# ═════════════════════════════════════════════════════════════════════════════
def make_showcase():
    W, H = 970, 420
    img  = Image.new("RGB", (W, H), (255,255,255))
    draw = ImageDraw.Draw(img)

    rainbow_stripe(draw, 0, 0, W, h=10)

    # ── Left: cover at angle ─────────────────────────────────────────────────
    book_size = 300
    cover = Image.open(COVER_PATH).convert("RGB").resize(
        (book_size, book_size), Image.LANCZOS)
    cover_r  = cover.rotate(-10, expand=True, fillcolor=(255,255,255))
    with_sh  = drop_shadow(cover_r, blur=18, offset=(14,14))
    bx = 48
    by = (H - with_sh.height) // 2 + 10
    img.paste(with_sh, (bx, by))

    # ── Right: text block ─────────────────────────────────────────────────────
    tx = bx + with_sh.width + 40
    tw = W - tx - 36

    fn_series = ImageFont.truetype(FONT_REG, 24)
    fn_title  = ImageFont.truetype(FONT_XB,  52)
    fn_sub    = ImageFont.truetype(FONT_B,   30)
    fn_body   = ImageFont.truetype(FONT_REG, 26)

    ty = 40
    draw.text((tx, ty), "LUMI DOODLE PRESENTS",
              fill=MID_GRAY, font=fn_series, anchor="lt")
    ty += 38

    rainbow_stripe(draw, ty, tx, tx+tw, h=4)
    ty += 16

    draw.text((tx, ty), "TINY MONSTERS",
              fill=BRAND_PURPLE, font=fn_title, anchor="lt")
    ty += 62

    draw.text((tx, ty), "Cryptids of the USA",
              fill=BRAND_DARK, font=fn_sub, anchor="lt")
    ty += 48

    rainbow_stripe(draw, ty, tx, tx+tw, h=3)
    ty += 18

    points = [
        "50 original kawaii coloring pages",
        "One cryptid per U.S. state",
        "Single-sided — no bleed-through",
        "Large 8.5 x 8.5 inch format",
        "For kids, teens & adults",
    ]
    fn_dot = ImageFont.truetype(FONT_B, 25)
    fn_body2 = ImageFont.truetype(FONT_REG, 25)
    for i, pt in enumerate(points):
        col = rainbow_color(i / (len(points)-1))
        draw.text((tx,      ty), "▸", fill=col,        font=fn_dot,   anchor="lt")
        draw.text((tx + 26, ty), pt,  fill=BRAND_DARK,  font=fn_body2, anchor="lt")
        ty += 36

    # LD logo bottom-right corner
    logo = ld_logo(size=60, ring_w=6)
    img.paste(logo, (W - logo.width - 20, H - logo.height - 14))

    rainbow_stripe(draw, H-10, 0, W, h=10)

    img.save(os.path.join(OUT_DIR, "aplus_2_showcase.png"))
    print("✓ Showcase")


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 3 — Feature Icons  (970 × 360)
# ═════════════════════════════════════════════════════════════════════════════
def make_features():
    W, H = 970, 360
    img  = Image.new("RGB", (W, H), (255,255,255))
    draw = ImageDraw.Draw(img)

    rainbow_stripe(draw, 0, 0, W, h=10)

    # Load the AI-generated icons image and scale to fit
    icons = Image.open(ICONS_IMG).convert("RGB")
    icon_h = H - 100   # leave room for labels below
    scale  = icon_h / icons.height
    icon_w = round(icons.width * scale)
    icons  = icons.resize((icon_w, icon_h), Image.LANCZOS)
    ix = (W - icon_w) // 2
    iy = 10
    img.paste(icons, (ix, iy))

    # Text labels below each icon (4 equally spaced)
    fn_title = ImageFont.truetype(FONT_B,   26)
    fn_desc  = ImageFont.truetype(FONT_REG, 22)

    labels = [
        ("Easy to Color",       "Crisp line art"),
        ("50 U.S. States",      "One cryptid per state"),
        ("Kawaii Art Style",    "Cute for all ages"),
        ("For All Ages",        "Kids to adults"),
    ]
    spacing = W // 4
    label_y = iy + icon_h + 6
    for i, (title, desc) in enumerate(labels):
        cx = spacing // 2 + i * spacing
        col = rainbow_color(i / (len(labels)-1))
        draw.text((cx, label_y),      title, fill=col,       font=fn_title, anchor="mt")
        draw.text((cx, label_y + 32), desc,  fill=MID_GRAY,  font=fn_desc,  anchor="mt")

    rainbow_stripe(draw, H-10, 0, W, h=10)

    img.save(os.path.join(OUT_DIR, "aplus_3_features.png"))
    print("✓ Features")


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 4 — Pages Grid  (970 × 720)
# ═════════════════════════════════════════════════════════════════════════════
def make_pages_grid():
    W, H = 970, 720
    img  = Image.new("RGB", (W, H), LIGHT_BG)
    draw = ImageDraw.Draw(img)

    fn_h   = ImageFont.truetype(FONT_XB,  38)
    fn_lbl = ImageFont.truetype(FONT_SB,  22)
    fn_sub = ImageFont.truetype(FONT_REG, 20)

    rainbow_stripe(draw, 0, 0, W, h=10)
    draw.text((W//2, 20), "INSIDE THE BOOK",
              fill=BRAND_PURPLE, font=fn_h, anchor="mt")
    rainbow_stripe(draw, 68, 60, W-60, h=4)

    pages = [
        ("Monster_23.png",            "Mermaid of Pascagoula", "Mississippi"),
        ("Monster_29.png",            "Jersey Devil",          "New Jersey"),
        ("Monster_46_WASHINGTON.png", "Batsquatch",            "Washington"),
        ("Monster_49.png",            "Jackalope",             "Wyoming"),
        ("Monster_42.png",            "Momo",                  "Missouri"),
        ("Monster_11.png",            "Turtle Cove Monster",   "Hawaii"),
    ]
    rotations = [-3, 2, -2, 3, -1, 2]

    cols    = 3
    thumb   = 228
    gap_x   = (W - cols * thumb) // (cols + 1)
    start_y = 88
    row_h   = thumb + 62

    for idx, ((fname, name, state), angle) in enumerate(zip(pages, rotations)):
        col = idx % cols
        row = idx // cols
        cx  = gap_x + col*(thumb+gap_x) + thumb//2
        cy  = start_y + row*row_h + thumb//2

        path = os.path.join(PAGES_DIR, fname)
        pg   = Image.open(path).convert("RGB").resize(
            (thumb, thumb), Image.LANCZOS) if os.path.exists(path) else \
            Image.new("RGB", (thumb, thumb), (228,224,240))

        pg_r    = pg.rotate(angle, expand=True, fillcolor=(255,255,255))
        with_sh = drop_shadow(pg_r, blur=12, offset=(8,8), color=(185,178,205))

        img.paste(with_sh, (cx - with_sh.width//2 + 4, cy - with_sh.height//2 + 4))

        draw = ImageDraw.Draw(img)
        ly   = cy + pg_r.height//2 + 14
        col_c = rainbow_color(idx / (len(pages)-1))
        draw.text((cx, ly),    name,  fill=col_c,    font=fn_lbl, anchor="mt")
        draw.text((cx, ly+28), state, fill=MID_GRAY, font=fn_sub, anchor="mt")

    rainbow_stripe(draw, H-10, 0, W, h=10)

    img.save(os.path.join(OUT_DIR, "aplus_4_grid.png"))
    print("✓ Pages grid")


make_banner()
make_showcase()
make_features()
make_pages_grid()
print(f"\nAll A+ Content → {OUT_DIR}/")
print("Upload order on KDP: banner → showcase → features → grid")
