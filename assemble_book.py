from PIL import Image, ImageDraw, ImageFont
import os

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
PAGES_DIR = "/home/user/Ebook/pages"
OUT_PDF   = "/home/user/Ebook/TinyMonsters_Vol1_Interior.pdf"

DPI     = 300
W_TRIM  = round(8.5   * DPI)    # 2550px — trim size
H_TRIM  = round(8.5   * DPI)    # 2550px
BLEED   = round(0.125 * DPI)    # 38px  — KDP required bleed each side
W       = W_TRIM + 2 * BLEED    # 2626px — canvas with bleed
H       = H_TRIM + 2 * BLEED    # 2626px
MARGIN  = round(0.375 * DPI)    # 113px — safe zone from trim edge


def with_bleed(trim_img):
    """Wrap a trim-size image in a white bleed canvas."""
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

    draw.text((cx, 520),  "TINY MONSTERS",          fill="black", font=fn_t, anchor="mt")
    draw.line([(280, 800), (W_TRIM-280, 800)],        fill="black", width=7)
    draw.text((cx, 850),  "Cryptids of the USA",     fill="black", font=fn_s, anchor="mt")
    draw.text((cx, 990),  "Vol. 1",                  fill="black", font=fn_v, anchor="mt")
    draw.line([(280, 1190), (W_TRIM-280, 1190)],      fill="black", width=7)
    draw.text((cx, 1780), "A Kawaii Coloring Book",   fill="black", font=fn_s, anchor="mt")
    draw.text((cx, 2200), "Lumi Doodle",              fill="black", font=fn_a, anchor="mt")
    return with_bleed(trim)


def copyright_page():
    trim = Image.new("RGB", (W_TRIM, H_TRIM), "white")
    draw = ImageDraw.Draw(trim)
    cx   = W_TRIM // 2
    fn   = ImageFont.truetype(FONT_REG, 58)
    fn2  = ImageFont.truetype(FONT_REG, 44)

    entries = [
        (fn,  "Tiny Monsters: Cryptids of the USA — Vol. 1",          500),
        (fn,  "© 2025 Lumi Doodle. All rights reserved.",             595),
        (fn2, "No part of this book may be reproduced or distributed", 760),
        (fn2, "in any form without prior written permission.",         815),
        (fn2, "Illustrations created with AI-assisted artwork.",       920),
        (fn2, "First published 2025.",                                 1025),
        (fn2, "Printed in the United States of America.",             1080),
        (fn2, "Published independently via Amazon KDP.",              1185),
    ]
    for f, text, y in entries:
        draw.text((cx, y), text, fill="black", font=f, anchor="mt")
    return with_bleed(trim)


# Correct alphabetical order — file → state label
PAGE_ORDER = [
    ("Monster_01.png",            "Alabama"),
    ("Monster_02.png",            "Alaska"),
    ("Monster_03.png",            "Arizona"),
    ("Monster_04.png",            "Arkansas"),
    ("Monster_05.png",            "California"),
    ("Monster_06.png",            "Colorado"),
    ("Monster_07.png",            "Connecticut"),
    ("Monster_08.png",            "Delaware"),
    ("Monster_09.png",            "Florida"),
    ("Monster_10.png",            "Georgia"),
    ("Monster_11.png",            "Hawaii"),
    ("Monster_12.png",            "Idaho"),
    ("Monster_13.png",            "Illinois"),
    ("Monster_14.png",            "Indiana"),
    ("Monster_15.png",            "Iowa"),
    ("Monster_16.png",            "Kansas"),
    ("Monster_17_KENTUCKY.png",   "Kentucky"),
    ("Monster_17.png",            "Louisiana"),
    ("Monster_18.png",            "Maine"),
    ("Monster_19.png",            "Maryland"),
    ("Monster_20.png",            "Massachusetts"),
    ("Monster_21.png",            "Michigan"),
    ("Monster_22.png",            "Minnesota"),
    ("Monster_23.png",            "Mississippi"),
    ("Monster_24.png",            "Missouri"),
    ("Monster_25.png",            "Montana"),
    ("Monster_26.png",            "Nebraska"),
    ("Monster_27.png",            "Nevada"),
    ("Monster_28.png",            "New Hampshire"),
    ("Monster_29.png",            "New Jersey"),
    ("Monster_30.png",            "New Mexico"),
    ("Monster_31.png",            "New York"),
    ("Monster_32.png",            "North Carolina"),
    ("Monster_33.png",            "North Dakota"),
    ("Monster_34.png",            "Ohio"),
    ("Monster_35.png",            "Oklahoma"),
    ("Monster_36.png",            "Oregon"),
    ("Monster_37.png",            "Pennsylvania"),
    ("Monster_38.png",            "Rhode Island"),
    ("Monster_39.png",            "South Carolina"),
    ("Monster_40.png",            "South Dakota"),
    ("Monster_41.png",            "Tennessee"),
    ("Monster_42.png",            "Texas"),
    ("Monster_43.png",            "Utah"),
    ("Monster_44.png",            "Vermont"),
    ("Monster_45.png",            "Virginia"),
    ("Monster_46_WASHINGTON.png", "Washington"),
    ("Monster_47.png",            "West Virginia"),
    ("Monster_48.png",            "Wisconsin"),
    ("Monster_49.png",            "Wyoming"),
]

print("Assembling Tiny Monsters Vol.1 interior PDF...")
print(f"Page size : {W}×{H}px ({W/DPI:.3f}\"×{H/DPI:.3f}\") — includes {BLEED}px bleed each side")

all_pages = [title_page(), copyright_page(), blank_page(), blank_page()]

for i, (filename, state) in enumerate(PAGE_ORDER):
    path = os.path.join(PAGES_DIR, filename)
    if not os.path.exists(path):
        print(f"  ⚠️  MISSING: {filename} ({state}) — blank substituted")
        all_pages.append(blank_page())
    else:
        img = Image.open(path).convert("RGB")
        all_pages.append(fit_on_canvas(img))
        print(f"  [{i+1:02d}/50] {state}")
    all_pages.append(blank_page())

total = len(all_pages)
spine_in = total * 0.002252
print(f"\nTotal pages : {total}")
print(f"Spine width : {spine_in:.4f}\" ({round(spine_in * 300)}px at 300 DPI)")

first = all_pages[0]
rest  = all_pages[1:]
first.save(OUT_PDF, "PDF", resolution=DPI, save_all=True, append_images=rest)
print(f"\nSaved → {OUT_PDF}")
