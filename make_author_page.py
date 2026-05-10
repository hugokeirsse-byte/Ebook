from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np
import os

FONT_XB  = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
FONT_B   = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ── Set this to your profile photo once generated ────────────────────────────
PHOTO_PATH = "/home/user/Ebook/author_photo.png"   # replace with real path
OUT_PATH   = "/home/user/Ebook/author_page.png"

# ── KDP page dimensions (8.5" × 8.5" + 0.125" bleed, 300 DPI) ───────────────
DPI      = 300
W_TRIM   = round(8.5   * DPI)   # 2550
H_TRIM   = round(8.5   * DPI)   # 2550
BLEED    = round(0.125 * DPI)   # 38
W        = W_TRIM + 2 * BLEED   # 2626
H        = H_TRIM + 2 * BLEED   # 2626
MARGIN   = round(0.375 * DPI)   # 113  ← KDP safe zone from trim edge
SAFE     = BLEED + MARGIN       # 151  ← from canvas edge

RAINBOW = [
    (255,  60,  60),
    (255, 160,   0),
    (255, 230,   0),
    ( 60, 200,  80),
    ( 40, 130, 255),
    (160,  60, 255),
]

BIO = (
    "Lumi Doodle is the pen name of an independent artist with a love "
    "for all things cute, quirky, and colorful. Inspired by kawaii culture "
    "and the rich world of folklore and mythology, Lumi creates coloring "
    "books that bring legendary creatures to life in the most adorable way possible.\n\n"
    "Whether it's a tiny Bigfoot exploring a national park or a baby dragon "
    "curled up with its family, every illustration is designed to spark joy "
    "and imagination — for kids and adults alike.\n\n"
    "When not drawing monsters, Lumi can be found collecting vintage postcards, "
    "drinking too much coffee, and planning the next volume."
)


def rainbow_color(t):
    n = len(RAINBOW) - 1
    pos = t * n
    i = min(int(pos), n - 1)
    f = pos - i
    c1, c2 = RAINBOW[i], RAINBOW[i + 1]
    return tuple(round(c1[j] + (c2[j] - c1[j]) * f) for j in range(3))


def rainbow_stripe(draw, y, x1, x2, h=10):
    for x in range(x1, x2):
        col = rainbow_color((x - x1) / max(x2 - x1 - 1, 1))
        draw.line([(x, y), (x, y + h - 1)], fill=col)


def circle_crop(img, size):
    """Resize image to size×size, crop to circle with white background."""
    img = img.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    result = Image.new("RGB", (size, size), (255, 255, 255))
    result.paste(img, (0, 0), mask)
    return result


def rainbow_ring(canvas, cx, cy, r, ring_w=18):
    """Draw a rainbow ring (outline circle) around a center point."""
    draw = ImageDraw.Draw(canvas)
    steps = 720
    for i in range(steps):
        angle0 = 2 * np.pi * i / steps
        angle1 = 2 * np.pi * (i + 1) / steps
        col = rainbow_color(i / steps)
        for rr in range(r, r + ring_w):
            x = round(cx + rr * np.cos(angle0))
            y = round(cy + rr * np.sin(angle0))
            if 0 <= x < canvas.width and 0 <= y < canvas.height:
                canvas.putpixel((x, y), col)


def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width pixels, respecting \n."""
    lines = []
    for paragraph in text.split("\n\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            w = draw.textlength(test, font=font)
            if w <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        lines.append("")   # blank line between paragraphs
    return lines


# ── Build the page ────────────────────────────────────────────────────────────
trim = Image.new("RGB", (W_TRIM, H_TRIM), (255, 255, 255))
draw = ImageDraw.Draw(trim)
cx   = W_TRIM // 2

# Fonts
fn_title  = ImageFont.truetype(FONT_XB,  110)
fn_label  = ImageFont.truetype(FONT_XB,   52)
fn_bio    = ImageFont.truetype(FONT_REG,  52)

# ── "About the Author" heading ────────────────────────────────────────────────
heading_y = MARGIN + 60
draw.text((cx, heading_y), "About the Author",
          fill=(40, 40, 40), font=fn_title, anchor="mt")

stripe_y = heading_y + 130
rainbow_stripe(draw, stripe_y, MARGIN + 40, W_TRIM - MARGIN - 40, h=12)

# ── Author photo (circle) ─────────────────────────────────────────────────────
photo_size  = 700
photo_cx    = cx
photo_cy    = stripe_y + 80 + photo_size // 2

if os.path.exists(PHOTO_PATH):
    photo_raw = Image.open(PHOTO_PATH).convert("RGB")
else:
    # Placeholder: pastel circle with initials
    photo_raw = Image.new("RGB", (photo_size, photo_size), (230, 210, 255))
    ph_draw   = ImageDraw.Draw(photo_raw)
    ph_font   = ImageFont.truetype(FONT_XB, 240)
    ph_draw.text((photo_size // 2, photo_size // 2), "LD",
                 fill=(140, 80, 200), font=ph_font, anchor="mm")

photo_circle = circle_crop(photo_raw, photo_size)
trim.paste(photo_circle,
           (photo_cx - photo_size // 2, stripe_y + 80))

# Rainbow ring around photo
rainbow_ring(trim, photo_cx, photo_cy, photo_size // 2 + 4, ring_w=16)

# ── "Lumi Doodle" name ────────────────────────────────────────────────────────
name_y = photo_cy + photo_size // 2 + 36
draw.text((cx, name_y), "Lumi Doodle",
          fill=(60, 60, 60), font=fn_label, anchor="mt")

stripe2_y = name_y + 68
rainbow_stripe(draw, stripe2_y, MARGIN + 100, W_TRIM - MARGIN - 100, h=8)

# ── Bio text ──────────────────────────────────────────────────────────────────
bio_x    = MARGIN + 60
bio_max_w = W_TRIM - 2 * (MARGIN + 60)
bio_y    = stripe2_y + 36
line_h   = 68   # line height in px

lines = wrap_text(BIO, fn_bio, bio_max_w, draw)
for line in lines:
    if line:
        draw.text((cx, bio_y), line, fill=(50, 50, 50), font=fn_bio, anchor="mt")
    bio_y += line_h

# ── Final rainbow stripe at bottom ────────────────────────────────────────────
bottom_stripe_y = H_TRIM - MARGIN - 20
rainbow_stripe(draw, bottom_stripe_y, MARGIN + 40, W_TRIM - MARGIN - 40, h=12)

# ── Add bleed and save ────────────────────────────────────────────────────────
canvas = Image.new("RGB", (W, H), (255, 255, 255))
canvas.paste(trim, (BLEED, BLEED))
canvas.save(OUT_PATH, "PNG", dpi=(DPI, DPI))
print(f"Saved → {OUT_PATH}  ({W}×{H}px, bleed included)")
