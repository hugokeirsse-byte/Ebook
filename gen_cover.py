"""
KDP full-wrap cover for "Backyard Birds of North America — Vol. 1"

Specs:
  Trim size : 8.5 × 11 in
  Pages     : 168  (60# cream paper)
  Spine     : 168 × 0.002252 = 0.3783 in  → rounded to 0.379 in
  Bleed     : 0.125 in on all sides

Canvas size:
  Width  = bleed + back(8.5) + spine(0.379) + front(8.5) + bleed
         = 0.125 + 8.5 + 0.379 + 8.5 + 0.125 = 17.629 in
  Height = bleed + 11 + bleed = 11.25 in
"""
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer

OUTPUT = "/home/user/Ebook/cover_kdp.pdf"

BLEED   = 0.125 * inch
SPINE   = 0.379 * inch
TRIM_W  = 8.5   * inch
TRIM_H  = 11.0  * inch

CW = 2 * BLEED + 2 * TRIM_W + SPINE   # total canvas width
CH = 2 * BLEED + TRIM_H                # total canvas height

# Key X positions
X_BACK_LEFT   = 0                       # left bleed edge
X_SPINE_LEFT  = BLEED + TRIM_W         # where spine starts
X_FRONT_LEFT  = X_SPINE_LEFT + SPINE   # where front cover starts
X_RIGHT       = CW                      # right bleed edge

# Safe zones (0.25 in inside trim on text-bearing sides)
SAFE = 0.25 * inch

G_DARK  = colors.HexColor("#1B4332")
G_MID   = colors.HexColor("#2D6A4F")
G_LIGHT = colors.HexColor("#B7E4C7")
GOLD    = colors.HexColor("#D4A017")
CREAM   = colors.HexColor("#FDFBF5")
GREY    = colors.HexColor("#C8C4BB")
DARK    = colors.HexColor("#1E1E1E")
WHITE   = colors.white

def sp(name,font,size,color=CREAM,leading=None,align=TA_LEFT,sb=0,sa=0):
    return ParagraphStyle(name,fontName=font,fontSize=size,textColor=color,
        leading=leading or size*1.4,alignment=align,spaceBefore=sb,spaceAfter=sa)

