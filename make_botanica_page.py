"""Generate a sample Botanica page — Medicinal Plants series."""
from PIL import Image, ImageDraw, ImageFont
import os, math

CREAM       = (252, 249, 242)
DARK        = (38,  32,  24)
GOLD        = (168, 138, 82)
LGOLD       = (210, 185, 130)
FOREST      = (45,  80,  22)
PALE_GREEN  = (220, 235, 210)

FC_REG  = "/home/user/Ebook/fonts/CormorantGaramond-Regular.ttf"
FC_BOLD = "/home/user/Ebook/fonts/CormorantGaramond-Bold.ttf"
FC_ITAL = "/home/user/Ebook/fonts/CormorantGaramond-Italic.ttf"
FP_BOLD = "/home/user/Ebook/fonts/PlayfairDisplay-Bold.ttf"
FP_ITAL = "/home/user/Ebook/fonts/PlayfairDisplay-Italic.ttf"

W, H   = 2400, 3300   # 8 × 11" at 300 DPI
MARGIN = 150
CX     = W // 2
TW     = W - 2 * MARGIN   # usable text width


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


def rule(d, y, x0=MARGIN, x1=W - MARGIN, color=GOLD, h=2):
    d.rectangle([x0, y, x1, y + h], fill=color)
    return y + h


def section_header(d, y, text, font, color=FOREST):
    d.text((MARGIN, y), text, fill=color, font=font)
    bbox = d.textbbox((0, 0), text, font=font)
    return y + (bbox[3] - bbox[1]) + 18


def body_block(d, y, text, font, color=DARK, indent=0):
    for line in wrap(text, font, TW - indent, d):
        d.text((MARGIN + indent, y), line, fill=color, font=font)
        bbox = d.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + 10
    return y + 14


def bullet_item(d, y, text, fn_bullet, fn_body, gap=70):
    d.text((MARGIN + 20, y), "·", fill=GOLD, font=fn_bullet)
    return body_block(d, y, text, fn_body, indent=gap)


