from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import os

# ── Constants ────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter          # 8.5 × 11 inches
MARGIN_INNER   = 1.0 * inch      # gutter (binding side)
MARGIN_OUTER   = 0.75 * inch
MARGIN_TOP     = 0.85 * inch
MARGIN_BOTTOM  = 0.85 * inch

OUTPUT  = "/home/user/Ebook/ebook_preview.pdf"
IMG_PATH = "/root/.claude/uploads/782ba508-385c-43fd-9a35-6bed394dd631/019dbe00-1000007733.png"

# ── Palette ──────────────────────────────────────────────────────────────────
GREEN_DARK   = colors.HexColor("#1B4332")
GREEN_MID    = colors.HexColor("#2D6A4F")
GREEN_LIGHT  = colors.HexColor("#B7E4C7")
GOLD         = colors.HexColor("#D4A017")
CREAM        = colors.HexColor("#FDFBF5")
CHARCOAL     = colors.HexColor("#2C2C2C")
GREY_LIGHT   = colors.HexColor("#F0EDE6")
GREY_MID     = colors.HexColor("#C8C4BB")

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def make_style(name, font, size, color=CHARCOAL, leading=None,
               align=TA_LEFT, space_before=0, space_after=0, bold=False):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        textColor=color,
        leading=leading or size * 1.4,
        alignment=align,
        spaceBefore=space_before,
        spaceAfter=space_after,
    )

S_COVER_TITLE = make_style("CoverTitle", "Helvetica-Bold", 34,
                            color=CREAM, align=TA_CENTER, leading=42)
S_COVER_SUB   = make_style("CoverSub", "Helvetica", 15,
                            color=GREEN_LIGHT, align=TA_CENTER, leading=22)
S_COVER_TAG   = make_style("CoverTag", "Helvetica-Oblique", 12,
                            color=GOLD, align=TA_CENTER)

S_BIRD_NAME   = make_style("BirdName", "Helvetica-Bold", 26,
                            color=GREEN_DARK, leading=30, space_after=2)
S_BIRD_EN     = make_style("BirdEN", "Helvetica-Oblique", 14,
                            color=GREEN_MID, leading=18, space_after=2)
S_BIRD_LAT    = make_style("BirdLat", "Helvetica-Oblique", 11,
                            color=GREY_MID, leading=15, space_after=10)

S_SECTION_HDR = make_style("SecHdr", "Helvetica-Bold", 10,
                            color=GREEN_MID, leading=13, space_before=10, space_after=3)
S_BODY        = make_style("Body", "Helvetica", 10,
                            color=CHARCOAL, leading=15, align=TA_JUSTIFY)
S_BULLET      = make_style("Bullet", "Helvetica", 10,
                            color=CHARCOAL, leading=14, space_before=1)
S_FACT        = make_style("Fact", "Helvetica-Oblique", 10,
                            color=GREEN_DARK, leading=15, align=TA_JUSTIFY)
S_PAGE_TITLE  = make_style("PageTitle", "Helvetica-Bold", 13,
                            color=CREAM, align=TA_CENTER, leading=16)
S_COLORING_HINT = make_style("ColorHint", "Helvetica-Oblique", 9,
                              color=GREY_MID, align=TA_CENTER)
S_MODULE_NUM  = make_style("ModNum", "Helvetica-Bold", 9,
                            color=GOLD, leading=12)

# ── Custom Flowables ──────────────────────────────────────────────────────────
class ColoredRect(Flowable):
    """Full-width colored horizontal band."""
    def __init__(self, width, height, fill_color, radius=4):
        super().__init__()
        self.width  = width
        self.height = height
        self.fill_color = fill_color
        self.radius = radius

    def draw(self):
        self.canv.setFillColor(self.fill_color)
        self.canv.roundRect(0, 0, self.width, self.height,
                            self.radius, fill=1, stroke=0)


