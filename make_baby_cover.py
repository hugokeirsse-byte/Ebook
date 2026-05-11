from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os

FONT_BOLD    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_FREDOKA = "/home/user/Ebook/fonts/FredokaOne-Regular.ttf"

FRONT_PATH = "/root/.claude/uploads/efcfd32a-2cb7-47d7-bd1a-d64c98070ebe/fc610695-1000008632.png"
BACK_PATH  = "/root/.claude/uploads/efcfd32a-2cb7-47d7-bd1a-d64c98070ebe/fbe7dae3-1000008633.png"
PAGES_DIR  = "/home/user/Ebook/MonsterFamilies/pages"
OUT_PATH   = "/home/user/Ebook/BabyCrossover_cover_full.png"

TITLE   = "BABY CROSSOVER"
SUB     = "Hybrid Monsters"
VOL     = "Vol. 1"
TAG     = "A Kawaii Coloring Book"
AUTHOR  = "Lumi Doodle"

# 2 sample pages to preview on back cover (full paths)
SAMPLES = [
    "/home/user/Ebook/MonsterFamilies/pages/Baby_15_JackOLantern_x_Wraith.jpg",
    "/home/user/Ebook/MonsterFamilies/pages/Baby_03_Ghost_x_Witch.jpg",
]

DPI      = 300
PAGE_IN  = 8.5
BLEED_IN = 0.125
PAGES    = 50
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


def bubble_rainbow_text(panel, x, y, text, font, outline_size=20, anchor="mt"):
    """Rainbow bubble text: crisp dilated outline + rainbow fill + white highlight."""
    tmp_draw = ImageDraw.Draw(panel)
    bbox = tmp_draw.textbbox((x, y), text, font=font, anchor=anchor)
    tx0, ty0, tx1, ty1 = bbox
    pad = outline_size + 24
    tw, th = tx1 - tx0 + 2 * pad, ty1 - ty0 + 2 * pad
    ox, oy = x - tx0 + pad, y - ty0 + pad

    # Render text white on black
    base = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(base).text((ox, oy), text, fill=255, font=font, anchor=anchor)

    # Dilate with 3 MaxFilter passes → approximates circular dilation (crisp outline)
    n = max(1, outline_size // 3)
    ks = n * 2 + 1
    dilated = base
    for _ in range(3):
        dilated = dilated.filter(ImageFilter.MaxFilter(ks))

    # Dark outline
    panel.paste(Image.new("RGB", (tw, th), (18, 18, 18)),
                (tx0 - pad, ty0 - pad), dilated)

    # Rainbow fill (slight blur for smooth edges, threshold back to crisp)
    fill_arr = np.array(base.filter(ImageFilter.GaussianBlur(radius=3)), float)
    fill_mask = Image.fromarray(np.clip(fill_arr * 5, 0, 255).astype(np.uint8))
    grad = np.zeros((th, tw, 3), dtype=np.uint8)
    for px in range(tw):
        grad[:, px, :] = rainbow_color(px / max(tw - 1, 1))
    panel.paste(Image.fromarray(grad), (tx0 - pad, ty0 - pad), fill_mask)

    # White highlight on top third for 3-D glossy look
    hi_h = th // 3
    hi_arr = np.array(base.crop((0, 0, tw, hi_h)), float)
    hi_mask = Image.fromarray(np.clip(hi_arr * 0.55, 0, 255).astype(np.uint8))
    panel.paste(Image.new("RGB", (tw, hi_h), (255, 255, 255)),
                (tx0 - pad, ty0 - pad), hi_mask)


def rainbow_stripe(draw, y, x1, x2, h=10):
    for x in range(x1, x2):
        col = rainbow_color((x - x1) / max(x2 - x1 - 1, 1))
        draw.line([(x, y), (x, y + h - 1)], fill=col)


def build_front(img):
    panel = fill_panel(img, FRONT_W, H)
    draw  = ImageDraw.Draw(panel)
    cx    = FRONT_W // 2
    x1, x2 = SAFE + 40, FRONT_W - SAFE - 40

    FONT_XB   = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
    fn_title  = ImageFont.truetype(FONT_XB,   228)
    fn_sub    = ImageFont.truetype(FONT_XB,    88)
    fn_vol    = ImageFont.truetype(FONT_XB,    66)
    fn_tag    = ImageFont.truetype(FONT_XB,    76)
    fn_author = ImageFont.truetype(FONT_XB,    62)

    # ── Title: big bubble rainbow ─────────────────────────────────────────
    bubble_rainbow_text(panel, cx, 180, TITLE, fn_title, outline_size=22, anchor="mt")

    rainbow_stripe(draw, 460, x1, x2, h=12)

    # ── Subtitle: medium bubble rainbow ──────────────────────────────────
    bubble_rainbow_text(panel, cx, 485, SUB, fn_sub, outline_size=13, anchor="mt")

    # ── Vol.: gold outlined ───────────────────────────────────────────────
    outlined_text(draw, cx, 615, VOL, fn_vol,
                  fill=(255, 230, 40), outline=(20, 20, 20), sw=5, anchor="mt")

    # ── Bottom tagline: bubble rainbow ───────────────────────────────────
    bubble_rainbow_text(panel, cx, 2185, TAG, fn_tag, outline_size=12, anchor="mt")

    rainbow_stripe(draw, 2300, x1, x2, h=12)

    # ── Author: white + strong outline (clean contrast) ───────────────────
    outlined_text(draw, cx, 2324, AUTHOR, fn_author,
                  fill=(255, 255, 255), outline=(20, 20, 20), sw=6, anchor="mt")

    return panel


def build_back(img):
    panel = fill_panel(img, BACK_W, H)
    draw  = ImageDraw.Draw(panel)
    cx    = BACK_W // 2
    x1, x2 = SAFE + 40, BACK_W - SAFE - 40

    # ── 1×2 thumbnail row (side by side) ─────────────────────────────────
    thumb = 900
    gap   = 50
    grid_w = 2 * thumb + gap
    grid_h = thumb
    gx = (BACK_W - grid_w) // 2
    gy = SAFE + 60   # thumbnails near top so back cover characters remain visible

    for idx, path in enumerate(SAMPLES):
        col = idx
        tx = gx + col * (thumb + gap)
        ty = gy

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
