from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module01_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/01_northern_cardinal.jpg"

W, H = letter  # 8.5 x 11 in
ML, MR, MT, MB = 0.75*inch, 0.75*inch, 0.55*inch, 0.5*inch
CW = W - ML - MR  # content width

# ── Palette
G_DARK  = colors.HexColor("#1B4332")
G_MID   = colors.HexColor("#2D6A4F")
G_LIGHT = colors.HexColor("#B7E4C7")
GOLD    = colors.HexColor("#D4A017")
CREAM   = colors.HexColor("#FDFBF5")
CHALK   = colors.HexColor("#F0EDE6")
GREY    = colors.HexColor("#C8C4BB")
DARK    = colors.HexColor("#1E1E1E")

def sp(name, font, size, color=DARK, leading=None, align=TA_LEFT, sb=0, sa=0):
    return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color,
        leading=leading or size*1.45, alignment=align, spaceBefore=sb, spaceAfter=sa)

S_TITLE  = sp("T",  "Helvetica-Bold",   28, G_DARK,  34,  TA_LEFT)
S_LAT    = sp("L",  "Helvetica-Oblique",11, GREY,    16,  TA_LEFT, sa=6)
S_HDR    = sp("H",  "Helvetica-Bold",    9, G_MID,   13,  TA_LEFT, sb=10, sa=3)
S_BODY   = sp("B",  "Helvetica",        10, DARK,    15,  TA_JUSTIFY)
S_BULLET = sp("BU", "Helvetica",        10, DARK,    14,  TA_LEFT, sb=1)
S_FACT   = sp("F",  "Helvetica-Oblique",10, G_DARK,  15,  TA_JUSTIFY)
S_STAT_L = sp("SL", "Helvetica-Bold",    9, CREAM,   13,  TA_LEFT)
S_STAT_V = sp("SV", "Helvetica",         9, CREAM,   13,  TA_LEFT)

# ── Divider
class GoldLine(Flowable):
    def __init__(self, w):
        super().__init__(); self.width=w; self.height=10
    def draw(self):
        c=self.canv; c.setStrokeColor(GOLD); c.setLineWidth(0.8)
        c.line(0,5,self.width,5)
        c.setFillColor(GOLD)
        m=self.width/2
        p=c.beginPath(); p.moveTo(m,10); p.lineTo(m+5,5); p.lineTo(m,0); p.lineTo(m-5,5); p.close()
        c.drawPath(p,fill=1,stroke=0)

# ── Page header/footer
def page_chrome(c, page_num, subtitle=""):
    # top band
    c.setFillColor(G_DARK); c.rect(0, H-MT, W, MT, fill=1, stroke=0)
    c.setFillColor(GOLD);   c.setFont("Helvetica-Bold", 7.5)
    c.drawString(ML, H-0.32*inch, "BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM);  c.setFont("Helvetica", 7.5)
    if subtitle: c.drawRightString(W-MR, H-0.32*inch, subtitle)
    # cream background
    c.setFillColor(CREAM); c.rect(0,0,W,H-MT,fill=1,stroke=0)
    # bottom band
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    c.setFillColor(CREAM);  c.setFont("Helvetica",8)
    c.drawCentredString(W/2, 0.16*inch, f"— {page_num} —")

# ── Stats box (4 stats in 2 columns)
def draw_stats(c, x, y, bw):
    stats = [
        ("Length",   "8.3 – 9.3 in  (21 – 23.5 cm)"),
        ("Wingspan",  "9.8 – 12.2 in  (25 – 31 cm)"),
        ("Weight",    "1.5 – 1.7 oz  (42 – 48 g)"),
        ("Lifespan",  "Up to 15 years (avg. 3 in wild)"),
    ]
    row_h = 0.26*inch; bh = len(stats)*row_h + 0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8)
    c.drawString(x+8, y-0.22*inch, "QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry = y - 0.28*inch - (i+0.5)*row_h
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5)
        c.drawString(x+8, ry, lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5)
        c.drawString(x+bw*0.42, ry, val)
    return bh