def draw_front(c):
    # Full bleed background
    c.setFillColor(G_DARK)
    c.rect(X_FRONT_LEFT, 0, TRIM_W + BLEED, CH, fill=1, stroke=0)

    # Decorative top band with diagonal texture lines
    band_h = 3.8 * inch
    c.setFillColor(G_MID)
    c.rect(X_FRONT_LEFT, CH - BLEED - band_h, TRIM_W + BLEED, band_h, fill=1, stroke=0)

    # Gold accent lines
    c.setStrokeColor(GOLD); c.setLineWidth(2.5)
    c.line(X_FRONT_LEFT, CH - BLEED - band_h, X_RIGHT, CH - BLEED - band_h)
    c.setLineWidth(0.8)
    c.line(X_FRONT_LEFT, CH - BLEED - band_h - 0.09*inch, X_RIGHT, CH - BLEED - band_h - 0.09*inch)

    # ── SERIES BADGE (top) ───────────────────────────────────────────────────
    bx = X_FRONT_LEFT + SAFE
    by = CH - BLEED - 0.55*inch
    bw = TRIM_W - 2*SAFE
    c.setFillColor(GOLD)
    c.roundRect(bx, by, bw, 0.34*inch, 4, fill=1, stroke=0)
    c.setFillColor(G_DARK); c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(X_FRONT_LEFT + TRIM_W/2, by + 0.10*inch,
        "BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")

    # ── MAIN TITLE ───────────────────────────────────────────────────────────
    cx = X_FRONT_LEFT + TRIM_W / 2
    c.setFillColor(CREAM); c.setFont("Helvetica-Bold", 54)
    c.drawCentredString(cx, CH - BLEED - 1.42*inch, "BACKYARD")
    c.setFont("Helvetica-Bold", 54)
    c.drawCentredString(cx, CH - BLEED - 2.10*inch, "BIRDS")
    c.setFillColor(G_LIGHT); c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(cx, CH - BLEED - 2.68*inch, "OF NORTH AMERICA")

    # Gold divider with diamond
    ly = CH - BLEED - 3.05*inch
    c.setStrokeColor(GOLD); c.setLineWidth(1.2)
    c.line(X_FRONT_LEFT + SAFE, ly, X_RIGHT - SAFE, ly)
    dm = cx
    p = c.beginPath()
    p.moveTo(dm, ly+7); p.lineTo(dm+6, ly); p.lineTo(dm, ly-7); p.lineTo(dm-6, ly)
    p.close()
    c.setFillColor(GOLD); c.drawPath(p, fill=1, stroke=0)

    # Subtitle
    c.setFillColor(CREAM); c.setFont("Helvetica-Oblique", 16)
    c.drawCentredString(cx, CH - BLEED - 3.42*inch, "A Coloring & Field Guide Book")

    # ── CENTRAL ILLUSTRATION AREA ─────────────────────────────────────────────
    # Decorative framed panel — cream border suggesting page/book
    px = X_FRONT_LEFT + SAFE + 0.1*inch
    py = BLEED + 2.1*inch
    pw = TRIM_W - 2*SAFE - 0.2*inch
    ph = CH - BLEED - 3.75*inch - py
    c.setFillColor(colors.HexColor("#163D2C"))
    c.roundRect(px, py, pw, ph, 8, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(1.0)
    c.roundRect(px, py, pw, ph, 8, fill=0, stroke=1)

    # Bird name grid inside panel
    birds = [
        "American Goldfinch", "Black-capped Chickadee", "Northern Cardinal",
        "Blue Jay", "Ruby-throated Hummingbird", "Eastern Bluebird",
        "American Robin", "Downy Woodpecker", "Northern Flicker",
        "Cedar Waxwing", "Baltimore Oriole", "American Kestrel",
    ]
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(px + pw/2, py + ph - 0.28*inch, "40 FEATURED SPECIES INCLUDE:")
    c.setStrokeColor(GOLD); c.setLineWidth(0.4)
    c.line(px + 0.2*inch, py + ph - 0.38*inch, px + pw - 0.2*inch, py + ph - 0.38*inch)

    col_w = pw / 2
    rows_per_col = (len(birds) + 1) // 2
    c.setFillColor(G_LIGHT); c.setFont("Helvetica", 8)
    for idx, name in enumerate(birds):
        col = idx // rows_per_col
        row = idx % rows_per_col
        tx = px + 0.18*inch + col * col_w
        ty = py + ph - 0.58*inch - row * 0.22*inch
        c.drawString(tx, ty, f"•  {name}")

    # "& many more" line
    c.setFillColor(GOLD); c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(px + pw/2, py + 0.18*inch, "& 28 more remarkable species")

    # ── BOTTOM INFO BAR ──────────────────────────────────────────────────────
    bar_h = 1.92*inch
    c.setFillColor(G_MID)
    c.rect(X_FRONT_LEFT, BLEED, TRIM_W + BLEED, bar_h, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.line(X_FRONT_LEFT, BLEED + bar_h, X_RIGHT, BLEED + bar_h)

    # Feature pills
    pills = ["40 Bird Species", "120 Coloring Pages", "Field Guide Data",
             "Color Guides", "Conservation Notes", "Feeder Tips"]
    pill_w = (TRIM_W - 2*SAFE) / 3
    for i, txt in enumerate(pills):
        col = i % 3; row = i // 3
        px2 = X_FRONT_LEFT + SAFE + col * pill_w + 0.05*inch
        py2 = BLEED + bar_h - 0.45*inch - row * 0.52*inch
        c.setFillColor(G_DARK)
        c.roundRect(px2, py2, pill_w - 0.1*inch, 0.28*inch, 3, fill=1, stroke=0)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(px2 + (pill_w-0.1*inch)/2, py2 + 0.07*inch, txt)

    # Tagline
    c.setFillColor(CREAM); c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(cx, BLEED + 0.28*inch,
        "For nature lovers, bird watchers, and coloring enthusiasts")

def draw_spine(c):
    # Spine background
    c.setFillColor(G_DARK)
    c.rect(X_SPINE_LEFT, 0, SPINE, CH, fill=1, stroke=0)
    # Gold side rules
    c.setStrokeColor(GOLD); c.setLineWidth(0.6)
    c.line(X_SPINE_LEFT, 0, X_SPINE_LEFT, CH)
    c.line(X_SPINE_LEFT + SPINE, 0, X_SPINE_LEFT + SPINE, CH)

    spine_cx = X_SPINE_LEFT + SPINE / 2
    spine_cy = CH / 2

    # Title along spine (rotated 90° — reads bottom to top)
    c.saveState()
    c.translate(spine_cx, spine_cy)
    c.rotate(90)
    c.setFillColor(CREAM); c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(0, 4, "BACKYARD BIRDS OF NORTH AMERICA")
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(0, -9, "A Coloring & Field Guide Book")
    c.restoreState()

    # Vol 1 badge at bottom of spine
    c.setFillColor(GOLD)
    c.roundRect(X_SPINE_LEFT + 2, BLEED + 0.12*inch, SPINE - 4, 0.28*inch, 2, fill=1, stroke=0)
    c.setFillColor(G_DARK); c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(spine_cx, BLEED + 0.18*inch, "VOL. 1")

def draw_back(c):
    # Full bleed background
    c.setFillColor(G_DARK)
    c.rect(0, 0, TRIM_W + BLEED, CH, fill=1, stroke=0)

    # Top band
    c.setFillColor(G_MID)
    c.rect(0, CH - BLEED - 1.1*inch, TRIM_W + BLEED, 1.1*inch, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(2.0)
    c.line(0, CH - BLEED - 1.1*inch, TRIM_W + BLEED, CH - BLEED - 1.1*inch)

    # Header text
    bx = BLEED + SAFE
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 8.5)
    c.drawString(bx, CH - BLEED - 0.4*inch, "BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica", 8.5)
    c.drawRightString(TRIM_W + BLEED - SAFE, CH - BLEED - 0.4*inch, "A Coloring & Field Guide Book")

    # Sub-header gold line
    c.setStrokeColor(GOLD); c.setLineWidth(0.7)
    c.line(bx, CH - BLEED - 0.58*inch, TRIM_W + BLEED - SAFE, CH - BLEED - 0.58*inch)

    # ── DESCRIPTION ──────────────────────────────────────────────────────────
    SB  = sp("bb","Helvetica",9.5,CREAM,14,align=TA_JUSTIFY)
    SH  = sp("bh","Helvetica-Bold",9,GOLD,13,sb=8,sa=2)
    SBU = sp("bu","Helvetica",9,G_LIGHT,13,sb=1)

    desc=[
        Spacer(1,0.05*inch),
        Paragraph(
            "Discover forty of the most beloved birds of North American backyards, "
            "parks, and woodlands — each brought to life through detailed educational "
            "content and a full-page coloring illustration waiting to be filled with color.",SB),
        Paragraph("WHAT'S INSIDE",SH),
        Paragraph("Each of the 40 bird modules includes:",SB),
        Paragraph("•  Two pages of natural history: habitat &amp; range, diet, behavior, "
            "nesting, song, and conservation status",SBU),
        Paragraph("•  Quick Stats box: size, wingspan, weight, and lifespan data",SBU),
        Paragraph("•  A coloring guide identifying key plumage zones and suggested colors",SBU),
        Paragraph("•  Practical feeder tips for attracting the species to your garden",SBU),
        Paragraph("•  A full-page coloring illustration printed single-sided — "
            "so markers never bleed through",SBU),
        Paragraph("FOR WHOM",SH),
        Paragraph("Designed for adult colorists, bird watchers, nature lovers, educators, "
            "and families with older children. Works beautifully with colored pencils, "
            "watercolor pencils, and fine-tip markers.",SB),
        Paragraph("CONSERVATION",SH),
        Paragraph("Each species profile includes IUCN Red List status and population trend "
            "data from the North American Breeding Bird Survey, with practical steps "
            "readers can take to support declining species.",SB),
    ]

    frame_h = CH - BLEED - 1.25*inch - (BLEED + 2.45*inch)
    Frame(bx, BLEED + 2.45*inch, TRIM_W - 2*SAFE, frame_h,
          leftPadding=0, rightPadding=0, topPadding=0,
          bottomPadding=0, showBoundary=0).addFromList(desc, c)

    # ── SPECIES STRIP ─────────────────────────────────────────────────────────
    strip_y = BLEED + 1.55*inch
    c.setFillColor(G_MID)
    c.rect(0, strip_y, TRIM_W + BLEED, 0.72*inch, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(0, strip_y + 0.72*inch, TRIM_W + BLEED, strip_y + 0.72*inch)
    c.line(0, strip_y, TRIM_W + BLEED, strip_y)
    highlight = [
        "American Goldfinch","Northern Cardinal","Blue Jay","Ruby-throated Hummingbird",
        "Eastern Bluebird","Baltimore Oriole","Cedar Waxwing","American Kestrel",
    ]
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7)
    c.drawString(bx, strip_y + 0.50*inch, "FEATURING:")
    c.setFillColor(G_LIGHT); c.setFont("Helvetica",7.5)
    line1 = "  •  ".join(highlight[:4])
    line2 = "  •  ".join(highlight[4:])
    c.drawString(bx, strip_y + 0.36*inch, line1)
    c.drawString(bx, strip_y + 0.18*inch, line2 + "  •  and 32 more")

    # ── BARCODE PLACEHOLDER ───────────────────────────────────────────────────
    bc_w = 1.8*inch; bc_h = 1.1*inch
    bc_x = TRIM_W + BLEED - SAFE - bc_w
    bc_y = BLEED + 0.2*inch
    c.setFillColor(WHITE)
    c.roundRect(bc_x, bc_y, bc_w, bc_h, 3, fill=1, stroke=0)
    c.setFillColor(GREY); c.setFont("Helvetica",6.5)
    c.drawCentredString(bc_x + bc_w/2, bc_y + 0.38*inch, "ISBN / Barcode")
    c.drawCentredString(bc_x + bc_w/2, bc_y + 0.22*inch, "KDP will place barcode here")

    # Publisher line
    c.setFillColor(GREY); c.setFont("Helvetica",7.5)
    c.drawString(bx, BLEED + 0.28*inch, "Printed in the United States of America")
    c.drawString(bx, BLEED + 0.12*inch, "www.BackyardBirdsBook.com")


# ── Build PDF ────────────────────────────────────────────────────────────────
cv = canvas.Canvas(OUTPUT, pagesize=(CW, CH))

draw_back(cv)
draw_spine(cv)
draw_front(cv)

cv.showPage()
cv.save()

print(f"Done -> {OUTPUT}")
print(f"Canvas: {CW/inch:.4f} in × {CH/inch:.4f} in")
print(f"Spine : {SPINE/inch:.4f} in  ({168} pages × 0.002252)")
print(f"Trim  : {TRIM_W/inch:.1f} × {TRIM_H/inch:.1f} in  |  Bleed: {BLEED/inch:.3f} in")
