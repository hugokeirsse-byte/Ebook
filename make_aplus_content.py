from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os

# ── Fonts ─────────────────────────────────────────────────────────────────────
FXB  = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
FB   = "/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf"
FSB  = "/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf"
FREG = "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf"

# ── Source images ─────────────────────────────────────────────────────────────
LOGO_IMG     = "/root/.claude/uploads/adbfa1c5-eebd-450f-a73d-c4c8c5acf7a6/b8607b1b-1000008640.png"
STUDIO_IMG   = "/root/.claude/uploads/adbfa1c5-eebd-450f-a73d-c4c8c5acf7a6/625f5668-1000008641.png"
GRADIENT_IMG = "/root/.claude/uploads/adbfa1c5-eebd-450f-a73d-c4c8c5acf7a6/7b5ca275-1000008642.png"
FRAME_IMG    = "/root/.claude/uploads/adbfa1c5-eebd-450f-a73d-c4c8c5acf7a6/67e191d9-1000008643.png"
BANNER_IMG   = "/root/.claude/uploads/447c523b-8610-4a2b-97da-9625e3b823f9/ab67d2b9-1000008639.png"
ICONS_IMG    = "/root/.claude/uploads/447c523b-8610-4a2b-97da-9625e3b823f9/e715fc2d-1000008638.png"
COVER_PATH   = "/root/.claude/uploads/e3aa924e-cb08-4062-b172-e0c76fa72e62/61afefb5-1000008430.png"
PAGES_DIR    = "/home/user/Ebook/pages"
OUT_DIR      = "/home/user/Ebook/aplus"
os.makedirs(OUT_DIR, exist_ok=True)

# ── Brand ─────────────────────────────────────────────────────────────────────
RAINBOW      = [(255,60,60),(255,160,0),(255,230,0),(60,200,80),(40,130,255),(160,60,255)]
BRAND_PURPLE = (90, 40, 160)
BRAND_DARK   = (28, 24, 48)
MID_GRAY     = (140, 132, 158)

def rainbow_color(t):
    n = len(RAINBOW)-1; pos = t*n; i = min(int(pos),n-1); f = pos-i
    c1,c2 = RAINBOW[i],RAINBOW[i+1]
    return tuple(round(c1[j]+(c2[j]-c1[j])*f) for j in range(3))

def stripe(draw, y, x1, x2, h=10):
    for x in range(x1,x2):
        draw.line([(x,y),(x,y+h-1)], fill=rainbow_color((x-x1)/max(x2-x1-1,1)))