# ── Color guide table
def draw_color_guide(c, x, y, bw):
    rows = [
        ("Male body",        "Vivid red — cadmium red"),
        ("Facial mask",      "Deep black"),
        ("Bill",             "Orange-coral"),
        ("Female body",      "Warm sandy brown"),
        ("Wings & crest ♀",  "Rusty-red highlights"),
        ("Eye",              "Dark brown, black ring"),
    ]
    rh=0.22*inch; hh=0.28*inch; bh=len(rows)*rh+hh
    c.setFillColor(G_DARK); c.rect(x,y-bh,bw,bh,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8)
    c.drawString(x+8,y-0.2*inch,"ZONE")
    c.drawString(x+bw*0.5,y-0.2*inch,"RECOMMENDED COLOR")
    for i,(z,col) in enumerate(rows):
        ry=y-hh-(i+0.5)*rh
        bg=colors.HexColor("#1B4332") if i%2==0 else colors.HexColor("#163D2C")
        c.setFillColor(bg); c.rect(x,y-hh-i*rh-rh,bw,rh,fill=1,stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica",8.5)
        c.drawString(x+8,ry-3,z)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica-Oblique",8.5)
        c.drawString(x+bw*0.5,ry-3,col)
    c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.rect(x,y-bh,bw,bh,fill=0,stroke=1)
    return bh

# ═══════════════════════════════════════════════════════════
# PAGE 1 — Info sheet part 1
# ═══════════════════════════════════════════════════════════
def page1(c):
    page_chrome(c, 1, "Module 01 of 40")

    frame_y = H - MT - 0.12*inch
    content = []

    # Module badge
    badge = Table([[Paragraph("MODULE  01  /  40", sp("m","Helvetica-Bold",8,G_DARK,11,TA_LEFT))]],
                  colWidths=[CW])
    badge.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),
    ]))
    content.append(badge)
    content.append(Spacer(1,8))
    content.append(Paragraph("Northern Cardinal", S_TITLE))
    content.append(Paragraph("Cardinalis cardinalis", S_LAT))
    content.append(GoldLine(CW))
    content.append(Spacer(1,6))

    # Stats box via frame, then drawn directly
    frame_h = H - MT - MB - 0.12*inch
    fr = Frame(ML, MB, CW, frame_h, leftPadding=0, rightPadding=0,
               topPadding=0.14*inch, bottomPadding=0, showBoundary=0)
    fr.addFromList(content, c)

    # Draw stats box below last flowable — approximate y position
    stats_y = H - MT - 0.14*inch - 1.52*inch  # after badge+title+lat+divider
    stats_h = draw_stats(c, ML, stats_y, CW)

    # Second frame for remaining text below stats
    content2 = []
    content2.append(Paragraph("PRESENTATION", S_HDR))
    content2.append(Paragraph(
        "The Northern Cardinal is one of the most iconic and instantly recognizable birds "
        "visiting North American gardens year-round. The brilliant scarlet male, with his "
        "dramatic crest and orange-red bill, is among the most photographed birds on the "
        "continent. The female, dressed in warm buff-brown with reddish tinges on her crest, "
        "wings and tail, is no less elegant. Both sexes remain on their territory throughout "
        "winter, bringing color and song to snow-covered gardens when most other species "
        "have migrated south.", S_BODY))

    content2.append(Paragraph("HABITAT & RANGE", S_HDR))
    content2.append(Paragraph(
        "The Northern Cardinal thrives across the eastern half of North America, from southern "
        "Maine and the Great Lakes south through Florida, and westward to the Great Plains of "
        "Texas and Oklahoma. Populations are also well-established in Arizona, New Mexico, "
        "and parts of California. Southern Ontario and Quebec host significant breeding "
        "populations. The species has expanded its range northward over the past century, "
        "likely aided by the proliferation of bird feeders and milder winters. It favors "
        "woodland edges, dense shrubby thickets, hedgerows, suburban gardens, and parks "
        "with mature trees and dense understory cover.", S_BODY))

    content2.append(Paragraph("DIET & FEEDING", S_HDR))
    foods = [
        "Black-oil sunflower seeds — the undisputed favorite",
        "Safflower seeds — especially attractive to cardinals",
        "White millet and cracked corn",
        "Wild berries: dogwood, holly, elderberry, sumac",
        "Insects and larvae (essential protein during breeding season)",
        "Fruit: grapes, mulberries, raspberries",
    ]
    for f in foods:
        content2.append(Paragraph(f"<bullet>•</bullet>  {f}", S_BULLET))

    fr2_y = stats_y - stats_h - 0.1*inch
    fr2_h = fr2_y - MB
    fr2 = Frame(ML, MB, CW, fr2_h, leftPadding=0, rightPadding=0,
                topPadding=0, bottomPadding=0, showBoundary=0)
    fr2.addFromList(content2, c)

