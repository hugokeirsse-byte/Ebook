from PIL import Image, ImageDraw, ImageFont
import numpy as np

FONT_BOLD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

FRONT_PATH = "/root/.claude/uploads/91f55099-f56c-4f0f-be5a-e6587f3b0d81/019dd906-1000008064.png"
BACK_PATH  = "/root/.claude/uploads/91f55099-f56c-4f0f-be5a-e6587f3b0d81/019dd90b-1000008065.png"
OUT_PATH   = "/home/user/Ebook/cover_full.png"

# KDP specs — 8.5"×8.5" square, 104 pages, white paper
DPI      = 300
PAGE_IN  = 8.5
BLEED_IN = 0.125
PAGES    = 104
SPINE_IN = PAGES * 0.002252  # 0.2387"

PAGE_PX  = round(PAGE_IN * DPI)               # 2550
BLEED_PX = round(BLEED_IN * DPI)              # 38
SPINE_PX = max(1, round(SPINE_IN * DPI))      # 72
H        = round((PAGE_IN + 2*BLEED_IN)*DPI)  # 2625
BACK_W   = PAGE_PX + BLEED_PX                 # 2588
FRONT_W  = PAGE_PX + BLEED_PX                 # 2588
W        = BACK_W + SPINE_PX + FRONT_W        # 5248

print(f"Canvas : {W}×{H}px  ({W/DPI:.3f}\"×{H/DPI:.3f}\")")
print(f"Spine  : {SPINE_PX}px = {SPINE_IN:.4f}\" ({PAGES} pages)")


def fit_panel(img, panel_w, panel_h):
    """Scale image to fit entirely inside the panel — no cropping, white background for gap."""
    iw, ih = img.size
    scale  = min(panel_w / iw, panel_h / ih)
    nw, nh = round(iw * scale), round(ih * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    panel = Image.new("RGB", (panel_w, panel_h), "white")
    panel.paste(resized, ((panel_w - nw) // 2, (panel_h - nh) // 2))
    return panel


# Fit each panel — image fully visible, no cropping
front = fit_panel(Image.open(FRONT_PATH).convert("RGB"), FRONT_W, H)
back  = fit_panel(Image.open(BACK_PATH).convert("RGB"),  BACK_W,  H)

# Sample spine gradient from front cover left edge
top_col = front.getpixel((5, 10))
mid_col = front.getpixel((5, H // 2))
bot_col = front.getpixel((5, H - 10))

# Build canvas
canvas = Image.new("RGB", (W, H), (255, 255, 255))
canvas.paste(back,  (0, 0))
canvas.paste(front, (BACK_W + SPINE_PX, 0))

# Build spine gradient (numpy row-fill)
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

# Spine text — draw horizontally, then rotate -90° (reads top→bottom, US convention)
TITLE_SZ  = min(44, SPINE_PX - 12)
AUTHOR_SZ = min(28, SPINE_PX - 26)
fn = ImageFont.truetype(FONT_BOLD, TITLE_SZ)
fs = ImageFont.truetype(FONT_REG,  AUTHOR_SZ)

txt = Image.new("RGBA", (H, SPINE_PX), (0, 0, 0, 0))
td  = ImageDraw.Draw(txt)
cx  = H // 2
cy  = SPINE_PX // 2
td.text((cx, cy - 2), "TINY MONSTERS", fill="white", font=fn, anchor="mb")
td.text((cx, cy + 2), "Lumi Doodle",   fill="white", font=fs, anchor="mt")

txt_rot = txt.rotate(-90, expand=True)
canvas.paste(txt_rot, (BACK_W, 0), txt_rot)

canvas.save(OUT_PATH, "PNG", dpi=(DPI, DPI))
print(f"Saved → {OUT_PATH}")