class GoldDivider(Flowable):
    """Thin gold rule with small leaf ornament."""
    def __init__(self, width):
        super().__init__()
        self.width  = width
        self.height = 8

    def draw(self):
        c = self.canv
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(0, 4, self.width, 4)
        # small diamond centre
        c.setFillColor(GOLD)
        mid = self.width / 2
        p = c.beginPath()
        p.moveTo(mid, 8)
        p.lineTo(mid + 5, 4)
        p.lineTo(mid, 0)
        p.lineTo(mid - 5, 4)
        p.close()
        c.drawPath(p, fill=1, stroke=0)


class ColorGuideTable(Flowable):
    """Compact two-column colour guide."""
    ROWS = [
        ("Body (male)",        "Vivid red — cadmium red"),
        ("Facial mask",        "Deep black"),
        ("Bill",               "Orange-coral"),
        ("Body (female)",      "Warm sandy brown"),
        ("Wings & crest (f.)", "Rusty red highlights"),
        ("Eye",                "Dark brown, black ring"),
    ]

    def __init__(self, width):
        super().__init__()
        self.width  = width
        self.height = len(self.ROWS) * 16 + 22

    def draw(self):
        c   = self.canv
        col = self.width
        row_h = 16
        hdr_h = 22

        # header
        c.setFillColor(GREEN_DARK)
        c.rect(0, self.height - hdr_h, col, hdr_h, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(6, self.height - hdr_h + 7, "ZONE")
        c.drawString(col * 0.52, self.height - hdr_h + 7, "RECOMMENDED COLOR")

        for i, (zone, color_txt) in enumerate(self.ROWS):
            y = self.height - hdr_h - (i + 1) * row_h
            bg = GREY_LIGHT if i % 2 == 0 else colors.white
            c.setFillColor(bg)
            c.rect(0, y, col, row_h, fill=1, stroke=0)
            c.setFillColor(CHARCOAL)
            c.setFont("Helvetica", 8.5)
            c.drawString(6, y + 4, zone)
            c.setFont("Helvetica-Oblique", 8.5)
            c.drawString(col * 0.52, y + 4, color_txt)

        # border
        c.setStrokeColor(GREY_MID)
        c.setLineWidth(0.5)
        c.rect(0, 0, col, self.height, fill=0, stroke=1)


# ── Cover page (drawn directly on canvas) ────────────────────────────────────
def draw_cover(canvas_obj, doc):
    c = canvas_obj
    w, h = PAGE_W, PAGE_H

    # dark green background
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # decorative top band
    c.setFillColor(GREEN_MID)
    c.rect(0, h - 1.6 * inch, w, 1.6 * inch, fill=1, stroke=0)

    # gold top rule
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(0.6 * inch, h - 1.65 * inch, w - 0.6 * inch, h - 1.65 * inch)

    # series label
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(w / 2, h - 0.55 * inch, "GARDEN BIRDS OF NORTH AMERICA  •  VOLUME 1")

    # main title
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(w / 2, h - 2.45 * inch, "COLOR & DISCOVER")

    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(GREEN_LIGHT)
    c.drawCentredString(w / 2, h - 3.05 * inch, "Garden Birds of North America")

    # gold rule below title
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(1.5 * inch, h - 3.35 * inch, w - 1.5 * inch, h - 3.35 * inch)

    # cardinal image centered
    img_w = 4.8 * inch
    img_h = 4.2 * inch
    img_x = (w - img_w) / 2
    img_y = h - 3.45 * inch - img_h

    # white card behind image
    pad = 0.18 * inch
    c.setFillColor(colors.white)
    c.roundRect(img_x - pad, img_y - pad,
                img_w + 2 * pad, img_h + 2 * pad, 8, fill=1, stroke=0)
    c.drawImage(IMG_PATH, img_x, img_y, width=img_w, height=img_h,
                preserveAspectRatio=True, mask='auto')

    # subtitle / tagline
    c.setFillColor(GREEN_LIGHT)
    c.setFont("Helvetica-Oblique", 13)
    c.drawCentredString(w / 2, img_y - 0.55 * inch,
                        "40 Species  •  Color  •  Learn  •  Explore")

    # gold bottom rule
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(0.6 * inch, 1.0 * inch, w - 0.6 * inch, 1.0 * inch)

    # ages tag
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(w / 2, 0.62 * inch, "FOR ALL AGES  •  EDUCATIONAL  •  FUN")


# ── Fact-sheet page builder ───────────────────────────────────────────────────
def build_fact_sheet(content_w):
    """Return list of flowables for the Cardinal fact-sheet page."""
    elems = []

    # ── Module badge ──
    badge_data = [[ Paragraph("MODULE  01", S_MODULE_NUM) ]]
    badge = Table(badge_data, colWidths=[content_w])
    badge.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), GREEN_LIGHT),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [4, 4, 4, 4]),
    ]))
    elems.append(badge)
    elems.append(Spacer(1, 8))

    # ── Bird names ──
    elems.append(Paragraph("Cardinal rouge", S_BIRD_NAME))
    elems.append(Paragraph("Northern Cardinal", S_BIRD_EN))
    elems.append(Paragraph("Cardinalis cardinalis", S_BIRD_LAT))
    elems.append(GoldDivider(content_w))
    elems.append(Spacer(1, 8))

    # ── Presentation ──
    elems.append(Paragraph("PRESENTATION", S_SECTION_HDR))
    elems.append(Paragraph(
        "The Northern Cardinal is one of the most recognizable visitors to gardens "
        "across eastern North America. The brilliant scarlet male and the warm "
        "brown female with red highlights are year-round residents, never migrating "
        "south for winter. Uniquely among North American songbirds, the female also "
        "sings — often communicating with her mate from the nest.",
        S_BODY))
    elems.append(Spacer(1, 8))

    # ── Diet ──
    elems.append(Paragraph("FAVORITE FEEDER FOODS", S_SECTION_HDR))
    foods = [
        "Black-oil sunflower seeds",
        "Safflower seeds",
        "White millet",
        "Wild berries (dogwood, holly)",
        "Insects during breeding season",
    ]
    for f in foods:
        elems.append(Paragraph(f"<bullet>•</bullet>  {f}", S_BULLET))
    elems.append(Spacer(1, 8))

    # ── Habitat ──
    elems.append(Paragraph("HABITAT & RANGE", S_SECTION_HDR))
    elems.append(Paragraph(
        "Found year-round from Maine south to Florida and west to the Great Plains. "
        "Also established in Texas, Arizona, and southern Ontario & Quebec. Prefers "
        "woodland edges, shrubby gardens, hedgerows, and parks with dense cover.",
        S_BODY))
    elems.append(Spacer(1, 8))

    # ── Did you know ──
    elems.append(Paragraph("DID YOU KNOW?", S_SECTION_HDR))
    fact_box_data = [[
        Paragraph(
            "“The female Northern Cardinal is one of the few female songbirds "
            "in North America that sings. She often calls to her mate from the nest, "
            "sometimes even while incubating eggs.”",
            S_FACT)
    ]]
    fact_box = Table(fact_box_data, colWidths=[content_w])
    fact_box.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), GREEN_LIGHT),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("BOX",          (0, 0), (-1, -1), 0.5, GREEN_MID),
    ]))
    elems.append(fact_box)
    elems.append(Spacer(1, 10))

    # ── Color guide ──
    elems.append(Paragraph("COLORING GUIDE", S_SECTION_HDR))
    elems.append(ColorGuideTable(content_w))

    return elems


