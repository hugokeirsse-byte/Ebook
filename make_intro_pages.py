"""
Generates polished interior intro pages for Tiny Monsters Vol.1 (KDP 2626×2626px):
  - intro_title_page.png   : illustrated title page
  - intro_belongs_page.png : "This Book Belongs To:" page
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import math, os

# ── Fonts ──────────────────────────────────────────────────────────────────────
FXB   = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
FB    = "/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf"
FSB   = "/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf"
FREG  = "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf"
FFRED = "/home/user/Ebook/fonts/FredokaOne-Regular.ttf"

# ── Assets ────────────────────────────────────────────────────────────────────
LOGO_IMG   = "/root/.claude/uploads/adbfa1c5-eebd-450f-a73d-c4c8c5acf7a6/b8607b1b-1000008640.png"
BANNER_IMG = "/root/.claude/uploads/447c523b-8610-4a2b-97da-9625e3b823f9/ab67d2b9-1000008639.png"
PAGES_DIR  = "/home/user/Ebook/pages"
OUT_DIR    = "/home/user/Ebook"

# ── KDP dimensions ────────────────────────────────────────────────────────────
DPI      = 300
W_TRIM   = round(8.5   * DPI)   # 2550
H_TRIM   = round(8.5   * DPI)   # 2550
BLEED    = round(0.125 * DPI)   # 38
W        = W_TRIM + 2 * BLEED   # 2626
H        = H_TRIM + 2 * BLEED   # 2626
MARGIN   = round(0.375 * DPI)   # 113  — safe zone

# ── Brand colors ──────────────────────────────────────────────────────────────
RAINBOW      = [(255,60,60),(255,160,0),(255,230,0),(60,200,80),(40,130,255),(160,60,255)]
BRAND_PURPLE = (90,  40, 160)
BRAND_DARK   = (28,  24,  48)
MID_GRAY     = (140, 132, 158)


# ── Helpers ───────────────────────────────────────────────────────────────────

def rainbow_color(t):
    n = len(RAINBOW)-1; pos = t*n; i = min(int(pos),n-1); f = pos-i
    c1,c2 = RAINBOW[i],RAINBOW[i+1]
    return tuple(round(c1[j]+(c2[j]-c1[j])*f) for j in range(3))


def rainbow_gradient(W, H, alpha_top=90, alpha_bot=60):
    """Soft pastel rainbow gradient background."""
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    for x in range(W):
        c = rainbow_color(x / max(W-1, 1))
        for y in range(H):
            blend = alpha_top + (alpha_bot - alpha_top) * y / max(H-1, 1)
            arr[y, x] = (*c, int(blend))
    return Image.fromarray(arr, 'RGBA')


def soft_bg(W, H):
    """Cream-white background with very light rainbow wash."""
    base = Image.new("RGB", (W, H), (252, 250, 248))
    gradient = rainbow_gradient(W, H, alpha_top=55, alpha_bot=35)
    base.paste(gradient, (0, 0), gradient)
    return base


def stripe(draw, y, x1, x2, h=12):
    for x in range(x1, x2):
        draw.line([(x,y),(x,y+h-1)], fill=rainbow_color((x-x1)/max(x2-x1-1,1)))


def text_centered(draw, cx, y, txt, font, fill, outline=(255,255,255), sw=3):
    for dx in range(-sw, sw+1):
        for dy in range(-sw, sw+1):
            if dx*dx+dy*dy <= sw*sw:
                draw.text((cx+dx, y+dy), txt, fill=outline, font=font, anchor="mt")
    draw.text((cx, y), txt, fill=fill, font=font, anchor="mt")


def fit_width(img, W):
    s = W / img.width
    return img.resize((W, round(img.height*s)), Image.LANCZOS)


def fit_height(img, H):
    s = H / img.height
    return img.resize((round(img.width*s), H), Image.LANCZOS)


def fit_fill(img, W, H):
    iw, ih = img.size; s = max(W/iw, H/ih)
    nw, nh = round(iw*s), round(ih*s)
    img = img.resize((nw, nh), Image.LANCZOS)
    return img.crop(((nw-W)//2, (nh-H)//2, (nw-W)//2+W, (nh-H)//2+H))


def drop_shadow(img, blur=12, offset=(8,8), color=(200,190,220)):
    pad = blur*2
    W2 = img.width+abs(offset[0])+pad; H2 = img.height+abs(offset[1])+pad
    out = Image.new("RGB",(W2,H2),(255,255,255))
    out.paste(Image.new("RGB",img.size,color),(pad//2+offset[0],pad//2+offset[1]))
    out = out.filter(ImageFilter.GaussianBlur(blur))
    out.paste(img,(pad//2,pad//2))
    return out


def bubble_rainbow_text(panel, x, y, text, font, outline_size=28, anchor="mt"):
    """Rainbow bubble letters — same technique as make_cover.py."""
    tmp = ImageDraw.Draw(panel)
    bbox = tmp.textbbox((x,y), text, font=font, anchor=anchor)
    tx0,ty0,tx1,ty1 = bbox
    pad = outline_size + 28
    tw, th = tx1-tx0+2*pad, ty1-ty0+2*pad
    ox, oy = x-tx0+pad, y-ty0+pad

    base = Image.new("L",(tw,th),0)
    ImageDraw.Draw(base).text((ox,oy), text, fill=255, font=font, anchor=anchor)

    n = max(1, outline_size//3); ks = n*2+1
    dilated = base
    for _ in range(3):
        dilated = dilated.filter(ImageFilter.MaxFilter(ks))

    panel.paste(Image.new("RGB",(tw,th),(20,20,20)), (tx0-pad,ty0-pad), dilated)

    fill_arr = np.array(base.filter(ImageFilter.GaussianBlur(3)), float)
    fill_mask = Image.fromarray(np.clip(fill_arr*5, 0, 255).astype(np.uint8))
    grad = np.zeros((th,tw,3), dtype=np.uint8)
    for px in range(tw):
        grad[:,px,:] = rainbow_color(px/max(tw-1,1))
    panel.paste(Image.fromarray(grad), (tx0-pad,ty0-pad), fill_mask)

    hi_h = th//3
    hi_arr = np.array(base.crop((0,0,tw,hi_h)), float)
    hi_mask = Image.fromarray(np.clip(hi_arr*0.55, 0, 255).astype(np.uint8))
    panel.paste(Image.new("RGB",(tw,hi_h),(255,255,255)), (tx0-pad,ty0-pad), hi_mask)


def draw_star(draw, cx, cy, r, fill, n=5):
    pts = []
    for i in range(n*2):
        angle = math.pi*i/n - math.pi/2
        radius = r if i%2==0 else r*0.42
        pts.append((cx+radius*math.cos(angle), cy+radius*math.sin(angle)))
    draw.polygon(pts, fill=fill)


def scatter_stars(draw, W, H, count=34, rng_seed=42):
    """Scatter small decorative stars around the page edges."""
    rng = np.random.default_rng(rng_seed)
    zones = []
    for _ in range(count):
        side = rng.integers(0,4)
        if side==0:   x,y = rng.integers(0,W), rng.integers(20,160)
        elif side==1: x,y = rng.integers(0,W), rng.integers(H-160,H-20)
        elif side==2: x,y = rng.integers(20,160), rng.integers(0,H)
        else:         x,y = rng.integers(W-160,W-20), rng.integers(0,H)
        r   = rng.integers(14,40)
        t   = rng.random()
        col = tuple(rainbow_color(t))
        # lighten
        col = tuple(min(255, int(c*0.7+255*0.3)) for c in col)
        draw_star(draw, int(x), int(y), r, col)


def draw_sparkle(draw, cx, cy, r, col):
    """4-point sparkle."""
    for angle in [0, 90, 45, 135]:
        a = math.radians(angle)
        draw.line([(cx-r*math.cos(a), cy-r*math.sin(a)),
                   (cx+r*math.cos(a), cy+r*math.sin(a))],
                  fill=col, width=max(2,r//5))
    # center dot
    draw.ellipse([(cx-r//4,cy-r//4),(cx+r//4,cy+r//4)], fill=col)


def scatter_sparkles(draw, W, H, count=20, rng_seed=7):
    rng = np.random.default_rng(rng_seed)
    for _ in range(count):
        x = int(rng.integers(80, W-80))
        y = int(rng.integers(80, H-80))
        r = int(rng.integers(12, 32))
        t = rng.random()
        col = tuple(min(255, int(c*0.65+255*0.35)) for c in rainbow_color(t))
        draw_sparkle(draw, x, y, r, col)


def with_bleed(trim_img):
    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(trim_img, (BLEED, BLEED))
    return canvas


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — TITLE PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def make_title_page():
    trim = soft_bg(W_TRIM, H_TRIM)
    draw = ImageDraw.Draw(trim)
    cx   = W_TRIM // 2

    # ── Rainbow stripes top & bottom ──
    stripe(draw, 0,          0, W_TRIM, h=18)
    stripe(draw, H_TRIM-18,  0, W_TRIM, h=18)

    # ── Scattered decorative stars ──
    scatter_stars(draw, W_TRIM, H_TRIM, count=40, rng_seed=11)

    # ── Top small label ──
    fn_pre = ImageFont.truetype(FSB, 52)
    text_centered(draw, cx, 40, "LUMI DOODLE PRESENTS", fn_pre, MID_GRAY,
                  outline=(255,255,255), sw=2)

    # ── Main bubble rainbow title ──
    fn_title = ImageFont.truetype(FFRED, 310)
    bubble_rainbow_text(trim, cx, 105, "TINY", fn_title, outline_size=32, anchor="mt")

    fn_title2 = ImageFont.truetype(FFRED, 230)
    bubble_rainbow_text(trim, cx, 460, "MONSTERS", fn_title2, outline_size=26, anchor="mt")

    # ── Subtitle ──
    fn_sub = ImageFont.truetype(FB, 80)
    text_centered(draw, cx, 730, "Cryptids of the USA", fn_sub, BRAND_PURPLE,
                  outline=(255,255,255), sw=3)

    # ── Rainbow divider ──
    stripe(draw, 836, 220, W_TRIM-220, h=6)

    # ── Hero banner illustration (the kawaii monster row) ──
    banner = Image.open(BANNER_IMG).convert("RGBA")
    # Scale to ~1960px wide keeping ratio
    banner = fit_width(banner, 1960)
    bx = (W_TRIM - banner.width)  // 2
    by = 870

    # Soft white rounded-rect behind banner
    pad = 24
    bg_rect = Image.new("RGB", (banner.width+pad*2, banner.height+pad*2), (252,250,248))
    trim.paste(bg_rect, (bx-pad, by-pad))
    trim.paste(banner, (bx, by), banner)

    # ── Rainbow divider below banner ──
    stripe(draw, by + banner.height + pad + 16, 220, W_TRIM-220, h=6)

    # ── 5 monster thumbnails row ──
    thumbs = ["Monster_47.png","Monster_29.png","Monster_23.png",
              "Monster_11.png","Monster_10.png"]
    rotations = [-4, 3, -2, 4, -3]
    THUMB = 270
    gap   = 36
    row_w = len(thumbs)*THUMB + (len(thumbs)-1)*gap
    tx    = (W_TRIM - row_w) // 2
    ty    = by + banner.height + pad + 50

    for i, (fname, angle) in enumerate(zip(thumbs, rotations)):
        path = os.path.join(PAGES_DIR, fname)
        if not os.path.exists(path):
            continue
        pg = Image.open(path).convert("RGB")
        pg = fit_fill(pg, THUMB, THUMB)
        pg_r = pg.rotate(angle, expand=True, fillcolor=(255,255,255))
        sh   = drop_shadow(pg_r, blur=10, offset=(6,6))
        px   = tx + i*(THUMB+gap) - (pg_r.width-THUMB)//2
        py   = ty - (pg_r.height-THUMB)//2
        trim.paste(sh, (px+4, py+4))  # shadow
        trim.paste(pg_r, (px, py))

    draw = ImageDraw.Draw(trim)

    # ── Tag line ──
    fn_tag = ImageFont.truetype(FSB, 60)
    ty_tag = ty + THUMB + 42
    text_centered(draw, cx, ty_tag,
                  "50 original kawaii coloring pages  ·  one per U.S. state",
                  fn_tag, MID_GRAY, outline=(255,255,255), sw=2)

    # ── Rainbow divider ──
    stripe(draw, ty_tag + 76, 220, W_TRIM-220, h=4)

    # ── Bottom Lumi Doodle logo + attribution ──
    logo = Image.open(LOGO_IMG).convert("RGBA")
    logo = fit_height(logo, 200)
    lx = cx - logo.width//2
    ly = H_TRIM - 270

    # Soft white ellipse behind logo
    draw.ellipse([(lx-16, ly-8), (lx+logo.width+16, ly+logo.height+8)],
                 fill=(255,255,255))
    trim.paste(logo, (lx, ly), logo)

    fn_brand = ImageFont.truetype(FXB, 50)
    text_centered(draw, cx, H_TRIM - 55, "A LUMI DOODLE COLORING BOOK",
                  fn_brand, BRAND_PURPLE, outline=(255,255,255), sw=2)

    # ── Scatter sparkles (last, on top of everything) ──
    scatter_sparkles(draw, W_TRIM, H_TRIM, count=18, rng_seed=99)

    out = with_bleed(trim)
    out.save(os.path.join(OUT_DIR, "intro_title_page.png"))
    print("✓ Title page")


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — "THIS BOOK BELONGS TO:" PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def draw_doodle_border(draw, W_T, H_T, margin=80):
    """Draw a playful dashed border made of small shapes."""
    rng = np.random.default_rng(42)
    colors_light = [
        (255,180,180), (255,210,130), (255,240,140),
        (150,220,160), (140,190,255), (210,160,255),
    ]
    step = 110
    # Top & bottom edges
    for edge_y in [margin//2, H_T - margin//2]:
        for x in range(margin, W_T-margin, step):
            ci = rng.integers(0,6)
            shape = rng.integers(0,3)
            col = colors_light[ci]
            r = int(rng.integers(18,30))
            if shape == 0:
                draw_star(draw, x, edge_y, r, col)
            elif shape == 1:
                draw.ellipse([(x-r,edge_y-r),(x+r,edge_y+r)], fill=col)
            else:
                # small heart (simplified: two circles + triangle)
                rh = r*2//3
                draw.ellipse([(x-rh,edge_y-rh),(x,edge_y)], fill=col)
                draw.ellipse([(x,edge_y-rh),(x+rh,edge_y)], fill=col)
                draw.polygon([(x-rh,edge_y-rh//2),(x+rh,edge_y-rh//2),(x,edge_y+rh)],
                             fill=col)
    # Left & right edges
    for edge_x in [margin//2, W_T - margin//2]:
        for y in range(margin, H_T-margin, step):
            ci = rng.integers(0,6)
            col = colors_light[ci]
            r = int(rng.integers(18,30))
            shape = rng.integers(0,3)
            if shape == 0:
                draw_star(draw, edge_x, y, r, col)
            elif shape == 1:
                draw.ellipse([(edge_x-r,y-r),(edge_x+r,y+r)], fill=col)
            else:
                rh = r*2//3
                draw.ellipse([(edge_x-rh,y-rh),(edge_x,y)], fill=col)
                draw.ellipse([(edge_x,y-rh),(edge_x+rh,y)], fill=col)
                draw.polygon([(edge_x-rh,y-rh//2),(edge_x+rh,y-rh//2),(edge_x,y+rh)],
                             fill=col)
    # Rounded rectangle border line
    draw.rounded_rectangle([margin, margin, W_T-margin, H_T-margin],
                           radius=60, outline=(200,190,225), width=5)


def make_belongs_page():
    trim = Image.new("RGB", (W_TRIM, H_TRIM), (254, 252, 255))
    draw = ImageDraw.Draw(trim)
    cx = W_TRIM // 2

    # ── Decorative doodle border ──
    draw_doodle_border(draw, W_TRIM, H_TRIM, margin=90)

    # ── Rainbow stripe top ──
    stripe(draw, 0, 0, W_TRIM, h=18)
    stripe(draw, H_TRIM-18, 0, W_TRIM, h=18)

    # ── Title text ──
    fn_t1 = ImageFont.truetype(FFRED, 180)
    fn_t2 = ImageFont.truetype(FFRED, 140)

    # Shadow
    draw.text((cx+6, 134), "THIS BOOK", fill=(220,210,235), font=fn_t1, anchor="mt")
    draw.text((cx+6, 330), "BELONGS TO:", fill=(220,210,235), font=fn_t2, anchor="mt")
    # Main text
    draw.text((cx, 128), "THIS BOOK", fill=BRAND_PURPLE, font=fn_t1, anchor="mt")
    draw.text((cx, 324), "BELONGS TO:", fill=BRAND_DARK,  font=fn_t2, anchor="mt")

    # ── Name line ──
    line_y = 528
    line_x1, line_x2 = 330, W_TRIM-330
    draw.line([(line_x1, line_y), (line_x2, line_y)], fill=(160,148,200), width=5)
    # Small star endpoints on the line
    draw_star(draw, line_x1-20, line_y, 16, (200,185,235))
    draw_star(draw, line_x2+20, line_y, 16, (200,185,235))

    fn_hint = ImageFont.truetype(FREG, 44)
    text_centered(draw, cx, line_y+16, "write your name here",
                  fn_hint, (200,188,222), outline=(255,255,255), sw=1)

    # ── Monster illustration — Mothman (Monster_47) ──
    monster_path = os.path.join(PAGES_DIR, "Monster_47.png")
    monster = Image.open(monster_path).convert("RGB")
    # Crop to trim size, removing bleed + bottom label area (~220px of text)
    monster = monster.crop((0, 0, 2550, 2330))
    # Scale to fit nicely in center area
    monster = fit_fill(monster, 1440, 1440)
    mx = (W_TRIM - monster.width) // 2
    my = 600
    # Paste with drop shadow effect
    sh = drop_shadow(monster, blur=20, offset=(10,10), color=(210,200,235))
    trim.paste(sh, (mx+4, my+4))
    trim.paste(monster, (mx, my))

    # ── "Vol. 1" ribbon below ──
    draw = ImageDraw.Draw(trim)
    fn_v = ImageFont.truetype(FFRED, 68)
    vy = my + monster.height + 44

    # Small rainbow stripe under monster
    stripe(draw, vy, 330, W_TRIM-330, h=5)
    vy += 26

    text_centered(draw, cx, vy,
                  "TINY MONSTERS Vol. 1  ·  Cryptids of the USA",
                  fn_v, BRAND_PURPLE, outline=(255,255,255), sw=2)

    # ── Lumi Doodle small credit ──
    fn_credit = ImageFont.truetype(FSB, 44)
    text_centered(draw, cx, H_TRIM-70, "A Lumi Doodle Coloring Book",
                  fn_credit, MID_GRAY, outline=(255,255,255), sw=1)

    out = with_bleed(trim)
    out.save(os.path.join(OUT_DIR, "intro_belongs_page.png"))
    print("✓ Belongs page")


make_title_page()
make_belongs_page()
print(f"\nDone → {OUT_DIR}/intro_*.png")
