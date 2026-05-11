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
              out_name="word_demo.png"):

    # ── Canvas ────────────────────────────────────────────────────────────────
    img  = Image.new("RGB", (W, H), CREAM)

    # ── Watercolor en bas ─────────────────────────────────────────────────────
    bg    = Image.open(BG_PATH).convert("RGB")
    scale = W / bg.width
    bh    = round(bg.height * scale)
    bg    = bg.resize((W, bh), Image.LANCZOS)

    # Fondu cream → watercolor
    arr = np.array(bg)
    fade = 180  # pixels de fondu
    for i in range(fade):
        t = i / fade
        arr[i] = (np.array(CREAM)*(1-t) + arr[i]*t).astype("uint8")
    bg = Image.fromarray(arr)
    img.paste(bg, (0, H - bh))

    draw = ImageDraw.Draw(img)

    # ── Marge dorée supérieure ────────────────────────────────────────────────
    draw.rectangle([0, 0, W, 8], fill=GOLD)

    # ── Date & numéro ─────────────────────────────────────────────────────────
    fn_date = ImageFont.truetype(FC_REG, 52)
    draw.text((W//2, 44), f"Day {day_num}  ·  {date_str}",
              fill=LGRAY, font=fn_date, anchor="mt")

    rule(draw, 116, color=RULE)

    # ── LE MOT — grande italique Playfair ─────────────────────────────────────
    fn_word = ImageFont.truetype(FP_ITAL, 260)
    draw.text((W//2, 136), word, fill=DARK, font=fn_word, anchor="mt")

    # ── Langue + prononciation ────────────────────────────────────────────────
    fn_lang = ImageFont.truetype(FC_REG, 62)
    lang_y  = 420
    draw.text((W//2, lang_y),
              f"{language.upper()}  ·  {pronunciation}",
              fill=GOLD, font=fn_lang, anchor="mt")

    rule(draw, lang_y + 86, color=RULE)
    y = lang_y + 110

    # ── Définition ────────────────────────────────────────────────────────────
    fn_def = ImageFont.truetype(FP_REG, 66)
    for line in wrap(definition, fn_def, draw, W - 340):
        draw.text((W//2, y), line, fill=DARK, font=fn_def, anchor="mt")
        y += 82
    y += 14

    # ── Étymologie ────────────────────────────────────────────────────────────
    fn_etym_lbl = ImageFont.truetype(FC_BOLD, 50)
    fn_etym     = ImageFont.truetype(FC_ITAL, 54)
    draw.text((W//2, y), "Etymology", fill=GOLD, font=fn_etym_lbl, anchor="mt")
    y += 60
    for line in wrap(etymology, fn_etym, draw, W - 340):
        draw.text((W//2, y), line, fill=GRAY, font=fn_etym, anchor="mt")
        y += 66
    y += 10

    rule(draw, y, color=RULE)
    y += 28

    # ── Phrase exemple ────────────────────────────────────────────────────────
    fn_ex = ImageFont.truetype(FC_ITAL, 60)
    for line in wrap(f'"{example}"', fn_ex, draw, W - 360):
        draw.text((W//2, y), line, fill=GRAY, font=fn_ex, anchor="mt")
        y += 72
    y += 10

    rule(draw, y, color=RULE)
    y += 30

    # ── Note culturelle ───────────────────────────────────────────────────────
    fn_note = ImageFont.truetype(FC_REG, 54)
    draw.text((160, y), "✦", fill=GOLD,
              font=ImageFont.truetype(FC_REG, 54), anchor="lt")
    note_lines = wrap(cultural_note, fn_note, draw, W - 400)
    for line in note_lines:
        draw.text((W//2, y), line, fill=DARK, font=fn_note, anchor="mt")
        y += 66

    # ── Marge dorée inférieure ────────────────────────────────────────────────
    draw.rectangle([0, H-8, W, H], fill=GOLD)

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
    cultural_note= "Danes rank among the world's happiest people — and hygge is widely cited as their secret.",
    out_name     = "word_jan01_hygge.png"
)

make_page(
    day_num      = 2,
    date_str     = "January 2",
    word         = "Saudade",
    language     = "Portuguese",
    pronunciation= "[ saw-DAH-deh ]",
    definition   = "A deep, bittersweet longing for someone or something beloved that is absent, lost, or may never have truly existed.",
    etymology    = "From Latin solitatem — solitude. Evolved through centuries of Portuguese seafaring and exile.",
    example      = "Listening to old records alone, he was quietly overcome by saudade.",
    cultural_note= "Saudade is considered the emotional soul of Portuguese and Brazilian culture, at the heart of fado music.",
    out_name     = "word_jan02_saudade.png"
)