# ── Coloring page builder ─────────────────────────────────────────────────────
def build_coloring_page(canvas_obj, doc):
    """Drawn directly — full-page coloring layout."""
    c   = canvas_obj
    w, h = PAGE_W, PAGE_H

    # pale cream background
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # top header band
    c.setFillColor(GREEN_DARK)
    c.rect(0, h - 0.85 * inch, w, 0.85 * inch, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(w / 2, h - 0.52 * inch, "COLOR ME!")
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, h - 0.73 * inch,
                        "Northern Cardinal  •  Cardinalis cardinalis")

    # bottom footer band
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, w, 0.6 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.5 * inch, 0.22 * inch,
                 "Color & Discover: Garden Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 8)
    c.drawRightString(w - 0.5 * inch, 0.22 * inch, "Module 01  |  Page 2")

    # image area — centered with white card
    img_w = 5.8 * inch
    img_h = 5.8 * inch
    img_x = (w - img_w) / 2
    img_y = (h - img_h) / 2 - 0.1 * inch

    pad = 0.22 * inch
    c.setFillColor(colors.white)
    c.setStrokeColor(GREY_MID)
    c.setLineWidth(0.5)
    c.roundRect(img_x - pad, img_y - pad,
                img_w + 2 * pad, img_h + 2 * pad, 10, fill=1, stroke=1)

    c.drawImage(IMG_PATH, img_x, img_y, width=img_w, height=img_h,
                preserveAspectRatio=True, mask='auto')

    # hint below image
    c.setFillColor(GREY_MID)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(w / 2, img_y - 0.28 * inch,
                        "Use the Color Guide on the facing page for realistic coloring.")