def draw_illustration_placeholder(img, d, y, illus_h=920):
    """Elegant framed placeholder for the Köhler illustration."""
    x0, x1 = MARGIN, W - MARGIN
    y1 = y + illus_h

    # Soft background tint
    bg = Image.new("RGB", (x1 - x0, illus_h), PALE_GREEN)
    img.paste(bg, (x0, y))

    # Border — double line
    d.rectangle([x0, y, x1, y1], outline=FOREST, width=3)
    d.rectangle([x0 + 10, y + 10, x1 - 10, y1 - 10], outline=LGOLD, width=1)

    # Corner ornaments
    cs = 28
    for cx_, cy_ in [(x0, y), (x1, y), (x0, y1), (x1, y1)]:
        d.rectangle([cx_ - cs // 2, cy_ - cs // 2, cx_ + cs // 2, cy_ + cs // 2],
                    fill=CREAM, outline=FOREST, width=2)

    # Centre label
    fn_ph = ImageFont.truetype(FC_ITAL, 56)
    fn_ph2 = ImageFont.truetype(FC_REG, 42)
    mid_y = y + illus_h // 2
    d.text((CX, mid_y - 50), "Matricaria chamomilla", fill=FOREST, font=fn_ph, anchor="mm")
    d.text((CX, mid_y + 30), "Illustration · Köhler's Medizinal-Pflanzen, 1887", fill=LGOLD, font=fn_ph2, anchor="mm")

    return y1


def make_botanica_demo(out_path="/home/user/Ebook/botanica_demo.png",
                       illus_path=None):
    img = Image.new("RGB", (W, H), CREAM)
    d   = ImageDraw.Draw(img)

    # ── Fonts ──────────────────────────────────────────────────────────
    fn_day    = ImageFont.truetype(FC_REG,  54)
    fn_name   = ImageFont.truetype(FC_BOLD, 138)
    fn_latin  = ImageFont.truetype(FC_ITAL,  76)
    fn_family = ImageFont.truetype(FC_REG,   52)
    fn_sec    = ImageFont.truetype(FP_BOLD,  58)
    fn_body   = ImageFont.truetype(FC_REG,   60)
    fn_props  = ImageFont.truetype(FC_ITAL,  60)
    fn_note   = ImageFont.truetype(FC_ITAL,  58)

    y = 72

    # ── Day header ─────────────────────────────────────────────────────
    d.text((CX, y), "Jour  1  ·  1er janvier", fill=GOLD, font=fn_day, anchor="mt")
    y += 82
    y = rule(d, y) + 22

    # ── Illustration ───────────────────────────────────────────────────
    if illus_path and os.path.exists(illus_path):
        try:
            illus = Image.open(illus_path).convert("RGB")
            ratio = min(TW / illus.width, 920 / illus.height)
            nw, nh = int(illus.width * ratio), int(illus.height * ratio)
            illus  = illus.resize((nw, nh), Image.LANCZOS)
            img.paste(illus, ((W - nw) // 2, y))
            y += nh
        except Exception:
            y = draw_illustration_placeholder(img, d, y)
    else:
        y = draw_illustration_placeholder(img, d, y)

    y += 28
    y = rule(d, y) + 34

    # ── Plant name ─────────────────────────────────────────────────────
    d.text((CX, y), "CAMOMILLE", fill=DARK, font=fn_name, anchor="mt")
    y += 148

    # ── Latin name ─────────────────────────────────────────────────────
    d.text((CX, y), "Matricaria chamomilla", fill=GOLD, font=fn_latin, anchor="mt")
    y += 90

    # ── Family · Origin ────────────────────────────────────────────────
    d.text((CX, y), "Asteraceae  ·  Europe centrale & Asie de l'Ouest",
           fill=DARK, font=fn_family, anchor="mt")
    y += 74
    y = rule(d, y, color=LGOLD, h=1) + 38

    # ── Propriétés ─────────────────────────────────────────────────────
    y = section_header(d, y, "Propriétés", fn_sec)
    y = body_block(d, y,
        "Antispasmodique  ·  Anti-inflammatoire  ·  Sédatif léger  ·  Carminatif  ·  Cicatrisant",
        fn_props)

    # ── Usages ─────────────────────────────────────────────────────────
    y = section_header(d, y, "Usages traditionnels", fn_sec)
    y = body_block(d, y,
        "Troubles digestifs (crampes, ballonnements, nausées), insomnies légères, "
        "anxiété, irritations cutanées, inflammations oculaires et conjonctivites.",
        fn_body)

    # ── Comment l'utiliser ─────────────────────────────────────────────
    y = section_header(d, y, "Comment l'utiliser", fn_sec)
    for item in [
        "Infusion : 1 c. à café de fleurs séchées dans 250 ml d'eau bouillante, 5 min. 2 à 3 tasses par jour.",
        "Huile essentielle : diluée dans une huile végétale, application locale sur zones douloureuses.",
        "Cataplasme : compresse imbibée d'infusion tiède sur les yeux fatigués ou irrités.",
    ]:
        y = bullet_item(d, y, item, fn_body, fn_body)

    # ── Précautions ────────────────────────────────────────────────────
    y = section_header(d, y, "Précautions", fn_sec)
    y = body_block(d, y,
        "Allergie possible chez les personnes sensibles aux Asteraceae (marguerites, seneçons). "
        "Déconseillée à forte dose pendant la grossesse.",
        fn_body)

    y = rule(d, y, color=LGOLD, h=1) + 28

    # ── Le savais-tu ───────────────────────────────────────────────────
    d.text((MARGIN, y), "Le savais-tu ?", fill=GOLD, font=fn_sec)
    y += 72
    y = body_block(d, y,
        "En Égypte ancienne, la camomille était consacrée au dieu soleil Râ et utilisée "
        "pour traiter la fièvre. Les Saxons la comptaient parmi leurs neuf herbes sacrées, "
        "capables de repousser le poison et la maladie.",
        fn_note, color=DARK)

    y = rule(d, y, color=LGOLD, h=1) + 24

    # ── Présente dans ──────────────────────────────────────────────────
    d.text((CX, y),
           "Europe  ·  Asie  ·  Amérique du Nord (naturalisée)  ·  Australie (naturalisée)",
           fill=GOLD, font=fn_family, anchor="mt")
    y += 60

    # ── Bottom rule ────────────────────────────────────────────────────
    rule(d, H - 60, color=GOLD)

    img.save(out_path)
    print(f"✓ {out_path}  (y_end={y} / {H})")


make_botanica_demo()
