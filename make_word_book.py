"""
"One Word a Day" — The Curiosity Press
Page KDP carrée 8×8in (2400×2400px, 300 DPI)
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

BG_PATH = "/root/.claude/uploads/ed975202-b10e-4904-b9ca-246001848a28/2be84b39-1000008697.png"
OUT_DIR  = "/home/user/Ebook"

W, H   = 2400, 2400          # 8×8 inch carré à 300 DPI
CREAM  = (252, 249, 242)
GOLD   = (168, 138, 82)
DARK   = (38,  32,  24)
GRAY   = (120, 110, 95)
LGRAY  = (190, 180, 162)
RULE   = (210, 200, 182)

# Polices élégantes
FC_REG  = "/home/user/Ebook/fonts/CormorantGaramond-Regular.ttf"
FC_BOLD = "/home/user/Ebook/fonts/CormorantGaramond-Bold.ttf"
FC_ITAL = "/home/user/Ebook/fonts/CormorantGaramond-Italic.ttf"
FP_BOLD = "/home/user/Ebook/fonts/PlayfairDisplay-Bold.ttf"
FP_ITAL = "/home/user/Ebook/fonts/PlayfairDisplay-Italic.ttf"
FP_REG  = "/home/user/Ebook/fonts/PlayfairDisplay-Regular.ttf"


def wrap(text, font, draw, max_w):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines


def rule(draw, y, x1=160, x2=None, color=None, w=1):
    if x2 is None: x2 = W - 160
    if color is None: color = RULE
    draw.rectangle([x1, y, x2, y+w], fill=color)


def ornament(draw, y, font_size=52):
    fn = ImageFont.truetype(FC_REG, font_size)
    draw.text((W//2, y), "✦", fill=GOLD, font=fn, anchor="mt")


def make_page(day_num, date_str, word, language, pronunciation,
              definition, etymology, example, cultural_note,
              related, quote, quote_author,
              out_name="word_demo.png"):

    # ── Canvas ────────────────────────────────────────────────────────────────
    img = Image.new("RGB", (W, H), CREAM)

    # ── Watercolor — remonte haut, texte écrit par-dessus ────────────────────
    bg = Image.open(BG_PATH).convert("RGB")
    # Étirer pour couvrir la moitié inférieure de la page
    bg_start = H // 2 - 80
    bg_zone  = H - bg_start
    scale_h  = bg_zone / bg.height
    scale_w  = W / bg.width
    scale    = max(scale_h, scale_w)
    nw, nh   = round(bg.width*scale), round(bg.height*scale)
    bg = bg.resize((nw, nh), Image.LANCZOS)
    bg = bg.crop(((nw-W)//2, 0, (nw-W)//2+W, bg_zone))

    # Fondu progressif cream → watercolor sur 220px
    arr  = np.array(bg, float)
    fade = 220
    for i in range(min(fade, bg_zone)):
        t = i / fade
        arr[i] = np.array(CREAM)*(1-t) + arr[i]*t
    img.paste(Image.fromarray(arr.astype("uint8")), (0, bg_start))

    draw = ImageDraw.Draw(img)

    # ── Bandes dorées ─────────────────────────────────────────────────────────
    draw.rectangle([0, 0, W, 9], fill=GOLD)
    draw.rectangle([0, H-9, W, H], fill=GOLD)

    # ── Date & numéro ─────────────────────────────────────────────────────────
    fn_date = ImageFont.truetype(FC_REG, 50)
    draw.text((W//2, 36), f"Day {day_num}  ·  {date_str}",
              fill=LGRAY, font=fn_date, anchor="mt")
    rule(draw, 104)

    # ── LE MOT ────────────────────────────────────────────────────────────────
    fn_word = ImageFont.truetype(FP_ITAL, 248)
    draw.text((W//2, 122), word, fill=DARK, font=fn_word, anchor="mt")

    # ── Langue + prononciation ────────────────────────────────────────────────
    fn_lang = ImageFont.truetype(FC_REG, 58)
    draw.text((W//2, 390), f"{language.upper()}  ·  {pronunciation}",
              fill=GOLD, font=fn_lang, anchor="mt")
    rule(draw, 468)
    y = 494

    # ── Définition ────────────────────────────────────────────────────────────
    fn_def = ImageFont.truetype(FP_REG, 64)
    for line in wrap(definition, fn_def, draw, W-340):
        draw.text((W//2, y), line, fill=DARK, font=fn_def, anchor="mt")
        y += 78
    y += 8

    # ── Étymologie ────────────────────────────────────────────────────────────
    fn_etym_lbl = ImageFont.truetype(FC_BOLD, 46)
    fn_etym     = ImageFont.truetype(FC_ITAL, 52)
    draw.text((W//2, y), "Etymology", fill=GOLD, font=fn_etym_lbl, anchor="mt")
    y += 56
    for line in wrap(etymology, fn_etym, draw, W-340):
        draw.text((W//2, y), line, fill=GRAY, font=fn_etym, anchor="mt")
        y += 62
    y += 8
    rule(draw, y); y += 26

    # ── Phrase exemple ────────────────────────────────────────────────────────
    fn_ex = ImageFont.truetype(FC_ITAL, 58)
    for line in wrap(f'"{example}"', fn_ex, draw, W-360):
        draw.text((W//2, y), line, fill=GRAY, font=fn_ex, anchor="mt")
        y += 68
    y += 6
    rule(draw, y); y += 26

    # ── Note culturelle ── (sur fond cream encore)
    fn_note = ImageFont.truetype(FC_REG, 52)
    draw.text((168, y), "✦", fill=GOLD, font=fn_note, anchor="lt")
    for line in wrap(cultural_note, fn_note, draw, W-400):
        draw.text((W//2, y), line, fill=DARK, font=fn_note, anchor="mt")
        y += 62
    y += 16

    # ═══ À partir d'ici : texte sur l'aquarelle ════════════════════════════
    rule(draw, y, color=GOLD, w=2); y += 36

    # ── Mots apparentés ───────────────────────────────────────────────────────
    fn_rel_lbl = ImageFont.truetype(FC_BOLD, 44)
    fn_rel     = ImageFont.truetype(FP_ITAL, 54)
    draw.text((W//2, y), "Also in the world", fill=GOLD,
              font=fn_rel_lbl, anchor="mt")
    y += 54
    draw.text((W//2, y), related, fill=DARK, font=fn_rel, anchor="mt")
    y += 72

    rule(draw, y); y += 30

    # ── Citation ──────────────────────────────────────────────────────────────
    fn_q  = ImageFont.truetype(FC_ITAL, 56)
    fn_qa = ImageFont.truetype(FC_REG,  46)
    for line in wrap(f'"{quote}"', fn_q, draw, W-380):
        draw.text((W//2, y), line, fill=DARK, font=fn_q, anchor="mt")
        y += 68
    y += 4
    draw.text((W//2, y), f"— {quote_author}", fill=GOLD, font=fn_qa, anchor="mt")

    img.save(os.path.join(OUT_DIR, out_name))
    print(f"✓ {out_name}")


# ── Pages demo ────────────────────────────────────────────────────────────────

make_page(
    day_num      = 1,
    date_str     = "January 1",
    word         = "Hygge",
    language     = "Danish",
    pronunciation= "[ HUE-gah ]",
    definition   = "The art of creating warm, cozy moments of togetherness that nurture a deep sense of well-being and contentment.",
    etymology    = "From Old Norse hygga — to comfort, to console. Related to the English word hug.",
    example      = "She lit candles, brewed tea, and let hygge fill the quiet Sunday afternoon.",
    cultural_note= "Danes consistently rank among the world's happiest people — and hygge is widely cited as their secret.",
    related      = "Gezellig (Dutch)  ·  Gemütlich (German)  ·  Mysig (Swedish)",
    quote        = "There is no duty we so much underrate as the duty of being happy.",
    quote_author = "Robert Louis Stevenson",
    out_name     = "word_jan01_hygge.png"
)

make_page(
    day_num      = 2,
    date_str     = "January 2",
    word         = "Saudade",
    language     = "Portuguese",
    pronunciation= "[ saw-DAH-deh ]",
    definition   = "A deep, bittersweet longing for someone or something beloved that is absent, lost, or may never have truly existed.",
    etymology    = "From Latin solitatem — solitude. Shaped by centuries of Portuguese seafaring and exile.",
    example      = "Listening to old records alone, he was quietly overcome by saudade.",
    cultural_note= "Saudade is the emotional soul of Portugal and Brazil — the very heart of fado music.",
    related      = "Hiraeth (Welsh)  ·  Toska (Russian)  ·  Sehnsucht (German)",
    quote        = "The bitterest tears shed over graves are for words left unsaid and deeds left undone.",
    quote_author = "Harriet Beecher Stowe",
    out_name     = "word_jan02_saudade.png"
)
