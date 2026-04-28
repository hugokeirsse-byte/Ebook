"""
KDP full-wrap cover assembly using the provided front and back cover images.

Layout (left → right):
  [BLEED][←── BACK COVER (8.5 in) ──→][←SPINE (0.420 in)→][←── FRONT COVER (8.5 in) ──→][BLEED]

Total canvas: 17.670 × 11.25 in  (with 0.125 in bleed on all sides)
Spine: 168 pages × 0.0025 in/page (cream 60# paper) = 0.420 in
"""
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT     = "/home/user/Ebook/cover_kdp.pdf"
FRONT_IMG  = "/home/user/Ebook/images/cover_front.png"
BACK_IMG   = "/home/user/Ebook/images/cover_back.png"

# Register Liberation Sans TTF — metrically identical to Helvetica, fully embedded
pdfmetrics.registerFont(TTFont("LibSans-Bold",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibSans",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))

BLEED  = 0.125 * inch
SPINE  = 0.420 * inch
TRIM_W = 8.5   * inch
TRIM_H = 11.0  * inch

CW = 2*BLEED + 2*TRIM_W + SPINE
CH = 2*BLEED + TRIM_H

X_SPINE_LEFT  = BLEED + TRIM_W
X_FRONT_LEFT  = X_SPINE_LEFT + SPINE

G_DARK = colors.HexColor("#1B4332")
GOLD   = colors.HexColor("#D4A017")
CREAM  = colors.HexColor("#FDFBF5")

cv = canvas.Canvas(OUTPUT, pagesize=(CW, CH))

# ── BACK COVER ───────────────────────────────────────────────────────────────
back_w = BLEED + TRIM_W
cv.drawImage(BACK_IMG, 0, 0, width=back_w, height=CH,
             preserveAspectRatio=False, mask="auto")

# ── FRONT COVER ──────────────────────────────────────────────────────────────
front_w = TRIM_W + BLEED
cv.drawImage(FRONT_IMG, X_FRONT_LEFT, 0, width=front_w, height=CH,
             preserveAspectRatio=False, mask="auto")

# ── SPINE ────────────────────────────────────────────────────────────────────
cv.setFillColor(G_DARK)
cv.rect(X_SPINE_LEFT, 0, SPINE, CH, fill=1, stroke=0)

# Gold border lines on spine edges
cv.setStrokeColor(GOLD); cv.setLineWidth(0.6)
cv.line(X_SPINE_LEFT, 0, X_SPINE_LEFT, CH)
cv.line(X_SPINE_LEFT + SPINE, 0, X_SPINE_LEFT + SPINE, CH)

# Spine text — rotated 90° (reads bottom to top), embedded TTF fonts
spine_cx = X_SPINE_LEFT + SPINE / 2
spine_cy = CH / 2
cv.saveState()
cv.translate(spine_cx, spine_cy)
cv.rotate(90)
cv.setFillColor(CREAM); cv.setFont("LibSans-Bold", 8.5)
cv.drawCentredString(0, 4, "BACKYARD BIRDS OF NORTH AMERICA")
cv.setFillColor(GOLD); cv.setFont("LibSans-Bold", 7.5)
cv.drawCentredString(0, -9, "VOL. 1")
cv.restoreState()

cv.showPage()
cv.save()

print(f"Done -> {OUTPUT}")
print(f"Canvas : {CW/inch:.4f} × {CH/inch:.4f} in")
print(f"Spine  : {SPINE/inch:.4f} in")
print(f"Bleed  : {BLEED/inch:.4f} in")
