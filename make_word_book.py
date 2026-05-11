"""
"Untranslatable" — A Word for Every Day of the Year
Demo: génère une page KDP (1800×2700px, 6×9in portrait, 300 DPI)
"""
from PIL import Image, ImageDraw, ImageFont
import os

BG_PATH = "/root/.claude/uploads/ed975202-b10e-4904-b9ca-246001848a28/2be84b39-1000008697.png"
OUT_DIR  = "/home/user/Ebook"

# KDP 6×9 portrait at 300 DPI
W, H   = 1800, 2700
CREAM  = (252, 249, 242)
GOLD   = (180, 148, 90)
DARK   = (45,  38,  30)
GRAY   = (140, 128, 110)
LGRAY  = (195, 185, 168)

FXB  = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
FB   = "/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf"
FSB  = "/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf"
FREG = "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf"
FFRED = "/home/user/Ebook/fonts/FredokaOne-Regular.ttf"

def make_page(date_str, word, language, pronunciation, definition, example,
              out_name="word_demo.png"):
    # ── Canvas ────────────────────────────────────────────────────────────────
    img  = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # ── Watercolor background — anchored at bottom ────────────────────────────
    bg   = Image.open(BG_PATH).convert("RGB")
    # Scale to full width
    scale = W / bg.width
    bh    = round(bg.height * scale)
    bg    = bg.resize((W, bh), Image.LANCZOS)
    # Paste at bottom
    img.paste(bg, (0, H - bh))

    # Soft gradient overlay at top to blend cream into watercolor
    import numpy as np
    grad_h = H - bh + 120
    arr    = np.array(img)
    for y in range(max(0, H-bh-80), min(H, H-bh+160)):
        t = (y - (H-bh-80)) / 240
        t = max(0, min(1, t))
        # blend row toward cream
        arr[y] = (arr[y] * t + np.array(CREAM) * (1-t)).astype("uint8")
    img  = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    # ── Thin gold top rule ────────────────────────────────────────────────────
    draw.rectangle([120, 110, W-120, 113], fill=GOLD)

    # ── Date ─────────────────────────────────────────────────────────────────
    fn_date = ImageFont.truetype(FREG, 52)
    draw.text((W//2, 145), date_str.upper(),
              fill=LGRAY, font=fn_date, anchor="mt",
              spacing=8)

    # ── Word ─────────────────────────────────────────────────────────────────
    fn_word = ImageFont.truetype(FB, 210)
    draw.text((W//2, 230), word,
              fill=DARK, font=fn_word, anchor="mt")

    # ── Language + pronunciation ──────────────────────────────────────────────
    fn_lang = ImageFont.truetype(FREG, 56)
    lang_y  = 480
    draw.text((W//2, lang_y), f"{language}  ·  {pronunciation}",
              fill=GOLD, font=fn_lang, anchor="mt")

    # ── Thin gold divider ─────────────────────────────────────────────────────
    draw.rectangle([120, lang_y+76, W-120, lang_y+79], fill=LGRAY)

    # ── Definition ────────────────────────────────────────────────────────────
    fn_def  = ImageFont.truetype(FSB,  68)
    fn_body = ImageFont.truetype(FREG, 60)

    def wrap(text, font, max_w):
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

    def_y   = lang_y + 106
    max_w   = W - 280
    lines   = wrap(definition, fn_body, max_w)
    for line in lines:
        draw.text((W//2, def_y), line, fill=DARK, font=fn_body, anchor="mt")
        def_y += 82

    # ── Example sentence ──────────────────────────────────────────────────────
    ex_y   = def_y + 60
    draw.rectangle([120, ex_y, W-120, ex_y+3], fill=LGRAY)
    ex_y  += 36

    fn_ex   = ImageFont.truetype(FREG, 54)
    ex_lines = wrap(f'"{example}"', fn_ex, max_w)
    for line in ex_lines:
        draw.text((W//2, ex_y), line, fill=GRAY, font=fn_ex, anchor="mt")
        ex_y += 72

    # ── Bottom thin gold rule ─────────────────────────────────────────────────
    draw.rectangle([120, H-bh-30, W-120, H-bh-27], fill=GOLD)

    # ── Book title footer ─────────────────────────────────────────────────────
    fn_footer = ImageFont.truetype(FREG, 40)
    draw.text((W//2, H-bh+8), "UNTRANSLATABLE  ·  A Word for Every Day",
              fill=LGRAY, font=fn_footer, anchor="mt")

    img.save(os.path.join(OUT_DIR, out_name))
    print(f"✓ {out_name}")


# ── Demo pages ────────────────────────────────────────────────────────────────

make_page(
    date_str    = "January  1",
    word        = "Hygge",
    language    = "Danish",
    pronunciation = "[ HUE-gah ]",
    definition  = "The art of creating warm, cozy moments of comfort and togetherness that nurture a sense of well-being and contentment.",
    example     = "She lit candles, brewed tea, and let hygge fill the quiet Sunday afternoon.",
    out_name    = "word_jan01_hygge.png"
)

make_page(
    date_str    = "January  2",
    word        = "Saudade",
    language    = "Portuguese",
    pronunciation = "[ saw-DAH-deh ]",
    definition  = "A deep, bittersweet longing for someone or something beloved that is absent, lost, or may never have existed.",
    example     = "Listening to old records, he was overcome by saudade for summers long gone.",
    out_name    = "word_jan02_saudade.png"
)