# ── Page templates ────────────────────────────────────────────────────────────
class EbookCanvas(canvas.Canvas):
    """Adds running header/footer to non-cover, non-coloring pages."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._page_num = 0

    def showPage(self):
        self._page_num += 1
        super().showPage()

    def save(self):
        super().save()


def add_page_frame(canvas_obj, doc):
    """Header + footer for fact-sheet pages."""
    c   = canvas_obj
    w, h = PAGE_W, PAGE_H
    pn  = doc.page

    if pn <= 1:   # cover — no header/footer
        return

    # pale cream background
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # top thin green rule
    c.setFillColor(GREEN_DARK)
    c.rect(0, h - 0.45 * inch, w, 0.45 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN_INNER, h - 0.28 * inch,
                 "COLOR & DISCOVER: GARDEN BIRDS OF NORTH AMERICA")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 8)
    c.drawRightString(w - MARGIN_OUTER, h - 0.28 * inch, f"Module 01")

    # bottom footer
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, w, 0.45 * inch, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, 0.16 * inch, f"— {pn} —")


# ── Build PDF ─────────────────────────────────────────────────────────────────
def build_pdf():
    content_w = PAGE_W - MARGIN_INNER - MARGIN_OUTER

    # We'll build pages manually using canvas for precise control
    c = canvas.Canvas(OUTPUT, pagesize=letter)

    # ── Page 1: Cover ──────────────────────────────────────────────────────
    draw_cover(c, None)
    c.showPage()

    # ── Page 2: Fact sheet ─────────────────────────────────────────────────
    # background + header/footer
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # top band
    c.setFillColor(GREEN_DARK)
    c.rect(0, PAGE_H - 0.5 * inch, PAGE_W, 0.5 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN_INNER, PAGE_H - 0.31 * inch,
                 "COLOR & DISCOVER: GARDEN BIRDS OF NORTH AMERICA")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 8)
    c.drawRightString(PAGE_W - MARGIN_OUTER, PAGE_H - 0.31 * inch, "Vol. 1")

    # bottom band
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, PAGE_W, 0.5 * inch, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 0.17 * inch, "— 2 —")

    # ── Fact sheet content via platypus on this canvas ──
    # We draw flowables manually onto canvas at fixed position
    from reportlab.platypus import Frame
    frame = Frame(
        MARGIN_INNER,
        0.6 * inch,
        content_w,
        PAGE_H - 0.5 * inch - 0.6 * inch - 0.1 * inch,
        leftPadding=0, rightPadding=0,
        topPadding=0.15 * inch, bottomPadding=0,
        showBoundary=0
    )
    story = build_fact_sheet(content_w)
    frame.addFromList(story, c)
    c.showPage()

    # ── Page 3: Coloring page ──────────────────────────────────────────────
    build_coloring_page(c, None)
    c.showPage()

    c.save()
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
