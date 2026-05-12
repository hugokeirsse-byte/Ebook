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

W, H     = 2400, 3300
BORDER   = 52          # outer border offset from edge
INNER    = BORDER + 16 # inner border offset
MARGIN   = BORDER + 50 # text margin from edge
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


def body_block(d, y, text, font, color=DARK, indent=0, line_gap=12):
    lh = text_h("Ag", font, d)
    for line in wrap(text, font, TW - indent, d):
        d.text((MARGIN + indent, y), line, fill=color, font=font)
        y += lh + line_gap
    return y + 10


def bullet(d, y, text, fn_body, color=DARK, line_gap=12):
    lh  = text_h("Ag", fn_body, d)
    ind = 72
    d.text((MARGIN + 14, y), "·", fill=GOLD, font=fn_body)
    for line in wrap(text, fn_body, TW - ind, d):
        d.text((MARGIN + ind, y), line, fill=color, font=fn_body)
        y += lh + line_gap
    return y + 8


def sec(d, y, label, fn_sec, gap_after=16):
    d.text((MARGIN, y), label, fill=FOREST, font=fn_sec)
    return y + text_h(label, fn_sec, d) + gap_after


def inline_pair(d, y, label, value, fn_label, fn_val, sep="  "):
    d.text((MARGIN, y), label, fill=FOREST, font=fn_label)
    lw = d.textbbox((0, 0), label + sep, font=fn_label)[2]
    d.text((MARGIN + lw, y), value, fill=DARK, font=fn_val)
    return y + text_h(label, fn_label, d) + 14


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