# ═══════════════════════════════════════════════════════════
# PAGE 2 — Info sheet part 2
# ═══════════════════════════════════════════════════════════
def page2(c):
    page_chrome(c, 2, "Northern Cardinal")
    frame_h = H - MT - MB - 0.1*inch

    content = []
    content.append(Paragraph("BEHAVIOR & SOCIAL LIFE", S_HDR))
    content.append(Paragraph(
        "Cardinals are territorial songbirds that maintain year-round home ranges of roughly "
        "2–4 acres. Males fiercely defend their territory through song and, famously, by "
        "attacking their own reflection in windows — mistaking it for a rival. They are "
        "monogamous and pairs often remain together through multiple breeding seasons. "
        "Outside the breeding season, cardinals may gather in loose flocks of up to 70 "
        "individuals at abundant food sources. Males frequently feed females during courtship "
        "— a behavior called mate-feeding — passing seeds beak-to-beak.", S_BODY))

    content.append(Paragraph("NESTING & BREEDING", S_HDR))
    content.append(Paragraph(
        "Breeding season runs from March through September, with females typically raising "
        "2 to 4 broods per year — one of the highest rates among North American songbirds. "
        "The female constructs a cup-shaped nest over 3–9 days using twigs, bark strips, "
        "grasses and leaves, lined with fine grasses and hair. Nests are built 1–15 feet "
        "above ground in dense shrubs, vines or low trees. Each clutch contains 2–5 eggs "
        "(usually 3), pale whitish or greenish with brown speckles. Incubation lasts "
        "11–13 days, performed almost exclusively by the female. Nestlings fledge at "
        "9–11 days and the male takes over their care while the female begins a new nest.", S_BODY))

    content.append(Paragraph("SONG & COMMUNICATION", S_HDR))
    content.append(Paragraph(
        "The Northern Cardinal is renowned for its rich, loud whistled song — a series of "
        "clear slurred notes often described as \"cheer-cheer-cheer\" or \"birdy-birdy-birdy.\" "
        "Both males and females sing, which is unusual among North American songbirds. "
        "The female often sings from the nest, possibly communicating food needs to her mate. "
        "Cardinals have a repertoire of 16 or more distinct song patterns. Their sharp metallic "
        "\"chip\" call is an alarm note used to warn of predators. Song peaks in late winter "
        "and early spring as males establish territories.", S_BODY))

    content.append(Paragraph("CONSERVATION STATUS", S_HDR))
    tbl = Table([[
        Paragraph("IUCN Red List:", sp("x","Helvetica-Bold",9,CREAM,13)),
        Paragraph("Least Concern", sp("x","Helvetica-Bold",9,G_LIGHT,13)),
        Paragraph("Population trend:", sp("x","Helvetica-Bold",9,CREAM,13)),
        Paragraph("Stable / Increasing", sp("x","Helvetica",9,G_LIGHT,13)),
    ]], colWidths=[CW*0.22, CW*0.28, CW*0.25, CW*0.25])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),G_DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8),
    ]))
    content.append(tbl)
    content.append(Spacer(1,6))
    content.append(Paragraph(
        "With an estimated population of over 100 million individuals, the Northern Cardinal "
        "is one of the most abundant songbirds in North America. Its range has expanded "
        "northward significantly since the 1900s. It is the official state bird of 7 US states "
        "— more than any other species.", S_BODY))

    content.append(Paragraph("FEEDER TIPS", S_HDR))
    tips = [
        "Best feeder type: hopper feeder or large platform feeder",
        "Preferred seeds: safflower (squirrels tend to avoid it) and black-oil sunflower",
        "Cardinals feed most actively at dawn and dusk",
        "Place feeders near dense shrubs — cardinals prefer cover close by",
        "Offer a shallow birdbath: cardinals bathe and drink regularly",
    ]
    for t in tips:
        content.append(Paragraph(f"<bullet>•</bullet>  {t}", S_BULLET))

    content.append(Paragraph("DID YOU KNOW?", S_HDR))
    fact_data = [[Paragraph(
        "The Northern Cardinal is the official state bird of Illinois, Indiana, Kentucky, "
        "North Carolina, Ohio, Virginia, and West Virginia — seven states in total, more "
        "than any other bird species. Its brilliant red plumage inspired the name of the "
        "St. Louis Cardinals baseball team and numerous other sports franchises across "
        "the eastern United States.", S_FACT)]]
    fact_tbl = Table(fact_data, colWidths=[CW])
    fact_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("BOX",(0,0),(-1,-1),0.5,G_MID),
    ]))
    content.append(fact_tbl)
    content.append(Spacer(1,8))
    content.append(Paragraph("COLORING GUIDE", S_HDR))

    fr = Frame(ML, MB+1.35*inch, CW, frame_h - 1.4*inch,
               leftPadding=0, rightPadding=0, topPadding=0.1*inch,
               bottomPadding=0, showBoundary=0)
    fr.addFromList(content, c)

    # Color guide at bottom
    guide_y = MB + 1.35*inch
    draw_color_guide(c, ML, guide_y, CW)

# ═══════════════════════════════════════════════════════════
# PAGE 3 — Full-page coloring illustration
# ═══════════════════════════════════════════════════════════
def page3(c):
    # cream background
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    # top header
    HDR_H = 0.65*inch
    c.setFillColor(G_DARK); c.rect(0,H-HDR_H,W,HDR_H,fill=1,stroke=0)
    c.setFillColor(CREAM);  c.setFont("Helvetica-Bold",16)
    c.drawCentredString(W/2, H-0.38*inch, "COLOR ME!")
    c.setFillColor(G_LIGHT); c.setFont("Helvetica",9)
    c.drawCentredString(W/2, H-0.56*inch, "Northern Cardinal  •  Cardinalis cardinalis  •  Module 01")
    # bottom footer
    FTR_H = 0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD);   c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML, 0.16*inch, "Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM);  c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR, 0.16*inch, "Page 3")
    # image — max available space
    pad = 0.18*inch
    img_x = ML - pad
    img_y = FTR_H + pad
    img_w = W - 2*(ML - pad)
    img_h = H - HDR_H - FTR_H - 2*pad
    c.drawImage(IMG_PATH, img_x, img_y, width=img_w, height=img_h,
                preserveAspectRatio=True, mask="auto")

# ═══════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════
cv = canvas.Canvas(OUTPUT, pagesize=letter)

page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()

cv.save()
print(f"Done → {OUTPUT}")
