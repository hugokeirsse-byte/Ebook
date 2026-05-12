"""Generate a Botanica page — Medicinal Plants series.
Layout: decorative border, multi-illustration area, rich text content.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

CREAM      = (252, 249, 242)
DARK       = (38,  32,  24)
GOLD       = (168, 138, 82)
LGOLD      = (210, 185, 130)
FOREST     = (45,  80,  22)
PALE_GREEN = (232, 241, 224)
PALE_GOLD  = (245, 238, 220)

FC_REG  = "/home/user/Ebook/fonts/CormorantGaramond-Regular.ttf"
FC_BOLD = "/home/user/Ebook/fonts/CormorantGaramond-Bold.ttf"
FC_ITAL = "/home/user/Ebook/fonts/CormorantGaramond-Italic.ttf"
FP_BOLD = "/home/user/Ebook/fonts/PlayfairDisplay-Bold.ttf"
FP_ITAL = "/home/user/Ebook/fonts/PlayfairDisplay-Italic.ttf"

W, H     = 2400, 2400
BORDER   = 52
INNER    = BORDER + 16
MARGIN   = BORDER + 50
CX       = W // 2
TW       = W - 2 * MARGIN


# ── Drawing helpers ───────────────────────────────────────────────────────────

def wrap(text, font, max_w, draw):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        if draw.textbbox((0, 0), test, font=font)[2] > max_w and cur:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines


def text_h(text, font, d):
    bb = d.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]


def hline(d, y, x0=None, x1=None, color=GOLD, h=2):
    if x0 is None: x0 = MARGIN
    if x1 is None: x1 = W - MARGIN
    d.rectangle([x0, y, x1, y + h], fill=color)
    return y + h + 1


def body_block(d, y, text, font, color=DARK, indent=0, line_gap=8):
    lh = text_h("Ag", font, d)
    for line in wrap(text, font, TW - indent, d):
        d.text((MARGIN + indent, y), line, fill=color, font=font)
        y += lh + line_gap
    return y + 8


def bullet(d, y, text, fn_body, color=DARK, line_gap=8):
    lh  = text_h("Ag", fn_body, d)
    ind = 64
    d.text((MARGIN + 14, y), "·", fill=GOLD, font=fn_body)
    for line in wrap(text, fn_body, TW - ind, d):
        d.text((MARGIN + ind, y), line, fill=color, font=fn_body)
        y += lh + line_gap
    return y + 8


def sec(d, y, label, fn_sec, gap_after=10):
    d.text((MARGIN, y), label, fill=FOREST, font=fn_sec)
    return y + text_h(label, fn_sec, d) + gap_after


def inline_pair(d, y, label, value, fn_label, fn_val, sep="  "):
    d.text((MARGIN, y), label, fill=FOREST, font=fn_label)
    lw = d.textbbox((0, 0), label + sep, font=fn_label)[2]
    d.text((MARGIN + lw, y), value, fill=DARK, font=fn_val)
    return y + text_h(label, fn_label, d) + 10


# ── Decorative border (matches cover aesthetic) ───────────────────────────────

def draw_border(img, d):
    b, i = BORDER, INNER
    # Outer thick line
    d.rectangle([b,   b,   W-b,   H-b  ], outline=GOLD,  width=3)
    # Inner thin line
    d.rectangle([i,   i,   W-i,   H-i  ], outline=LGOLD, width=1)

    # Corner diamond ornaments
    def diamond(cx, cy, r=16):
        pts = [(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)]
        d.polygon(pts, fill=GOLD)

    for px, py in [(b, b), (W-b, b), (b, H-b), (W-b, H-b)]:
        diamond(px, py)

    # Small tick marks along top & bottom borders (every 120px)
    for x in range(b + 120, W - b, 120):
        d.rectangle([x-1, b-6,   x+1, b+6  ], fill=LGOLD)
        d.rectangle([x-1, H-b-6, x+1, H-b+6], fill=LGOLD)
    # Along left & right
    for y in range(b + 120, H - b, 120):
        d.rectangle([b-6,   y-1, b+6,   y+1], fill=LGOLD)
        d.rectangle([W-b-6, y-1, W-b+6, y+1], fill=LGOLD)


# ── Illustration placeholder (elegant framed box) ────────────────────────────

def illus_placeholder(img, d, x0, y0, x1, y1, label="Illustration · Köhler 1887",
                      sublabel=None):
    bw, bh = x1 - x0, y1 - y0
    bg = Image.new("RGB", (bw, bh), PALE_GREEN)
    img.paste(bg, (x0, y0))
    d.rectangle([x0,    y0,    x1,    y1   ], outline=FOREST, width=2)
    d.rectangle([x0+8,  y0+8,  x1-8,  y1-8 ], outline=LGOLD,  width=1)
    fn = ImageFont.truetype(FC_ITAL, 44)
    fn2 = ImageFont.truetype(FC_REG, 36)
    mid = y0 + bh // 2
    d.text(((x0+x1)//2, mid - (20 if sublabel else 0)),
           label, fill=FOREST, font=fn, anchor="mm")
    if sublabel:
        d.text(((x0+x1)//2, mid + 34), sublabel, fill=LGOLD, font=fn2, anchor="mm")


def sample_bg_color(src_img):
    """Average the edge pixels to get the illustration's background colour."""
    w, h = src_img.size
    pts  = [(5,5),(w-5,5),(5,h-5),(w-5,h-5),
            (w//4,5),(w//2,5),(3*w//4,5),
            (w//4,h-5),(w//2,h-5),(3*w//4,h-5)]
    pixels = [src_img.getpixel(p) for p in pts]
    return tuple(sum(c[i] for c in pixels)//len(pixels) for i in range(3))


def place_crop(page_img, src_img, bg_col, fracs, dst_box):
    """
    Crop src_img at fractional coordinates (fx0,fy0,fx1,fy1),
    fill dst_box on page_img with bg_col so the cut is invisible,
    then paste the cropped region centred inside.
    """
    bx0, by0, bx1, by1 = dst_box
    bw, bh = bx1 - bx0, by1 - by0

    # Fill box with source background → seamless cutout
    page_img.paste(Image.new("RGB", (bw, bh), bg_col), (bx0, by0))

    sw, sh = src_img.size
    crop = src_img.crop((int(fracs[0]*sw), int(fracs[1]*sh),
                         int(fracs[2]*sw), int(fracs[3]*sh)))
    cw, ch = crop.size
    ratio  = min(bw/cw, bh/ch) * 0.96   # tiny padding
    nw, nh = int(cw*ratio), int(ch*ratio)
    crop   = crop.resize((nw, nh), Image.LANCZOS)
    page_img.paste(crop, (bx0 + (bw-nw)//2, by0 + (bh-nh)//2))

    # Thin gold border on top
    ImageDraw.Draw(page_img).rectangle([bx0, by0, bx1, by1],
                                        outline=LGOLD, width=1)


# ── Main page generator ───────────────────────────────────────────────────────

def make_botanica_page(
    day_num, date_str,
    name_fr, name_la, family, origin,
    parts_used, harvest, habitat,
    active_compounds,
    properties,
    traditional_uses,
    how_to_use,
    precautions,
    interactions,
    cultural_note,
    regions,
    illus_main=None,
    out_name="botanica_demo.png"
):
    img = Image.new("RGB", (W, H), CREAM)
    d   = ImageDraw.Draw(img)

    # Fonts — tuned for 2400×2400 square
    fn_tiny   = ImageFont.truetype(FC_REG,  34)
    fn_day    = ImageFont.truetype(FC_REG,  44)
    fn_sec    = ImageFont.truetype(FP_BOLD, 42)
    fn_label  = ImageFont.truetype(FP_BOLD, 40)
    fn_body   = ImageFont.truetype(FC_REG,  44)
    fn_props  = ImageFont.truetype(FC_ITAL, 43)
    fn_note   = ImageFont.truetype(FC_ITAL, 43)
    fn_tag    = ImageFont.truetype(FC_REG,  38)

    # ── Border ────────────────────────────────────────────────────────
    draw_border(img, d)

    y = BORDER + 38

    # ── Publisher micro-line ──────────────────────────────────────────
    d.text((CX, y), "MIRABILIA  ÉDITIONS  ·  THE BOTANICA COLLECTION",
           fill=LGOLD, font=fn_tiny, anchor="mt")
    y += text_h("M", fn_tiny, d) + 14

    hline(d, y, color=LGOLD, h=1)
    y += 18

    # ── Day + date ────────────────────────────────────────────────────
    d.text((CX, y), f"Day  {day_num}  ·  {date_str}",
           fill=GOLD, font=fn_day, anchor="mt")
    y += text_h("Ag", fn_day, d) + 22

    hline(d, y, color=GOLD, h=2)
    y += 24

    # ── Two-column section: image LEFT | name + legend RIGHT ─────────
    COL_H   = 820
    LEFT_W  = 1000
    GAP_COL = 28
    RIGHT_X = MARGIN + LEFT_W + GAP_COL
    RIGHT_W = W - MARGIN - RIGHT_X

    # Vertical separator
    sep_x = MARGIN + LEFT_W + GAP_COL // 2
    d.rectangle([sep_x, y, sep_x+1, y+COL_H], fill=LGOLD)

    # Left — full illustration, fit to column, cream background
    col_top = y
    if illus_main and os.path.exists(illus_main):
        try:
            raw    = Image.open(illus_main).convert("RGB")
            bg_col = sample_bg_color(raw)
            # Fill column with image background
            img.paste(Image.new("RGB", (LEFT_W, COL_H), bg_col), (MARGIN, y))
            # Scale to fit column
            ratio = min(LEFT_W / raw.width, COL_H / raw.height)
            nw    = int(raw.width  * ratio)
            nh    = int(raw.height * ratio)
            sized = raw.resize((nw, nh), Image.LANCZOS)
            ox    = MARGIN + (LEFT_W - nw) // 2
            oy    = y       + (COL_H - nh) // 2
            img.paste(sized, (ox, oy))
            d.rectangle([MARGIN, y, MARGIN+LEFT_W, y+COL_H], outline=LGOLD, width=1)
        except Exception as e:
            print(f"  ✗ illustration: {e}")
            illus_placeholder(img, d, MARGIN, y, MARGIN+LEFT_W, y+COL_H, name_la)
    else:
        illus_placeholder(img, d, MARGIN, y, MARGIN+LEFT_W, y+COL_H, name_la)

    # Right — plant name + legend
    fn_rname  = ImageFont.truetype(FC_BOLD, 82)
    fn_rlatin = ImageFont.truetype(FC_ITAL, 52)
    fn_rfam   = ImageFont.truetype(FC_REG,  42)
    fn_lhdr   = ImageFont.truetype(FP_BOLD, 42)
    fn_litem  = ImageFont.truetype(FC_REG,  42)
    fn_lsrc   = ImageFont.truetype(FC_ITAL, 36)

    ry = y + 22

    # Plant name
    d.text((RIGHT_X, ry), name_fr.upper(), fill=DARK, font=fn_rname)
    ry += text_h(name_fr.upper(), fn_rname, d) + 8

    # Latin
    d.text((RIGHT_X, ry), name_la, fill=GOLD, font=fn_rlatin)
    ry += text_h(name_la, fn_rlatin, d) + 8

    # Family · origin (wrapped)
    for line in wrap(f"{family}  ·  {origin}", fn_rfam, RIGHT_W, d):
        d.text((RIGHT_X, ry), line, fill=DARK, font=fn_rfam)
        ry += text_h(line, fn_rfam, d) + 5

    # Habitat
    ry += 6
    d.text((RIGHT_X, ry), "Habitat :", fill=FOREST, font=fn_rfam)
    hw = d.textbbox((0,0), "Habitat :  ", font=fn_rfam)[2]
    d.text((RIGHT_X + hw, ry), habitat, fill=DARK, font=fn_rfam)
    ry += text_h("A", fn_rfam, d) + 16

    # Rule
    d.rectangle([RIGHT_X, ry, W-MARGIN, ry+1], fill=LGOLD)
    ry += 20

    # Legend header
    d.text((RIGHT_X, ry), "Figure Legend", fill=FOREST, font=fn_lhdr)
    ry += text_h("A", fn_lhdr, d) + 18

    # Legend items — airy spacing
    legend_items = [
        ("1.",     "Flowering plant"),
        ("2.",     "Flower head cross-section"),
        ("3.",     "Ray floret (petal)"),
        ("4.",     "Disc floret"),
        ("5.",     "Flower bud"),
        ("6.",     "Disc floret — magnified"),
        ("7.",     "Ray floret — magnified"),
        ("8.",     "Achene"),
        ("9.",     "Achene cross-section"),
        ("10–11.", "Seeds"),
        ("12–13.", "Seed cross-sections"),
        ("19.",    "Leaf & stem detail"),
    ]
    num_w = d.textbbox((0,0), "10–11.  ", font=fn_litem)[2]
    li_h  = text_h("A", fn_litem, d) + 16   # airy gap
    for num, desc in legend_items:
        if ry + li_h > col_top + COL_H - 52:
            break
        d.text((RIGHT_X,         ry), num,  fill=GOLD, font=fn_litem)
        d.text((RIGHT_X + num_w, ry), desc, fill=DARK, font=fn_litem)
        ry += li_h

    # Source pinned to bottom of right column
    src_y = col_top + COL_H - 42
    d.rectangle([RIGHT_X, src_y - 12, W-MARGIN, src_y - 11], fill=LGOLD)
    d.text((RIGHT_X, src_y),
           "Köhler's Medizinal-Pflanzen, 1887  ·  Public domain",
           fill=LGOLD, font=fn_lsrc)

    y = col_top + COL_H + 28

    hline(d, y, color=GOLD, h=2)
    y += 30

    # ── Quick-ref row ─────────────────────────────────────────────────
    y = inline_pair(d, y, "Parts used: ",       parts_used,       fn_label, fn_body)
    y = inline_pair(d, y, "Harvest: ",          harvest,          fn_label, fn_body)
    y = inline_pair(d, y, "Active compounds: ", active_compounds, fn_label, fn_props)

    hline(d, y, color=LGOLD, h=1)
    y += 28

    # ── Propriétés ────────────────────────────────────────────────────
    y = sec(d, y, "Properties", fn_sec)
    y = body_block(d, y, properties, fn_props)

    # ── Traditional uses ──────────────────────────────────────────────
    y = sec(d, y, "Traditional Uses", fn_sec)
    y = body_block(d, y, traditional_uses, fn_body)

    # ── How to use ────────────────────────────────────────────────────
    y = sec(d, y, "How to Use", fn_sec)
    for item in how_to_use:
        y = bullet(d, y, item, fn_body)

    # ── Precautions & Interactions ────────────────────────────────────
    y = sec(d, y, "Precautions & Drug Interactions", fn_sec)
    y = body_block(d, y, f"{precautions}  |  Interactions: {interactions}", fn_body)

    hline(d, y, color=LGOLD, h=1)
    y += 22

    # ── Did you know ──────────────────────────────────────────────────
    d.text((MARGIN, y), "Did you know?", fill=GOLD, font=fn_sec)
    y += text_h("A", fn_sec, d) + 16
    y = body_block(d, y, cultural_note, fn_note, color=DARK)

    hline(d, y, color=LGOLD, h=1)
    y += 20

    # ── Found in ──────────────────────────────────────────────────────
    d.text((CX, y), regions, fill=GOLD, font=fn_tag, anchor="mt")

    # ── Bottom rule inside border ─────────────────────────────────────
    hline(d, H - BORDER - 44, color=GOLD, h=1)

    print(f"✓  {out_name}  (y_end={y} / {H})")
    img.save(out_name)


# ── Demo — Chamomile ──────────────────────────────────────────────────────────

make_botanica_page(
    day_num   = 1,
    date_str  = "January 1st",
    name_fr   = "Chamomile",
    name_la   = "Matricaria chamomilla",
    family    = "Asteraceae",
    origin    = "Central Europe & Western Asia",

    parts_used       = "Dried flowers, leaves, stems",
    harvest          = "June – August, in dry weather, at peak bloom",
    habitat          = "Meadows, roadsides, cultivated fields, disturbed soils",
    active_compounds = "Chamazulene · α-Bisabolol · Apigenin · Matricine",

    properties = (
        "Anti-inflammatory  ·  Antispasmodic  ·  Mild sedative  ·  "
        "Carminative  ·  Cicatrizant  ·  Antipyretic"
    ),
    traditional_uses = (
        "Digestive complaints (cramps, bloating, colic, nausea), mild insomnia "
        "and anxiety, skin inflammation, eye irritations and conjunctivitis. "
        "Used since Antiquity as a fever remedy and nervous system relaxant "
        "across European and Middle Eastern traditions."
    ),
    how_to_use = [
        "Infusion: 1 tsp dried flowers in 250 ml boiling water, steep 5–10 min "
        "covered. 2 to 3 cups daily, between meals.",
        "Essential oil: diluted to 2% in a carrier oil (jojoba, sweet almond) "
        "for local massage on joint pain or muscle tension.",
        "Compress: a warm chamomile-soaked cloth applied to tired or irritated "
        "eyes for 10 minutes.",
        "Tincture: 30 drops in a glass of water, three times a day.",
    ],
    precautions   = (
        "Possible allergy in people sensitive to Asteraceae (daisies, ragweed, "
        "mugwort). Not recommended in high doses during pregnancy."
    ),
    interactions  = (
        "Anticoagulants (warfarin), sedatives, cyclosporine — "
        "consult a healthcare professional."
    ),
    cultural_note = (
        "In ancient Egypt, chamomile was dedicated to the sun god Ra and used "
        "to treat fever. The Anglo-Saxons counted it among their nine sacred herbs, "
        "believed to repel poison and disease. In medieval monastery gardens, it was "
        "planted between paving stones and called the \"plant of the walker\" — "
        "the more it was trodden upon, the more it thrived."
    ),
    regions = (
        "Europe  ·  Asia  ·  North Africa  ·  "
        "North America (naturalized)  ·  Australia (naturalized)"
    ),
    illus_main = "/home/user/Ebook/kohler_main.jpg",
    out_name   = "/home/user/Ebook/botanica_demo.png",
)
