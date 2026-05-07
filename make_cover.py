from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

FRONT_PATH = "/root/.claude/uploads/e3aa924e-cb08-4062-b172-e0c76fa72e62/61afefb5-1000008430.png"
BACK_PATH  = "/root/.claude/uploads/e3aa924e-cb08-4062-b172-e0c76fa72e62/f97abaa8-1000008431.png"
PAGES_DIR  = "/home/user/Ebook/pages"
OUT_PATH   = "/home/user/Ebook/cover_full.png"

TITLE   = "TINY MONSTERS"
SUB     = "Cryptids of the USA"
VOL     = "Vol. 1"
TAG     = "A Kawaii Coloring Book"
AUTHOR  = "Lumi Doodle"

# 4 sample pages to preview on back cover
SAMPLES = [
    "Monster_05.png",   # California
    "Monster_11.png",   # Hawaii
    "Monster_31.png",   # New York
    "Monster_42.png",   # Texas
]

DPI      = 300
PAGE_IN  = 8.5
BLEED_IN = 0.125
PAGES    = 104
SPINE_IN = PAGES * 0.002252

PAGE_PX  = round(PAGE_IN * DPI)
BLEED_PX = round(BLEED_IN * DPI)
SPINE_PX = max(1, round(SPINE_IN * DPI))
H        = round((PAGE_IN + 2*BLEED_IN)*DPI)
BACK_W   = PAGE_PX + BLEED_PX
FRONT_W  = PAGE_PX + BLEED_PX
W        = BACK_W + SPINE_PX + FRONT_W
SAFE     = BLEED_PX + round(0.375 * DPI)   # 151px

RAINBOW = [
    (255,  60,  60),
    (255, 160,   0),
    (255, 230,   0),
    ( 60, 200,  80),
    ( 40, 130, 255),
    (160,  60, 255),
]

print(f"Canvas : {W}×{H}px  ({W/DPI:.3f}\"×{H/DPI:.3f}\")")
print(f"Spine  : {SPINE_PX}px = {SPINE_IN:.4f}\" ({PAGES} pages)")


def rainbow_color(t):
    n = len(RAINBOW) - 1
    pos = t * n
    i = min(int(pos), n - 1)
    f = pos - i
    c1, c2 = RAINBOW[i], RAINBOW[i + 1]
    return tuple(round(c1[j] + (c2[j] - c1[j]) * f) for j in range(3))