def fit_fill(img, W, H):
    """Scale+center-crop image to exactly W×H."""
    iw,ih = img.size; s = max(W/iw, H/ih)
    nw,nh = round(iw*s), round(ih*s)
    img = img.resize((nw,nh), Image.LANCZOS)
    return img.crop(((nw-W)//2,(nh-H)//2,(nw-W)//2+W,(nh-H)//2+H))

def fit_height(img, H):
    """Scale image to height H, keeping ratio."""
    s = H/img.height
    return img.resize((round(img.width*s), H), Image.LANCZOS)

def fit_width(img, W):
    """Scale image to width W, keeping ratio."""
    s = W/img.width
    return img.resize((W, round(img.height*s)), Image.LANCZOS)

def drop_shadow(img, blur=14, offset=(10,10), color=(185,175,205)):
    pad = blur*2; W=img.width+abs(offset[0])+pad; H=img.height+abs(offset[1])+pad
    out = Image.new("RGB",(W,H),(255,255,255))
    out.paste(Image.new("RGB",img.size,color),(pad//2+offset[0],pad//2+offset[1]))
    out = out.filter(ImageFilter.GaussianBlur(blur))
    out.paste(img,(pad//2,pad//2)); return out

def text_outlined(draw, x, y, txt, font, fill, outline=(255,255,255), sw=3, anchor="lt"):
    for dx in range(-sw,sw+1):
        for dy in range(-sw,sw+1):
            if dx*dx+dy*dy <= sw*sw:
                draw.text((x+dx,y+dy), txt, fill=outline, font=font, anchor=anchor)
    draw.text((x,y), txt, fill=fill, font=font, anchor=anchor)

def white_panel(img, box, alpha=0.82):
    """Blend a white rectangle into img at box (x0,y0,x1,y1) with given opacity."""
    x0,y0,x1,y1 = box
    region = np.array(img.crop(box), float)
    white  = np.ones_like(region)*255
    blended = (region*(1-alpha)+white*alpha).astype(np.uint8)
    img.paste(Image.fromarray(blended), (x0,y0))


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 1 — Brand Banner  970×300
# Background: gradient stars  |  Left: logo  |  Center-right: text
# ═════════════════════════════════════════════════════════════════════════════
def make_banner():
    W,H = 970,300
    # Background: gradient image
    bg = fit_fill(Image.open(GRADIENT_IMG).convert("RGB"), W, H)
    draw = ImageDraw.Draw(bg)
    stripe(draw, 0, 0, W, h=14)
    stripe(draw, H-14, 0, W, h=14)

    # Soft white overlay in center for text readability
    white_panel(bg, (160, 30, W-30, H-30), alpha=0.55)
    draw = ImageDraw.Draw(bg)

    # Logo (circular chibi artist)
    logo = Image.open(LOGO_IMG).convert("RGBA")
    logo = fit_height(logo, 240)
    lx, ly = 18, (H-logo.height)//2
    bg.paste(logo, (lx, ly), logo)

    # Brand name
    fn_brand = ImageFont.truetype(FXB, 90)
    fn_sub   = ImageFont.truetype(FB,  32)
    fn_tag   = ImageFont.truetype(FREG,26)
    cx = lx + logo.width + 40
    text_outlined(draw, cx, 52, "LUMI DOODLE", fn_brand, BRAND_PURPLE,
                  outline=(255,255,255), sw=4, anchor="lt")
    stripe(draw, 158, cx, W-40, h=4)
    text_outlined(draw, cx, 172, "KAWAII COLORING BOOKS", fn_sub, MID_GRAY,
                  outline=(255,255,255), sw=2, anchor="lt")
    text_outlined(draw, cx, 218, "Monsters  ·  Hybrids  ·  Creatures  ·  Folklore  ·  and more",
                  fn_tag, (170,148,210), outline=(255,255,255), sw=1, anchor="lt")

    bg.save(os.path.join(OUT_DIR,"aplus_1_banner.png")); print("✓ Banner")


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 2 — Showcase  970×420
# Background: studio scene  |  Left: book cover  |  Right: white panel + text
# ═════════════════════════════════════════════════════════════════════════════
def make_showcase():
    W,H = 970,420
    bg = fit_fill(Image.open(STUDIO_IMG).convert("RGB"), W, H)

    # White panel on right half for text
    white_panel(bg, (430, 20, W-14, H-14), alpha=0.88)
    draw = ImageDraw.Draw(bg)
    stripe(draw, 0, 0, W, h=10)
    stripe(draw, H-10, 0, W, h=10)

    # Book cover, tilted, with shadow
    cover = Image.open(COVER_PATH).convert("RGB").resize((290,290), Image.LANCZOS)
    cover_r = cover.rotate(-8, expand=True, fillcolor=(255,255,255))
    sh = drop_shadow(cover_r, blur=18, offset=(14,14))
    bg.paste(sh, (30, (H-sh.height)//2+10))

    # Text block
    fn_pre  = ImageFont.truetype(FREG, 22)
    fn_t    = ImageFont.truetype(FXB,  56)
    fn_sub  = ImageFont.truetype(FB,   30)
    fn_body = ImageFont.truetype(FSB,  25)
    fn_desc = ImageFont.truetype(FREG, 24)

    tx = 450; ty = 36
    text_outlined(draw, tx, ty, "LUMI DOODLE PRESENTS", fn_pre, MID_GRAY,
                  outline=(255,255,255), sw=1, anchor="lt")
    ty += 34
    stripe(draw, ty, tx, W-24, h=3); ty += 14
    text_outlined(draw, tx, ty, "TINY MONSTERS", fn_t, BRAND_PURPLE,
                  outline=(255,255,255), sw=3, anchor="lt")
    ty += 66
    text_outlined(draw, tx, ty, "Cryptids of the USA", fn_sub, BRAND_DARK,
                  outline=(255,255,255), sw=2, anchor="lt")
    ty += 42
    stripe(draw, ty, tx, W-24, h=3); ty += 16

    points = [
        "50 original kawaii coloring pages",
        "One cryptid per U.S. state",
        "Single-sided — no bleed-through",
        "Large 8.5 × 8.5 inch format",
        "For kids, teens & adults",
    ]
    for i,pt in enumerate(points):
        col = rainbow_color(i/(len(points)-1))
        text_outlined(draw, tx,    ty, "▸", fn_body, col, outline=(255,255,255), sw=2)
        text_outlined(draw, tx+26, ty, pt,  fn_desc, BRAND_DARK, outline=(255,255,255), sw=1)
        ty += 36

    bg.save(os.path.join(OUT_DIR,"aplus_2_showcase.png")); print("✓ Showcase")


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 3 — Features  970×360
# Background: gradient stars  |  Center: icons image  |  Labels below
# ═════════════════════════════════════════════════════════════════════════════
def make_features():
    W,H = 970,360
    bg = fit_fill(Image.open(GRADIENT_IMG).convert("RGB"), W, H)
    draw = ImageDraw.Draw(bg)
    stripe(draw, 0, 0, W, h=10)
    stripe(draw, H-10, 0, W, h=10)

    # Icons image centered
    icons = Image.open(ICONS_IMG).convert("RGBA")
    icon_h = H - 110
    icons  = fit_height(icons, icon_h)
    ix = (W - icons.width)//2; iy = 10
    bg.paste(icons, (ix,iy), icons)

    # Labels beneath each of the 4 icons
    fn_t = ImageFont.truetype(FB,   26)
    fn_d = ImageFont.truetype(FREG, 21)
    labels = [
        ("Easy to Color",    "Crisp line art"),
        ("50 U.S. States",   "One per state"),
        ("Kawaii Art Style", "Cute for all ages"),
        ("For All Ages",     "Kids to adults"),
    ]
    sp = W//4; ly = iy+icon_h+6
    for i,(title,desc) in enumerate(labels):
        cx = sp//2+i*sp
        col = rainbow_color(i/(len(labels)-1))
        text_outlined(draw, cx, ly,    title, fn_t, col,      outline=(255,255,255), sw=2, anchor="mt")
        text_outlined(draw, cx, ly+32, desc,  fn_d, MID_GRAY, outline=(255,255,255), sw=1, anchor="mt")

    # Logo top-right corner
    logo = Image.open(LOGO_IMG).convert("RGBA")
    logo = fit_height(logo, 72)
    bg.paste(logo, (W-logo.width-8, 14), logo)

    bg.save(os.path.join(OUT_DIR,"aplus_3_features.png")); print("✓ Features")


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 4 — Pages Grid  970×720
# Background: kawaii frame  |  Inside: 6 coloring pages  |  Title
# ═════════════════════════════════════════════════════════════════════════════
def make_pages_grid():
    W,H = 970,720

    # Scale frame to 970×970 then center-crop to 970×720
    frame = Image.open(FRAME_IMG).convert("RGB")
    frame = frame.resize((970,970), Image.LANCZOS)
    frame = frame.crop((0,125,970,845))   # keep center 720px
    bg    = frame.copy()
    draw  = ImageDraw.Draw(bg)

    # Estimate inner content area (frame border ≈ 13% of 970 ≈ 126px each side)
    INNER_X1, INNER_X2 = 130, 840
    INNER_Y1, INNER_Y2 = 20,  640
    inner_w = INNER_X2 - INNER_X1   # 710
    inner_h = INNER_Y2 - INNER_Y1   # 620

    # Title
    fn_h = ImageFont.truetype(FXB, 38)
    text_outlined(draw, W//2, INNER_Y1+8, "INSIDE THE BOOK",
                  fn_h, BRAND_PURPLE, outline=(255,255,255), sw=3, anchor="mt")

    # 6 thumbnails — 3 cols × 2 rows inside the frame
    fn_lbl = ImageFont.truetype(FSB, 20)
    fn_st  = ImageFont.truetype(FREG,17)
    pages  = [
        ("Monster_23.png",            "Mermaid of Pascagoula","Mississippi"),
        ("Monster_29.png",            "Jersey Devil",         "New Jersey"),
        ("Monster_46_WASHINGTON.png", "Batsquatch",           "Washington"),
        ("Monster_49.png",            "Jackalope",            "Wyoming"),
        ("Monster_42.png",            "Momo",                 "Missouri"),
        ("Monster_11.png",            "Turtle Cove",          "Hawaii"),
    ]
    rotations = [-2, 2, -2, 2, -1, 1]
    cols  = 3; rows = 2
    thumb = 190
    title_h = 60
    avail_h = inner_h - title_h
    gap_x = (inner_w - cols*thumb)//(cols+1)
    gap_y = (avail_h - rows*thumb)//(rows+1)

    for idx,((fname,name,state),angle) in enumerate(zip(pages,rotations)):
        col = idx%cols; row = idx//cols
        cx = INNER_X1 + gap_x + col*(thumb+gap_x) + thumb//2
        cy = INNER_Y1 + title_h + gap_y + row*(thumb+gap_y) + thumb//2

        path = os.path.join(PAGES_DIR,fname)
        pg   = Image.open(path).convert("RGB").resize((thumb,thumb),Image.LANCZOS) \
               if os.path.exists(path) else Image.new("RGB",(thumb,thumb),(235,230,245))

        pg_r = pg.rotate(angle, expand=True, fillcolor=(255,255,255))
        sh   = drop_shadow(pg_r, blur=10, offset=(6,6), color=(180,170,200))
        bg.paste(sh, (cx-sh.width//2+3, cy-sh.height//2+3))

        draw = ImageDraw.Draw(bg)
        ly = cy + pg_r.height//2 + 12
        col_c = rainbow_color(idx/(len(pages)-1))
        text_outlined(draw, cx, ly,    name,  fn_lbl, col_c,    outline=(255,255,255), sw=2, anchor="mt")
        text_outlined(draw, cx, ly+26, state, fn_st,  MID_GRAY, outline=(255,255,255), sw=1, anchor="mt")

    bg.save(os.path.join(OUT_DIR,"aplus_4_grid.png")); print("✓ Pages grid")


make_banner()
make_showcase()
make_features()
make_pages_grid()
print(f"\nDone → {OUT_DIR}/")
print("KDP upload order: banner → showcase → features → grid")
