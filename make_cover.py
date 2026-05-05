from PIL import Image, ImageDraw, ImageFont
import numpy as np

FONT_BOLD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

FRONT_PATH = "/root/.claude/uploads/91f55099-f56c-4f0f-be5a-e6587f3b0d81/019dd906-1000008064.png"
BACK_PATH  = "/root/.claude/uploads/91f55099-f56c-4f0f-be5a-e6587f3b0d81/019dd90b-1000008065.png"
OUT_PATH   = "/home/user/Ebook/cover_full.png"

AUTHOR     = "Lumi Doodle"

# KDP specs — 8.5"×8.5" square, 104 pages, white paper
DPI      = 300
PAGE_IN  = 8.5
BLEED_IN = 0.125
PAGES    = 104
SPINE_IN = PAGES * 0.002252

PAGE_PX  = round(PAGE_IN * DPI)               # 2550
BLEED_PX = round(BLEED_IN * DPI)              # 38
SPINE_PX = max(1, round(SPINE_IN * DPI))      # 70
H        = round((PAGE_IN + 2*BLEED_IN)*DPI)  # 2625
BACK_W   = PAGE_PX + BLEED_PX                 # 2588
FRONT_W  = PAGE_PX + BLEED_PX                 # 2588
W        = BACK_W + SPINE_PX + FRONT_W

# Safe zone: 0.375" from trim = 113px; + 38px bleed = 151px from canvas edge
SAFE     = BLEED_PX + round(0.375 * DPI)      # 151px from panel edge

print(f"Canvas : {W}×{H}px  ({W/DPI:.3f}\"×{H/DPI:.3f}\")")
print(f"Spine  : {SPINE_PX}px = {SPINE_IN:.4f}\" ({PAGES} pages)")


def fill_panel(img, panel_w, panel_h):
    """Scale image to fill entire panel edge-to-edge (satisfies bleed requirement)."""
    iw, ih = img.size
    scale  = max(panel_w / iw, panel_h / ih)
    nw, nh = round(iw * scale), round(ih * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    panel = Image.new("RGB", (panel_w, panel_h), "white")
    panel.paste(resized, ((panel_w - nw) // 2, (panel_h - nh) // 2))
    return panel


def apply_author_gradient(panel, name):
    """Dark gradient vignette at bottom — covers old name, author name drawn on top."""
    w, h  = panel.size
    grad_h = round(1.0 * DPI)          # gradient height: 1 inch
    grad_top = h - grad_h

    # Build semi-transparent black gradient overlay
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    for row in range(grad_top, h):
        alpha = int(200 * (row - grad_top) / grad_h)   # 0 → 200
        ov_draw.line([(0, row), (w, row)], fill=(0, 0, 0, alpha))

    # Composite onto panel
    base = panel.convert("RGBA")
    merged = Image.alpha_composite(base, overlay).convert("RGB")
    panel.paste(merged)

    # Author name in white, centered, within safe zone
    draw = ImageDraw.Draw(panel)
    fn   = ImageFont.truetype(FONT_BOLD, 72)
    cx   = w // 2
    y    = h - SAFE - round(0.15 * DPI)   # well inside safe zone
    draw.text((cx, y), name, fill=(255, 255, 255), font=fn, anchor="mm")


# Load and fill panels
front = fill_panel(Image.open(FRONT_PATH).convert("RGB"), FRONT_W, H)
back  = fill_panel(Image.open(BACK_PATH).convert("RGB"),  BACK_W,  H)

# Apply gradient + new author name on both panels
for panel in (front, back):
    apply_author_gradient(panel, AUTHOR)

# Sample spine gradient from front cover left edge (inside content)
top_col = front.getpixel((5, SAFE + 20))
mid_col = front.getpixel((5, H // 2))
bot_col = front.getpixel((5, H - SAFE - 20))

# Build canvas
canvas = Image.new("RGB", (W, H), (255, 255, 255))
canvas.paste(back,  (0, 0))
canvas.paste(front, (BACK_W + SPINE_PX, 0))

# Build spine gradient
spine_arr = np.zeros((H, SPINE_PX, 3), dtype=np.uint8)
for i in range(H):
    t = i / (H - 1)
    if t < 0.5:
        t2 = t * 2
        c = [int(top_col[j]*(1-t2) + mid_col[j]*t2) for j in range(3)]
    else:
        t2 = (t - 0.5) * 2
        c = [int(mid_col[j]*(1-t2) + bot_col[j]*t2) for j in range(3)]
    spine_arr[i, :] = c
canvas.paste(Image.fromarray(spine_arr), (BACK_W, 0))

# Spine text
TITLE_SZ  = min(44, SPINE_PX - 12)
AUTHOR_SZ = min(28, SPINE_PX - 26)
fn = ImageFont.truetype(FONT_BOLD, TITLE_SZ)
fs = ImageFont.truetype(FONT_REG,  AUTHOR_SZ)

txt = Image.new("RGBA", (H, SPINE_PX), (0, 0, 0, 0))
td  = ImageDraw.Draw(txt)
cx  = H // 2
cy  = SPINE_PX // 2
td.text((cx, cy - 2), "TINY MONSTERS", fill="white", font=fn, anchor="mb")
td.text((cx, cy + 2), AUTHOR,          fill="white", font=fs, anchor="mt")

txt_rot = txt.rotate(-90, expand=True)
canvas.paste(txt_rot, (BACK_W, 0), txt_rot)

canvas.save(OUT_PATH, "PNG", dpi=(DPI, DPI))
print(f"Saved → {OUT_PATH}")
