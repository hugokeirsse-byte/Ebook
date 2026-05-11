"""
New A+ module: Book Specs Diagram  970×400
Illustrated open book showing dimensions, single-sided layout & key features.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math, os

FXB   = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
FB    = "/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf"
FSB   = "/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf"
FREG  = "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf"
FFRED = "/home/user/Ebook/fonts/FredokaOne-Regular.ttf"

PAGES_DIR = "/home/user/Ebook/pages"
LOGO_IMG  = "/root/.claude/uploads/adbfa1c5-eebd-450f-a73d-c4c8c5acf7a6/b8607b1b-1000008640.png"
OUT_DIR   = "/home/user/Ebook/aplus"

RAINBOW      = [(255,60,60),(255,160,0),(255,230,0),(60,200,80),(40,130,255),(160,60,255)]
BRAND_PURPLE = (90, 40, 160)
BRAND_DARK   = (28, 24, 48)
MID_GRAY     = (140, 132, 158)
PAGE_PURPLE  = (230, 222, 248)
SPINE_COLOR  = (150, 120, 200)
SHADOW_COLOR = (195, 185, 220)


def rainbow_color(t):
    n = len(RAINBOW)-1; pos = t*n; i = min(int(pos),n-1); f = pos-i
    c1,c2 = RAINBOW[i],RAINBOW[i+1]
    return tuple(round(c1[j]+(c2[j]-c1[j])*f) for j in range(3))

def stripe(draw, y, x1, x2, h=10):
    for x in range(x1, x2):
        draw.line([(x,y),(x,y+h-1)], fill=rainbow_color((x-x1)/max(x2-x1-1,1)))

def fit_fill(img, W, H):
    iw,ih = img.size; s = max(W/iw, H/ih)
    nw,nh = round(iw*s),round(ih*s)
    img = img.resize((nw,nh),Image.LANCZOS)
    return img.crop(((nw-W)//2,(nh-H)//2,(nw-W)//2+W,(nh-H)//2+H))

def fit_height(img, H):
    s = H/img.height
    return img.resize((round(img.width*s), H), Image.LANCZOS)

def text_c(draw, cx, y, txt, font, fill, outline=(255,255,255), sw=2, anchor="mt"):
    for dx in range(-sw, sw+1):
        for dy in range(-sw, sw+1):
            if dx*dx+dy*dy <= sw*sw:
                draw.text((cx+dx,y+dy), txt, fill=outline, font=font, anchor=anchor)
    draw.text((cx, y), txt, fill=fill, font=font, anchor=anchor)

def draw_arrow(draw, x1, y1, x2, y2, col, width=3, head=10):
    """Draw an arrow from (x1,y1) to (x2,y2)."""
    draw.line([(x1,y1),(x2,y2)], fill=col, width=width)
    angle = math.atan2(y2-y1, x2-x1)
    for side in [-1, 1]:
        ax = x2 - head*math.cos(angle) + side*head*0.45*math.sin(angle)
        ay = y2 - head*math.sin(angle) - side*head*0.45*math.cos(angle)
        draw.line([(ax,ay),(x2,y2)], fill=col, width=width)

def draw_double_arrow(draw, x1, y, x2, col=(120,100,160), width=3, head=10):
    """Horizontal double-headed arrow."""
    draw.line([(x1,y),(x2,y)], fill=col, width=width)
    draw_arrow(draw, x2-head, y, x2, y, col, width, head)
    draw_arrow(draw, x1+head, y, x1, y, col, width, head)

def draw_double_arrow_v(draw, x, y1, y2, col=(120,100,160), width=3, head=10):
    """Vertical double-headed arrow."""
    draw.line([(x,y1),(x,y2)], fill=col, width=width)
    draw_arrow(draw, x, y2-head, x, y2, col, width, head)
    draw_arrow(draw, x, y1+head, x, y1, col, width, head)


def make_book_specs():
    W, H = 970, 400

    # ── Background: soft pastel gradient ──
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    for y in range(H):
        t = y / (H-1)
        top = np.array([242, 238, 255])
        bot = np.array([255, 248, 240])
        arr[y, :] = (top*(1-t) + bot*t).astype(np.uint8)
    bg = Image.fromarray(arr)
    draw = ImageDraw.Draw(bg)

    # ── Rainbow stripes ──
    stripe(draw, 0, 0, W, h=10)
    stripe(draw, H-10, 0, W, h=10)

    # ════════════════════════════════════════════════════
    # BOOK DIAGRAM — centered at (cx_book, cy_book)
    # Open book: left page (content) + spine + right page (blank)
    # Slight 3-D: left page rises to left, right page rises to right
    # ════════════════════════════════════════════════════
    PAGE_W = 185   # width of each book page (open book = 2×PAGE_W + spine)
    PAGE_H = 230   # height of each page
    SPINE  = 14    # spine width
    PERSP  = 18    # vertical offset for perspective tilt at outer edges
    CORNER = 12    # border radius (approximated with line)

    cx_book = 400       # shifted left to give more room for features
    cy_book = H // 2 + 12

    # Page polygon points (trapezoidal perspective)
    # Left page: top-left slightly higher (outer), top-right flush (spine)
    lx0 = cx_book - SPINE//2 - PAGE_W
    lx1 = cx_book - SPINE//2
    ly_outer_top = cy_book - PAGE_H//2 + PERSP
    ly_outer_bot = cy_book + PAGE_H//2 - PERSP
    ly_spine_top = cy_book - PAGE_H//2
    ly_spine_bot = cy_book + PAGE_H//2

    left_page_pts = [
        (lx0, ly_outer_top),
        (lx1, ly_spine_top),
        (lx1, ly_spine_bot),
        (lx0, ly_outer_bot),
    ]

    # Right page: mirror
    rx0 = cx_book + SPINE//2
    rx1 = cx_book + SPINE//2 + PAGE_W
    right_page_pts = [
        (rx0, ly_spine_top),
        (rx1, ly_outer_top),
        (rx1, ly_outer_bot),
        (rx0, ly_spine_bot),
    ]

    # Drop shadow
    def shift_pts(pts, dx, dy):
        return [(x+dx,y+dy) for x,y in pts]

    draw.polygon(shift_pts(left_page_pts + right_page_pts[::-1], 8, 8),
                 fill=SHADOW_COLOR)

    # Left page fill
    draw.polygon(left_page_pts, fill=(255,255,255), outline=(160,145,200), width=3)

    # Right page fill (very light blue-gray = blank back)
    draw.polygon(right_page_pts, fill=(245,245,252), outline=(160,145,200), width=3)

    # Spine rectangle
    draw.rectangle([cx_book-SPINE//2, ly_spine_top, cx_book+SPINE//2, ly_spine_bot],
                   fill=SPINE_COLOR)
    # Small highlight on spine
    draw.rectangle([cx_book-SPINE//2+2, ly_spine_top+4,
                    cx_book-SPINE//2+5, ly_spine_bot-4],
                   fill=(180, 158, 225))

    # ── Paste sample coloring page thumbnail on left page ──
    THUMB = PAGE_W - 24  # fit inside the page with padding
    pg = Image.open(os.path.join(PAGES_DIR, "Monster_23.png")).convert("RGB")
    pg = pg.crop((0, 0, 2550, 2330))  # remove bottom text label
    pg = fit_fill(pg, THUMB, THUMB)

    # Compute paste position: left page center
    lpage_cx = (lx0 + lx1) // 2
    lpage_cy = cy_book
    # Account for perspective: left page center y shifts by PERSP/2
    thumb_x = lpage_cx - THUMB//2
    thumb_y = lpage_cy - THUMB//2

    bg.paste(pg, (thumb_x, thumb_y))

    # Thin border around thumbnail
    draw = ImageDraw.Draw(bg)
    draw.rectangle([thumb_x-1, thumb_y-1, thumb_x+THUMB+1, thumb_y+THUMB+1],
                   outline=(200,190,225), width=2)

    # ── "SINGLE-SIDED" label on left page (below thumbnail) ──
    fn_sm   = ImageFont.truetype(FSB,  18)
    fn_tiny = ImageFont.truetype(FREG, 15)
    draw.text((lpage_cx, thumb_y+THUMB+6), "CONTENT SIDE",
              fill=(120,100,160), font=fn_sm, anchor="mt")

    # ── "BLANK" label on right page ──
    rpage_cx = (rx0 + rx1) // 2

    # Dashed lines to suggest blank page
    for line_y in range(cy_book-60, cy_book+60, 24):
        draw.line([(rx0+16, line_y), (rx1-16, line_y)],
                  fill=(210,205,230), width=2)

    fn_blank = ImageFont.truetype(FSB, 19)
    draw.text((rpage_cx, cy_book-14), "BLANK BACK",
              fill=(150,140,185), font=fn_blank, anchor="mt")
    fn_no = ImageFont.truetype(FREG, 14)
    draw.text((rpage_cx, cy_book+12), "No bleed-through",
              fill=(170,160,200), font=fn_no, anchor="mt")

    # ════════════════════════════════════════════════════
    # DIMENSION ANNOTATIONS
    # ════════════════════════════════════════════════════
    ARROW_COL  = (100, 80, 155)
    TICK_LEN   = 10

    fn_dim  = ImageFont.truetype(FB,   22)
    fn_diml = ImageFont.truetype(FREG, 17)

    # Horizontal arrow — full open book width
    book_left   = lx0 - 6
    book_right  = rx1 + 6
    arr_y_top   = ly_outer_top - 30

    draw.line([(book_left, arr_y_top-TICK_LEN//2),
               (book_left, arr_y_top+TICK_LEN//2)],
              fill=ARROW_COL, width=2)
    draw.line([(book_right, arr_y_top-TICK_LEN//2),
               (book_right, arr_y_top+TICK_LEN//2)],
              fill=ARROW_COL, width=2)
    draw_double_arrow(draw, book_left, arr_y_top, book_right,
                      col=ARROW_COL, width=2, head=8)
    mid_x = (book_left+book_right)//2
    # White pill behind text
    tw_half = 52
    draw.rounded_rectangle([mid_x-tw_half, arr_y_top-13, mid_x+tw_half, arr_y_top+2],
                            radius=8, fill=(255,255,255))
    draw.text((mid_x, arr_y_top-12), "8.5 inches",
              fill=ARROW_COL, font=fn_dim, anchor="mt")

    # Vertical arrow — left page height only (one page = 8.5 in too)
    arr_x_left = lx0 - 36
    page_top   = ly_outer_top
    page_bot   = ly_outer_bot
    draw.line([(arr_x_left-TICK_LEN//2, page_top),
               (arr_x_left+TICK_LEN//2, page_top)], fill=ARROW_COL, width=2)
    draw.line([(arr_x_left-TICK_LEN//2, page_bot),
               (arr_x_left+TICK_LEN//2, page_bot)], fill=ARROW_COL, width=2)
    draw_double_arrow_v(draw, arr_x_left, page_top, page_bot,
                        col=ARROW_COL, width=2, head=8)
    mid_y = (page_top+page_bot)//2
    tw_half_v = 52
    draw.rounded_rectangle([arr_x_left-12, mid_y-tw_half_v,
                             arr_x_left+14, mid_y+tw_half_v],
                            radius=8, fill=(255,255,255))
    # Vertical text
    from PIL import Image as PILImage
    vtxt_img = PILImage.new("RGBA", (120, 30), (0,0,0,0))
    vtxt_draw = ImageDraw.Draw(vtxt_img)
    vtxt_draw.text((60, 0), "8.5 inches", fill=ARROW_COL, font=fn_dim, anchor="mt")
    vtxt_rot = vtxt_img.rotate(90, expand=True)
    bg.paste(vtxt_rot, (arr_x_left-vtxt_rot.width//2, mid_y-vtxt_rot.height//2), vtxt_rot)

    # ════════════════════════════════════════════════════
    # RIGHT SIDE: Feature callout list
    # ════════════════════════════════════════════════════
    feat_x = rx1 + 46
    feat_y = ly_outer_top - 8

    fn_ft = ImageFont.truetype(FB,   22)
    fn_fd = ImageFont.truetype(FREG, 17)

    features = [
        ("Single-Sided Pages",    "Color without bleed-through",  (255, 80, 80)),
        ("50 Original Pages",     "One U.S. cryptid per state",   (255, 180, 0)),
        ("8.5 × 8.5 Inch Format", "Generous coloring space",      (80, 190, 80)),
        ("For All Ages",          "Kids, teens & adults",         (60, 140, 255)),
        ("Kawaii Art Style",      "Cute thick-outline art",       (160, 60, 255)),
    ]

    for title, desc, col in features:
        # Colored bullet dot
        draw.ellipse([(feat_x, feat_y+4),
                      (feat_x+14, feat_y+18)], fill=col)
        draw.text((feat_x+22, feat_y), title,
                  fill=BRAND_DARK, font=fn_ft, anchor="lt")
        feat_y += 26
        draw.text((feat_x+22, feat_y), desc,
                  fill=MID_GRAY, font=fn_fd, anchor="lt")
        feat_y += 34

    # ════════════════════════════════════════════════════
    # LEFT SIDE: module title
    # ════════════════════════════════════════════════════
    # Left side: rotated "BOOK SPECS" label
    title_cx = max(0, (0 + (lx0-48)) // 2)
    if title_cx > 14:
        fn_mod  = ImageFont.truetype(FFRED, 30)
        fn_sub2 = ImageFont.truetype(FSB,   17)
        label_h = H - 30
        label_w = 46
        lbl = Image.new("RGBA", (label_h, label_w), (0,0,0,0))
        ld  = ImageDraw.Draw(lbl)
        ld.text((label_h//2, 4), "BOOK SPECS",
                fill=BRAND_PURPLE, font=fn_mod, anchor="mt")
        lbl_rot = lbl.rotate(90, expand=True)  # rotate CCW → vertical
        bg.paste(lbl_rot, (title_cx - lbl_rot.width//2, (H-lbl_rot.height)//2), lbl_rot)

    out_path = os.path.join(OUT_DIR, "aplus_5_specs.png")
    bg.save(out_path)
    print(f"✓ Book specs diagram → {out_path}")


make_book_specs()
