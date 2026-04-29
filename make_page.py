from PIL import Image, ImageDraw, ImageFont
import sys
import os

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def make_page(image_path, cryptid, state, monument, output_path):
    DPI = 300
    PAGE = 2550          # 8.5 x 8.5 inches square

    MARGIN_TOP   = 80
    MARGIN_SIDE  = 80
    BORDER       = 15    # black frame thickness
    FRAME_SIZE   = PAGE - 2 * MARGIN_SIDE          # 2390px square frame
    IMAGE_SIZE   = FRAME_SIZE - 2 * BORDER         # inner image

    GAP          = 55    # space between frame and text
    NAME_SIZE    = 95
    SUB_SIZE     = 62

    # Load and center-crop to square
    src = Image.open(image_path).convert("RGB")
    w, h = src.size
    side = min(w, h)
    left = (w - side) // 2
    top  = (h - side) // 2
    src  = src.crop((left, top, left + side, top + side))
    src  = src.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)

    # Total height: top margin + frame + gap + 2 text lines + bottom margin
    TOTAL_H = MARGIN_TOP + FRAME_SIZE + GAP + NAME_SIZE + 20 + SUB_SIZE + 70
    page = Image.new("RGB", (PAGE, TOTAL_H), "white")
    draw = ImageDraw.Draw(page)

    # Black frame
    fx = MARGIN_SIDE
    fy = MARGIN_TOP
    draw.rectangle([fx, fy, fx + FRAME_SIZE, fy + FRAME_SIZE], fill="black")

    # Paste image inside frame
    page.paste(src, (fx + BORDER, fy + BORDER))

    # Fonts
    fn = ImageFont.truetype(FONT_BOLD, NAME_SIZE)
    fs = ImageFont.truetype(FONT_REG,  SUB_SIZE)

    # Text Y positions
    ty_name = fy + FRAME_SIZE + GAP
    ty_sub  = ty_name + NAME_SIZE + 20

    cx = PAGE // 2

    # Cryptid name — uppercase bold centered
    draw.text((cx, ty_name), cryptid.upper(), fill="black", font=fn, anchor="mt")

    # State · Monument — regular centered
    subtitle = f"{state}  ·  {monument}"
    draw.text((cx, ty_sub), subtitle, fill="black", font=fs, anchor="mt")

    page.save(output_path, "PNG", dpi=(DPI, DPI))
    print(f"Saved → {output_path}")


if __name__ == "__main__":
    # Args: image_path cryptid state monument output
    make_page(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
