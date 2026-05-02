from PIL import Image, ImageDraw, ImageFont
import os

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# TODO: set these two paths to match your Backyard Birds files
PAGES_DIR = "/home/user/Ebook/BackyardBirds/pages"
OUT_PDF   = "/home/user/Ebook/BackyardBirds_Vol1_Interior.pdf"

DPI     = 300
W_TRIM  = round(8.5   * DPI)    # 2550px — trim size
H_TRIM  = round(8.5   * DPI)    # 2550px
BLEED   = round(0.125 * DPI)    # 38px  — KDP required bleed each side
W       = W_TRIM + 2 * BLEED    # 2626px — canvas with bleed
H       = H_TRIM + 2 * BLEED    # 2626px
MARGIN  = round(0.375 * DPI)    # 113px — safe zone from trim edge


def with_bleed(trim_img):
    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(trim_img, (BLEED, BLEED))
    return canvas


def fit_on_canvas(img):
    safe_w = W_TRIM - 2 * MARGIN
    safe_h = H_TRIM - 2 * MARGIN
    iw, ih = img.size
    scale  = min(safe_w / iw, safe_h / ih)
    nw, nh = round(iw * scale), round(ih * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    trim = Image.new("RGB", (W_TRIM, H_TRIM), "white")
    trim.paste(resized, (MARGIN + (safe_w - nw) // 2,
                         MARGIN + (safe_h - nh) // 2))
    return with_bleed(trim)


def blank_page():
    return Image.new("RGB", (W, H), "white")


def title_page():
    trim = Image.new("RGB", (W_TRIM, H_TRIM), "white")
    draw = ImageDraw.Draw(trim)
    cx   = W_TRIM // 2
    fn_t = ImageFont.truetype(FONT_BOLD, 185)
    fn_s = ImageFont.truetype(FONT_REG,  90)
    fn_v = ImageFont.truetype(FONT_BOLD, 120)
    fn_a = ImageFont.truetype(FONT_REG,  80)

    # TODO: update title text to match your Backyard Birds book
    draw.text((cx, 520),  "BACKYARD BIRDS",          fill="black", font=fn_t, anchor="mt")
    draw.line([(280, 800), (W_TRIM-280, 800)],        fill="black", width=7)
    draw.text((cx, 850),  "Birds of North America",  fill="black", font=fn_s, anchor="mt")
    draw.text((cx, 990),  "Vol. 1",                  fill="black", font=fn_v, anchor="mt")
    draw.line([(280, 1190), (W_TRIM-280, 1190)],      fill="black", width=7)
    draw.text((cx, 1780), "A Kawaii Coloring Book",  fill="black", font=fn_s, anchor="mt")
    draw.text((cx, 2200), "Mimi Doodle",             fill="black", font=fn_a, anchor="mt")
    return with_bleed(trim)


def copyright_page():
    trim = Image.new("RGB", (W_TRIM, H_TRIM), "white")
    draw = ImageDraw.Draw(trim)
    cx   = W_TRIM // 2
    fn   = ImageFont.truetype(FONT_REG, 58)
    fn2  = ImageFont.truetype(FONT_REG, 44)

    # TODO: update book title in first line to match your book
    entries = [
        (fn,  "Backyard Birds: Birds of North America — Vol. 1",          500),
        (fn,  "© 2025 Mimi Doodle. All rights reserved.",                 595),
        (fn2, "No part of this book may be reproduced or distributed",    760),
        (fn2, "in any form without prior written permission.",            815),
        (fn2, "Illustrations created with AI-assisted artwork.",          920),
        (fn2, "First published 2025.",                                    1025),
        (fn2, "Printed in the United States of America.",                1080),
        (fn2, "Published independently via Amazon KDP.",                 1185),
    ]
    for f, text, y in entries:
        draw.text((cx, y), text, fill="black", font=f, anchor="mt")
    return with_bleed(trim)


# TODO: replace with your actual filenames and bird names in the correct order
PAGE_ORDER = [
    ("Bird_01.png", "American Robin"),
    ("Bird_02.png", "Blue Jay"),
    ("Bird_03.png", "Cardinal"),
    ("Bird_04.png", "Chickadee"),
    ("Bird_05.png", "Downy Woodpecker"),
    # ... continue with your full list ...
]


print("Assembling Backyard Birds Vol.1 interior PDF...")
print(f"Page size : {W}×{H}px ({W/DPI:.3f}\"×{H/DPI:.3f}\") — includes {BLEED}px bleed each side")

all_pages = [title_page(), copyright_page(), blank_page(), blank_page()]

for i, (filename, bird) in enumerate(PAGE_ORDER):
    path = os.path.join(PAGES_DIR, filename)
    if not os.path.exists(path):
        print(f"  MISSING: {filename} ({bird}) — blank substituted")
        all_pages.append(blank_page())
    else:
        img = Image.open(path).convert("RGB")
        all_pages.append(fit_on_canvas(img))
        print(f"  [{i+1:02d}/{len(PAGE_ORDER):02d}] {bird}")
    all_pages.append(blank_page())

total = len(all_pages)
spine_in = total * 0.002252
print(f"\nTotal pages : {total}")
print(f"Spine width : {spine_in:.4f}\" ({round(spine_in * 300)}px at 300 DPI)")

first = all_pages[0]
rest  = all_pages[1:]
first.save(OUT_PDF, "PDF", resolution=DPI, save_all=True, append_images=rest)
print(f"\nSaved → {OUT_PDF}")