def fill_panel(img, panel_w, panel_h):
    iw, ih = img.size
    scale  = max(panel_w / iw, panel_h / ih)
    nw, nh = round(iw * scale), round(ih * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    panel = Image.new("RGB", (panel_w, panel_h), "white")
    panel.paste(resized, ((panel_w - nw) // 2, (panel_h - nh) // 2))
    return panel


def outlined_text(draw, x, y, text, font, fill, outline=(10,10,10), sw=5, anchor="mt"):
    for dx in range(-sw, sw + 1):
        for dy in range(-sw, sw + 1):
            if abs(dx) + abs(dy) >= sw:
                draw.text((x+dx, y+dy), text, fill=outline, font=font, anchor=anchor)
    draw.text((x, y), text, fill=fill, font=font, anchor=anchor)


def rainbow_stripe(draw, y, x1, x2, h=10):
    for x in range(x1, x2):
        col = rainbow_color((x - x1) / max(x2 - x1 - 1, 1))
        draw.line([(x, y), (x, y + h - 1)], fill=col)


def build_front(img):
    panel = fill_panel(img, FRONT_W, H)
    draw  = ImageDraw.Draw(panel)
    cx    = FRONT_W // 2
    x1, x2 = SAFE + 40, FRONT_W - SAFE - 40

    fn_title  = ImageFont.truetype(FONT_BOLD, 210)
    fn_sub    = ImageFont.truetype(FONT_BOLD, 88)
    fn_vol    = ImageFont.truetype(FONT_REG,  68)
    fn_tag    = ImageFont.truetype(FONT_BOLD, 74)
    fn_author = ImageFont.truetype(FONT_BOLD, 62)

    # Title — gold + black outline
    outlined_text(draw, cx, 195, TITLE, fn_title,
                  fill=(255,215,0), outline=(15,15,15), sw=7, anchor="mt")

    rainbow_stripe(draw, 440, x1, x2, h=10)

    outlined_text(draw, cx, 470, SUB, fn_sub,
                  fill=(255,255,255), outline=(15,15,15), sw=4, anchor="mt")

    outlined_text(draw, cx, 580, VOL, fn_vol,
                  fill=(255,255,255), outline=(15,15,15), sw=3, anchor="mt")

    # Bottom — tagline + author (all within safe zone)
    outlined_text(draw, cx, 2195, TAG, fn_tag,
                  fill=(255,255,255), outline=(15,15,15), sw=4, anchor="mt")

    rainbow_stripe(draw, 2292, x1, x2, h=10)

    # Author bottom: 2314 + 62 = 2376 < 2474 ✓
    outlined_text(draw, cx, 2314, AUTHOR, fn_author,
                  fill=(255,255,255), outline=(15,15,15), sw=3, anchor="mt")

    return panel


def build_back(img):
    panel = fill_panel(img, BACK_W, H)
    draw  = ImageDraw.Draw(panel)
    cx    = BACK_W // 2
    x1, x2 = SAFE + 40, BACK_W - SAFE - 40

    # ── 2×2 thumbnail grid ────────────────────────────────────────────────
    thumb = 840
    gap   = 48
    grid_w = 2 * thumb + gap
    grid_h = 2 * thumb + gap
    gx = (BACK_W - grid_w) // 2   # 429px — well inside safe zone
    gy = SAFE + 50                 # 201px from top

    for idx, filename in enumerate(SAMPLES):
        row = idx // 2
        col = idx % 2
        tx = gx + col * (thumb + gap)
        ty = gy + row * (thumb + gap)

        path = os.path.join(PAGES_DIR, filename)
        if os.path.exists(path):
            src = Image.open(path).convert("RGB").resize((thumb, thumb), Image.LANCZOS)
        else:
            src = Image.new("RGB", (thumb, thumb), (240,240,240))

        # Drop shadow
        draw.rectangle([tx+10, ty+10, tx+thumb+10, ty+thumb+10], fill=(150,150,150))
        panel.paste(src, (tx, ty))

        # Rainbow border around each thumbnail
        bw = 6
        for x in range(tx - bw, tx + thumb + bw):
            for edge_y in [ty - bw, ty + thumb + bw - 1]:
                if 0 <= x < BACK_W and 0 <= edge_y < H:
                    t = (x - (tx - bw)) / (thumb + 2*bw)
                    col = rainbow_color(min(t, 1.0))
                    panel.putpixel((x, edge_y), col)
        for y in range(ty - bw, ty + thumb + bw):
            for edge_x in [tx - bw, tx + thumb + bw - 1]:
                if 0 <= edge_x < BACK_W and 0 <= y < H:
                    t = (y - (ty - bw)) / (thumb + 2*bw)
                    col = rainbow_color(min(t, 1.0))
                    panel.putpixel((edge_x, y), col)

    # ── Rainbow separator + author ────────────────────────────────────────
    draw = ImageDraw.Draw(panel)
    y_sep = gy + grid_h + 60

    rainbow_stripe(draw, y_sep, x1, x2, h=10)

    fn_author = ImageFont.truetype(FONT_BOLD, 62)
    # Author bottom: y_sep+25+62 = depends on y_sep. Max y_sep≈1948, bottom≈2035 < 2474 ✓
    outlined_text(draw, cx, y_sep + 25, AUTHOR, fn_author,
                  fill=(255,255,255), outline=(15,15,15), sw=3, anchor="mt")

    # ── White barcode box (bottom right within safe zone) ─────────────────
    bc_w, bc_h = 520, 300
    bc_x = BACK_W - SAFE - bc_w
    bc_y = H - SAFE - bc_h
    draw.rectangle([bc_x, bc_y, bc_x+bc_w, bc_y+bc_h], fill=(255,255,255))
    draw.rectangle([bc_x, bc_y, bc_x+bc_w, bc_y+bc_h], outline=(180,180,180), width=2)

    return panel


# Build panels
front = build_front(Image.open(FRONT_PATH).convert("RGB"))
back  = build_back(Image.open(BACK_PATH).convert("RGB"))

# Canvas
canvas = Image.new("RGB", (W, H), (255,255,255))
canvas.paste(back,  (0, 0))
canvas.paste(front, (BACK_W + SPINE_PX, 0))

# Rainbow spine
spine_arr = np.zeros((H, SPINE_PX, 3), dtype=np.uint8)
for i in range(H):
    spine_arr[i, :] = rainbow_color(i / (H - 1))
canvas.paste(Image.fromarray(spine_arr), (BACK_W, 0))

# Spine text
fn_st = ImageFont.truetype(FONT_BOLD, min(44, SPINE_PX - 12))
fn_sa = ImageFont.truetype(FONT_REG,  min(28, SPINE_PX - 26))
txt   = Image.new("RGBA", (H, SPINE_PX), (0,0,0,0))
td    = ImageDraw.Draw(txt)
td.text((H//2, SPINE_PX//2 - 2), TITLE,  fill="white", font=fn_st, anchor="mb")
td.text((H//2, SPINE_PX//2 + 2), AUTHOR, fill="white", font=fn_sa, anchor="mt")
txt_r = txt.rotate(-90, expand=True)
canvas.paste(txt_r, (BACK_W, 0), txt_r)

canvas.save(OUT_PATH, "PNG", dpi=(DPI, DPI))
print(f"Saved → {OUT_PATH}")
