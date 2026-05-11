"""
"One Word a Day" — The Curiosity Press
Page KDP carrée 8×8in (2400×2400px, 300 DPI)
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

BG_PATH = "/root/.claude/uploads/ed975202-b10e-4904-b9ca-246001848a28/2be84b39-1000008697.png"
OUT_DIR  = "/home/user/Ebook"

W, H   = 2400, 2400
CREAM  = (252, 249, 242)
GOLD   = (168, 138, 82)
DARK   = (38,  32,  24)
GRAY   = (120, 110, 95)
LGRAY  = (190, 180, 162)
RULE   = (210, 200, 182)

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
    draw.rectangle([x1, y, x2, y + w], fill=color)


# ── Mini flag data ─────────────────────────────────────────────────────────────
# (kind, color1, color2, color3)
_FLAGS = {
    "DANISH":               ("nordic",  (198,12,48),    (255,255,255), None),
    "NORWEGIAN":            ("nordic",  (239,43,45),    (255,255,255), (0,40,104)),
    "SWEDISH":              ("nordic",  (0,106,167),    (254,204,2),   None),
    "FINNISH":              ("nordic",  (255,255,255),  (0,53,128),    None),
    "ICELANDIC":            ("nordic",  (0,79,157),     (255,255,255), (220,0,0)),
    "GERMAN":               ("h3",      (0,0,0),        (221,0,0),     (255,206,0)),
    "DUTCH":                ("h3",      (174,28,40),    (255,255,255), (33,70,139)),
    "RUSSIAN":              ("h3",      (255,255,255),  (0,57,166),    (213,43,30)),
    "POLISH":               ("h2",      (255,255,255),  (220,0,0),     None),
    "CZECH":                ("czech",   (255,255,255),  (215,20,26),   (17,69,126)),
    "FRENCH":               ("v3",      (0,85,164),     (255,255,255), (239,65,53)),
    "ITALIAN":              ("v3",      (0,146,70),     (255,255,255), (206,43,55)),
    "SPANISH":              ("h4",      (170,21,27),    (241,191,0),   None),
    "PORTUGUESE":           ("pt",      (0,102,0),      (220,0,0),     (255,215,0)),
    "BRAZILIAN PORTUGUESE": ("pt",      (0,102,0),      (220,0,0),     (255,215,0)),
    "JAPANESE":             ("circle",  (255,255,255),  (188,0,45),    None),
    "KOREAN":               ("circle",  (255,255,255),  (205,46,58),   None),
    "INUIT":                ("circle",  (255,255,255),  (204,12,0),    None),
    "TURKISH":              ("turkish", (227,10,23),    (255,255,255), None),
    "GREEK":                ("greek",   (13,94,175),    (255,255,255), None),
    "HEBREW":               ("israel",  (255,255,255),  (0,56,184),    None),
    "ARABIC":               ("solid",   (0,106,78),     None,          None),
    "WELSH":                ("welsh",   (255,255,255),  (0,159,40),    (210,16,52)),
    "URDU":                 ("india",   (255,153,51),   (255,255,255), (19,136,8)),
    "HINDI":                ("india",   (255,153,51),   (255,255,255), (19,136,8)),
    "SANSKRIT":             ("india",   (255,153,51),   (255,255,255), (19,136,8)),
    "BORO":                 ("india",   (255,153,51),   (255,255,255), (19,136,8)),
    "ZULU":                 ("solid",   (0,119,73),     None,          None),
    "TAGALOG":              ("solid",   (0,56,168),     None,          None),
    "YAGHAN":               ("solid",   (180,170,155),  None,          None),
}


def draw_mini_flag(draw, cx, cy, language):
    """Draw a 100×66 mini flag centered at (cx, cy)."""
    FW, FH = 100, 66
    x0, y0 = cx - FW // 2, cy - FH // 2
    x1, y1 = cx + FW // 2, cy + FH // 2
    mx = x0 + FW // 3   # Nordic cross vertical bar (offset left)

    lang = language.upper()
    kind, c1, c2, c3 = _FLAGS.get(lang, ("solid", (200,185,165), None, None))

    # Drop shadow
    draw.rectangle([x0+3, y0+3, x1+3, y1+3], fill=(195,185,170))

    # Base
    draw.rectangle([x0, y0, x1, y1], fill=c1 or (235,228,215))

    if kind == "nordic":
        draw.rectangle([x0, cy-5, x1, cy+5], fill=c2)
        draw.rectangle([mx-5, y0, mx+5, y1], fill=c2)
        if c3:
            draw.rectangle([x0, cy-3, x1, cy+3], fill=c3)
            draw.rectangle([mx-3, y0, mx+3, y1], fill=c3)

    elif kind == "h3":
        h = FH // 3
        draw.rectangle([x0, y0+h,   x1, y0+2*h], fill=c2)
        draw.rectangle([x0, y0+2*h, x1, y1],     fill=c3)

    elif kind == "h2":
        draw.rectangle([x0, y0+FH//2, x1, y1], fill=c2)

    elif kind == "h4":
        draw.rectangle([x0, y0+FH//4, x1, y0+3*FH//4], fill=c2)

    elif kind == "v3":
        w3 = FW // 3
        draw.rectangle([x0+w3,   y0, x0+2*w3, y1], fill=c2)
        draw.rectangle([x0+2*w3, y0, x1,       y1], fill=c3)

    elif kind == "circle":
        draw.ellipse([cx-17, cy-17, cx+17, cy+17], fill=c2)

    elif kind == "pt":
        # Portugal: narrow green stripe left, red right, gold sphere on seam
        draw.rectangle([x0+FW*2//5, y0, x1, y1], fill=c2)
        draw.ellipse([cx-FW//5-4, cy-14, cx-FW//5+16, cy+14], fill=c3)

    elif kind == "czech":
        draw.rectangle([x0, cy, x1, y1], fill=c2)
        draw.polygon([(x0,y0),(x0+FW//2,cy),(x0,y1)], fill=c3)

    elif kind == "israel":
        draw.rectangle([x0, y0+FH//6,   x1, y0+2*FH//6], fill=c2)
        draw.rectangle([x0, y0+4*FH//6, x1, y0+5*FH//6], fill=c2)

    elif kind == "welsh":
        draw.rectangle([x0, cy, x1, y1], fill=c2)
        # Simplified dragon hint
        draw.ellipse([cx-13, cy-24, cx+13, cy+4], fill=c3)

    elif kind == "turkish":
        draw.ellipse([cx-18, cy-13, cx+11, cy+13], fill=c2)
        draw.ellipse([cx-11, cy-10, cx+14, cy+10], fill=c1)

    elif kind == "greek":
        h = FH // 5
        for i in range(5):
            if i % 2 == 1:
                draw.rectangle([x0, y0+i*h, x1, y0+(i+1)*h], fill=c2)

    elif kind == "india":
        h3 = FH // 3
        draw.rectangle([x0, y0,      x1, y0+h3],   fill=c1)
        draw.rectangle([x0, y0+h3,   x1, y0+2*h3], fill=c2)
        draw.rectangle([x0, y0+2*h3, x1, y1],       fill=c3)

    # Gold border
    draw.rectangle([x0, y0, x1, y1], outline=GOLD, width=2)


# ── Page renderer ─────────────────────────────────────────────────────────────

def make_page(day_num, date_str, word, language, country, capital, pronunciation,
              definition, etymology, example, cultural_note,
              related, quote, quote_author,
              out_name="word_demo.png"):

    # Canvas
    img = Image.new("RGB", (W, H), CREAM)

    # Watercolor background
    bg       = Image.open(BG_PATH).convert("RGB")
    bg_start = round(H * 0.60)
    bg_zone  = H - bg_start
    scale    = max(bg_zone / bg.height, W / bg.width)
    nw, nh   = round(bg.width * scale), round(bg.height * scale)
    bg = bg.resize((nw, nh), Image.LANCZOS)
    bg = bg.crop(((nw - W) // 2, 0, (nw - W) // 2 + W, bg_zone))
    arr  = np.array(bg, float)
    fade = 260
    for i in range(min(fade, bg_zone)):
        t = i / fade
        arr[i] = np.array(CREAM) * (1 - t) + arr[i] * t
    img.paste(Image.fromarray(arr.astype("uint8")), (0, bg_start))

    draw = ImageDraw.Draw(img)

    # Gold bands
    draw.rectangle([0, 0, W, 9],   fill=GOLD)
    draw.rectangle([0, H-9, W, H], fill=GOLD)

    # ── Date ──────────────────────────────────────────────────────────────────
    fn_date = ImageFont.truetype(FC_REG, 60)
    draw.text((W // 2, 38), f"Day {day_num}  ·  {date_str}",
              fill=LGRAY, font=fn_date, anchor="mt")
    rule(draw, 122)

    # ── Word ──────────────────────────────────────────────────────────────────
    fn_word = ImageFont.truetype(FP_ITAL, 295)
    draw.text((W // 2, 142), word, fill=DARK, font=fn_word, anchor="mt")

    # ── Flag + Language + Pronunciation ───────────────────────────────────────
    flag_cy = 462
    draw_mini_flag(draw, W // 2, flag_cy, language)

    fn_lang = ImageFont.truetype(FC_REG, 72)
    draw.text((W // 2, flag_cy + 46),
              f"{language.upper()}  —  {country} ({capital})  ·  {pronunciation}",
              fill=GOLD, font=fn_lang, anchor="mt")
    rule(draw, 618)
    y = 646

    # ── Definition ────────────────────────────────────────────────────────────
    fn_def = ImageFont.truetype(FP_REG, 82)
    for line in wrap(definition, fn_def, draw, W - 300):
        draw.text((W // 2, y), line, fill=DARK, font=fn_def, anchor="mt")
        y += 98
    y += 12

    # ── Etymology ─────────────────────────────────────────────────────────────
    fn_etym_lbl = ImageFont.truetype(FC_BOLD, 58)
    fn_etym     = ImageFont.truetype(FC_ITAL, 66)
    draw.text((W // 2, y), "Etymology", fill=GOLD, font=fn_etym_lbl, anchor="mt")
    y += 70
    for line in wrap(etymology, fn_etym, draw, W - 300):
        draw.text((W // 2, y), line, fill=GRAY, font=fn_etym, anchor="mt")
        y += 80
    y += 10
    rule(draw, y); y += 36

    # ── Example ───────────────────────────────────────────────────────────────
    fn_ex = ImageFont.truetype(FC_ITAL, 74)
    for line in wrap(f'"{example}"', fn_ex, draw, W - 320):
        draw.text((W // 2, y), line, fill=GRAY, font=fn_ex, anchor="mt")
        y += 88
    y += 10
    rule(draw, y); y += 36

    # ── Cultural note ─────────────────────────────────────────────────────────
    fn_note = ImageFont.truetype(FC_REG, 66)
    draw.text((168, y), "✦", fill=GOLD, font=fn_note, anchor="lt")
    for line in wrap(cultural_note, fn_note, draw, W - 370):
        draw.text((W // 2, y), line, fill=DARK, font=fn_note, anchor="mt")
        y += 80
    y += 24

    # ═══ Watercolor zone ══════════════════════════════════════════════════════
    rule(draw, y, color=GOLD, w=2); y += 48

    # ── Related words ─────────────────────────────────────────────────────────
    fn_rel_lbl = ImageFont.truetype(FC_BOLD, 56)
    fn_rel     = ImageFont.truetype(FP_ITAL, 70)
    draw.text((W // 2, y), "Same feeling, other words",
              fill=GOLD, font=fn_rel_lbl, anchor="mt")
    y += 70
    draw.text((W // 2, y), related, fill=DARK, font=fn_rel, anchor="mt")
    y += 92
    rule(draw, y); y += 40

    # ── Quote ─────────────────────────────────────────────────────────────────
    fn_q  = ImageFont.truetype(FC_ITAL, 72)
    fn_qa = ImageFont.truetype(FC_REG,  58)
    for line in wrap(f'"{quote}"', fn_q, draw, W - 340):
        draw.text((W // 2, y), line, fill=DARK, font=fn_q, anchor="mt")
        y += 86
    y += 8
    draw.text((W // 2, y), f"— {quote_author}", fill=GOLD, font=fn_qa, anchor="mt")

    img.save(os.path.join(OUT_DIR, out_name))
    print(f"✓ {out_name}  (content ends y={y})")


# ── Demo ──────────────────────────────────────────────────────────────────────

make_page(
    day_num       = 1,
    date_str      = "January 1",
    word          = "Hygge",
    language      = "Danish",
    country       = "Denmark",
    capital       = "Copenhagen",
    pronunciation = "[ HUE-gah ]",
    definition    = "The art of creating warm, cozy moments of togetherness that nurture a deep sense of well-being and contentment.",
    etymology     = "From Old Norse hygga — to comfort, to console. Related to the English word hug.",
    example       = "She lit candles, brewed tea, and let hygge fill the quiet Sunday afternoon.",
    cultural_note = "Danes consistently rank among the world's happiest people — and hygge is widely cited as their secret.",
    related       = "Gezellig (Dutch)  ·  Gemütlich (German)  ·  Mysig (Swedish)",
    quote         = "Life itself is the most wonderful fairy tale.",
    quote_author  = "Hans Christian Andersen",
    out_name      = "word_jan01_hygge.png",
)

make_page(
    day_num       = 2,
    date_str      = "January 2",
    word          = "Saudade",
    language      = "Portuguese",
    country       = "Portugal",
    capital       = "Lisbon",
    pronunciation = "[ saw-DAH-deh ]",
    definition    = "A deep, bittersweet longing for someone or something beloved that is absent, lost, or may never have truly existed.",
    etymology     = "From Latin solitatem — solitude. Shaped by centuries of Portuguese seafaring and exile.",
    example       = "Listening to old records alone, he was quietly overcome by saudade.",
    cultural_note = "Saudade is the emotional soul of Portugal and Brazil — the very heart of fado music.",
    related       = "Hiraeth (Welsh)  ·  Toska (Russian)  ·  Sehnsucht (German)",
    quote         = "Everything is worth it if the soul is not small.",
    quote_author  = "Fernando Pessoa",
    out_name      = "word_jan02_saudade.png",
)