def paste_illustration(img, illus_path, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    try:
        il = Image.open(illus_path).convert("RGB")
        ratio = min(bw / il.width, bh / il.height)
        nw, nh = int(il.width * ratio), int(il.height * ratio)
        il = il.resize((nw, nh), Image.LANCZOS)
        ox = x0 + (bw - nw) // 2
        oy = y0 + (bh - nh) // 2
        img.paste(il, (ox, oy))
        return True
    except Exception as e:
        print(f"  ✗ illustration: {e}")
        return False


# ── Main page generator ───────────────────────────────────────────────────────

def make_botanica_page(
    day_num, date_str,
    name_fr, name_la, family, origin,
    parts_used, harvest,
    active_compounds,
    properties,
    traditional_uses,
    how_to_use,        # list of strings
    precautions,
    interactions,
    cultural_note,
    regions,
    # optional illustration paths
    illus_main=None,
    illus_detail1=None,
    illus_detail2=None,
    out_name="botanica_demo.png"
):
    img = Image.new("RGB", (W, H), CREAM)
    d   = ImageDraw.Draw(img)

    # Fonts
    fn_tiny   = ImageFont.truetype(FC_REG,  40)
    fn_day    = ImageFont.truetype(FC_REG,  52)
    fn_name   = ImageFont.truetype(FC_BOLD, 130)
    fn_latin  = ImageFont.truetype(FC_ITAL,  72)
    fn_family = ImageFont.truetype(FC_REG,   50)
    fn_sec    = ImageFont.truetype(FP_BOLD,  52)
    fn_label  = ImageFont.truetype(FP_BOLD,  48)
    fn_body   = ImageFont.truetype(FC_REG,   56)
    fn_props  = ImageFont.truetype(FC_ITAL,  54)
    fn_note   = ImageFont.truetype(FC_ITAL,  54)
    fn_tag    = ImageFont.truetype(FC_REG,   44)

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
    d.text((CX, y), f"Jour  {day_num}  ·  {date_str}",
           fill=GOLD, font=fn_day, anchor="mt")
    y += text_h("Ag", fn_day, d) + 22

    hline(d, y, color=GOLD, h=2)
    y += 24

    # ── Illustrations ─────────────────────────────────────────────────
    # Main illustration (left 2/3) + 2 detail squares (right 1/3 stacked)
    ILLUS_H    = 880
    main_x1    = MARGIN + int(TW * 0.65)
    detail_x0  = main_x1 + 20
    detail_x1  = W - MARGIN
    detail_h   = (ILLUS_H - 14) // 2

    # Main
    if illus_main and paste_illustration(img, illus_main, MARGIN, y, main_x1, y + ILLUS_H):
        d.rectangle([MARGIN, y, main_x1, y + ILLUS_H], outline=LGOLD, width=1)
    else:
        illus_placeholder(img, d, MARGIN, y, main_x1, y + ILLUS_H,
                          f"{name_la}", "Plante entière · Köhler 1887")

    # Detail 1
    if illus_detail1 and paste_illustration(img, illus_detail1, detail_x0, y, detail_x1, y + detail_h):
        d.rectangle([detail_x0, y, detail_x1, y + detail_h], outline=LGOLD, width=1)
    else:
        illus_placeholder(img, d, detail_x0, y, detail_x1, y + detail_h,
                          "Détail fleur")

    # Detail 2
    dy2 = y + detail_h + 14
    if illus_detail2 and paste_illustration(img, illus_detail2, detail_x0, dy2, detail_x1, dy2 + detail_h):
        d.rectangle([detail_x0, dy2, detail_x1, dy2 + detail_h], outline=LGOLD, width=1)
    else:
        illus_placeholder(img, d, detail_x0, dy2, detail_x1, dy2 + detail_h,
                          "Racine & graine")

    y += ILLUS_H + 30

    hline(d, y, color=GOLD, h=2)
    y += 32

    # ── Plant name ────────────────────────────────────────────────────
    d.text((CX, y), name_fr.upper(), fill=DARK, font=fn_name, anchor="mt")
    y += text_h(name_fr.upper(), fn_name, d) + 12

    d.text((CX, y), name_la, fill=GOLD, font=fn_latin, anchor="mt")
    y += text_h(name_la, fn_latin, d) + 16

    d.text((CX, y), f"{family}  ·  {origin}",
           fill=DARK, font=fn_family, anchor="mt")
    y += text_h(family, fn_family, d) + 28

    hline(d, y, color=LGOLD, h=1)
    y += 28

    # ── Quick-ref inline row ──────────────────────────────────────────
    y = inline_pair(d, y, "Parties utilisées : ", parts_used, fn_label, fn_body)
    y = inline_pair(d, y, "Récolte : ",           harvest,    fn_label, fn_body)
    y = inline_pair(d, y, "Composés actifs : ",   active_compounds, fn_label, fn_props)

    hline(d, y, color=LGOLD, h=1)
    y += 28

    # ── Propriétés ────────────────────────────────────────────────────
    y = sec(d, y, "Propriétés", fn_sec)
    y = body_block(d, y, properties, fn_props)

    # ── Usages traditionnels ──────────────────────────────────────────
    y = sec(d, y, "Usages traditionnels", fn_sec)
    y = body_block(d, y, traditional_uses, fn_body)

    # ── Comment l'utiliser ────────────────────────────────────────────
    y = sec(d, y, "Comment l'utiliser", fn_sec)
    for item in how_to_use:
        y = bullet(d, y, item, fn_body)

    # ── Précautions & Interactions ────────────────────────────────────
    y = sec(d, y, "Précautions & Interactions", fn_sec)
    y = body_block(d, y, f"{precautions}  |  Interactions : {interactions}", fn_body)

    hline(d, y, color=LGOLD, h=1)
    y += 22

    # ── Le savais-tu ──────────────────────────────────────────────────
    d.text((MARGIN, y), "Le savais-tu ?", fill=GOLD, font=fn_sec)
    y += text_h("A", fn_sec, d) + 16
    y = body_block(d, y, cultural_note, fn_note, color=DARK)

    hline(d, y, color=LGOLD, h=1)
    y += 20

    # ── Présente dans ─────────────────────────────────────────────────
    d.text((CX, y), regions, fill=GOLD, font=fn_tag, anchor="mt")

    # ── Bottom rule inside border ─────────────────────────────────────
    hline(d, H - BORDER - 44, color=GOLD, h=1)

    print(f"✓  {out_name}  (y_end={y} / {H})")
    img.save(out_name)


# ── Demo — Camomille ──────────────────────────────────────────────────────────

make_botanica_page(
    day_num   = 1,
    date_str  = "1er janvier",
    name_fr   = "Camomille",
    name_la   = "Matricaria chamomilla",
    family    = "Asteraceae",
    origin    = "Europe centrale & Asie de l'Ouest",

    parts_used       = "Fleurs séchées, feuilles, tiges",
    harvest          = "Juin – Août, par temps sec, en pleine floraison",
    active_compounds = "Azulène · α-Bisabolol · Apigénine · Matricine",

    properties = (
        "Anti-inflammatoire  ·  Antispasmodique  ·  Sédatif léger  ·  "
        "Carminatif  ·  Cicatrisant  ·  Antipyrétique"
    ),
    traditional_uses = (
        "Troubles digestifs (crampes, ballonnements, coliques, nausées), "
        "insomnies et anxiété légères, inflammations cutanées, irritations "
        "oculaires et conjonctivites. Utilisée depuis l'Antiquité comme "
        "antifièvre et relaxant nerveux."
    ),
    how_to_use = [
        "Infusion : 1 c. à café de fleurs séchées dans 250 ml d'eau bouillante, "
        "infuser 5–10 min à couvert. 2 à 3 tasses par jour, entre les repas.",
        "Huile essentielle : diluée à 2 % dans une huile végétale (jojoba, amande douce) "
        "pour massage local, douleurs articulaires ou tensions musculaires.",
        "Cataplasme : compresse imbibée d'infusion tiède appliquée sur les yeux "
        "fatigués ou irrités, 10 min.",
        "Teinture mère : 30 gouttes dans un verre d'eau, 3 fois par jour.",
    ],
    precautions   = (
        "Allergie possible chez les personnes sensibles aux Asteraceae "
        "(marguerites, séneçons, armoises). Déconseillée à forte dose "
        "pendant la grossesse."
    ),
    interactions  = (
        "Anticoagulants (warfarine), sédatifs, cyclosporine — "
        "consulter un professionnel de santé."
    ),
    cultural_note = (
        "En Égypte ancienne, la camomille était consacrée au dieu soleil Râ "
        "et utilisée pour traiter la fièvre. Les Saxons la comptaient parmi "
        "leurs neuf herbes sacrées. Au Moyen Âge, elle était plantée entre "
        "les pavés des jardins monastiques : on l'appelait la \"plante du marcheur\" "
        "car elle résistait à tous les piétinements."
    ),
    regions = (
        "Europe  ·  Asie  ·  Afrique du Nord  ·  "
        "Amérique du Nord (naturalisée)  ·  Australie (naturalisée)"
    ),
    out_name = "/home/user/Ebook/botanica_demo.png",
)
