from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module02_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/02_blackcapped_chickadee.jpg"

W, H = letter
ML, MR, MT, MB = 0.75*inch, 0.75*inch, 0.55*inch, 0.5*inch
CW = W - ML - MR

G_DARK  = colors.HexColor("#1B4332")
G_MID   = colors.HexColor("#2D6A4F")
G_LIGHT = colors.HexColor("#B7E4C7")
GOLD    = colors.HexColor("#D4A017")
CREAM   = colors.HexColor("#FDFBF5")
GREY    = colors.HexColor("#C8C4BB")
DARK    = colors.HexColor("#1E1E1E")

def sp(name, font, size, color=DARK, leading=None, align=TA_LEFT, sb=0, sa=0):
    return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color,
        leading=leading or size*1.45, alignment=align, spaceBefore=sb, spaceAfter=sa)

S_TITLE = sp("T",  "Helvetica-Bold",   28, G_DARK,  34)
S_LAT   = sp("L",  "Helvetica-Oblique",11, GREY,    16, sa=6)
S_HDR   = sp("H",  "Helvetica-Bold",    9, G_MID,   13, sb=10, sa=3)
S_BODY  = sp("B",  "Helvetica",        10, DARK,    15, align=TA_JUSTIFY)
S_BUL   = sp("BU", "Helvetica",        10, DARK,    14, sb=1)
S_FACT  = sp("F",  "Helvetica-Oblique",10, G_DARK,  15, align=TA_JUSTIFY)

class GoldLine(Flowable):
    def __init__(self, w):
        super().__init__(); self.width=w; self.height=10
    def draw(self):
        c=self.canv; c.setStrokeColor(GOLD); c.setLineWidth(0.8)
        c.line(0,5,self.width,5)
        c.setFillColor(GOLD); m=self.width/2
        p=c.beginPath(); p.moveTo(m,10); p.lineTo(m+5,5); p.lineTo(m,0); p.lineTo(m-5,5); p.close()
        c.drawPath(p,fill=1,stroke=0)

def page_chrome(c, page_num, subtitle=""):
    c.setFillColor(G_DARK); c.rect(0,H-MT,W,MT,fill=1,stroke=0)
    c.setFillColor(GOLD);   c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,H-0.32*inch,"BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM);  c.setFont("Helvetica",7.5)
    if subtitle: c.drawRightString(W-MR,H-0.32*inch,subtitle)
    c.setFillColor(CREAM); c.rect(0,0,W,H-MT,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    c.setFillColor(CREAM);  c.setFont("Helvetica",8)
    c.drawCentredString(W/2,0.16*inch,f"— {page_num} —")

def draw_stats(c, x, y, bw):
    stats = [
        ("Length",   "4.7 – 5.9 in  (12 – 15 cm)"),
        ("Wingspan",  "6.3 – 8.3 in  (16 – 21 cm)"),
        ("Weight",    "0.3 – 0.5 oz  (9 – 14 g)"),
        ("Lifespan",  "Up to 12 years (avg. 2–3 in wild)"),
    ]
    row_h=0.26*inch; bh=len(stats)*row_h+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8)
    c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*row_h
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5)
        c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5)
        c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c, x, y, bw):
    rows = [
        ("Crown & bib",    "Deep black"),
        ("Cheek patches",  "Pure white"),
        ("Back & wings",   "Slate gray"),
        ("Belly",          "White to pale gray"),
        ("Flanks",         "Buffy-white"),
        ("Bill",           "Short, black"),
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

def page1(c):
    page_chrome(c, 4, "Module 02 of 40")
    content = []
    badge = Table([[Paragraph("MODULE  02  /  40", sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])
    badge.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content += [badge, Spacer(1,8),
                Paragraph("Black-capped Chickadee", S_TITLE),
                Paragraph("Poecile atricapillus", S_LAT),
                GoldLine(CW), Spacer(1,6)]
    fr = Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,topPadding=0.14*inch,bottomPadding=0,showBoundary=0)
    fr.addFromList(content, c)
    stats_y = H-MT-0.14*inch-1.52*inch
    stats_h = draw_stats(c, ML, stats_y, CW)
    content2 = []
    content2.append(Paragraph("PRESENTATION", S_HDR))
    content2.append(Paragraph(
        "The Black-capped Chickadee is one of the most beloved and recognizable backyard birds "
        "across northern North America. Bold, curious, and remarkably tolerant of humans, it is "
        "often the first species to discover a newly installed feeder. Its cheerful "
        "\"chick-a-dee-dee-dee\" call is one of the most familiar sounds of North American "
        "winters. Despite its tiny size, the chickadee is supremely adapted to cold climates, "
        "capable of surviving temperatures well below freezing through a combination of "
        "extraordinary memory, metabolic flexibility, and dense winter plumage.", S_BODY))
    content2.append(Paragraph("HABITAT & RANGE", S_HDR))
    content2.append(Paragraph(
        "The Black-capped Chickadee occupies a vast range across the northern tier of North "
        "America, from Alaska and the Yukon east to Newfoundland and Nova Scotia, and south "
        "through the northern United States including New England, the Great Lakes region, "
        "and the Rocky Mountain states down to northern New Mexico. It inhabits deciduous and "
        "mixed forests, forest edges, riparian corridors, suburban parks, and wooded gardens. "
        "It is a permanent resident throughout its range and does not migrate, relying instead "
        "on cached food and physiological adaptations to endure harsh winters.", S_BODY))
    content2.append(Paragraph("DIET & FEEDING", S_HDR))
    for f in ["Black-oil sunflower seeds — the top choice at any feeder",
              "Suet cakes — critical high-energy winter food source",
              "Nyjer (thistle) seed and hulled sunflower chips",
              "Peanut pieces and peanut butter mixtures",
              "Mealworms (live or dried) during breeding season",
              "Wild: insects, insect eggs, spiders, berries, seeds"]:
        content2.append(Paragraph(f"<bullet>•</bullet>  {f}", S_BUL))
    fr2_y = stats_y-stats_h-0.1*inch
    fr2 = Frame(ML,MB,CW,fr2_y-MB,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,showBoundary=0)
    fr2.addFromList(content2, c)

def page2(c):
    page_chrome(c, 5, "Black-capped Chickadee")
    content = []
    content.append(Paragraph("BEHAVIOR & SOCIAL LIFE", S_HDR))
    content.append(Paragraph(
        "Chickadees are highly social birds that form stable winter flocks of 6–12 individuals "
        "with a clear dominance hierarchy. These flocks often serve as the nucleus for mixed-"
        "species foraging groups, attracting nuthatches, woodpeckers, and warblers. Within the "
        "flock, dominant birds feed first and claim the best roost sites. The chickadee's "
        "\"chick-a-dee\" alarm call is remarkably sophisticated: the number of \"dee\" notes "
        "appended to the call signals the level of threat, with more notes indicating a more "
        "dangerous predator nearby. Researchers have identified it as one of the most complex "
        "vocalizations in the animal kingdom.", S_BODY))
    content.append(Paragraph("NESTING & BREEDING", S_HDR))
    content.append(Paragraph(
        "Breeding pairs form in late winter as flocks begin to break up. Chickadees are "
        "cavity nesters, excavating their own nest holes in soft rotting wood or using "
        "natural cavities and nest boxes. The female lines the cavity with moss, plant fibers, "
        "fur, and feathers, creating a deep insulating cup. Clutches typically contain 6–8 "
        "white eggs with reddish-brown speckles. Incubation lasts 12–13 days, performed by "
        "the female alone while the male brings her food. Both parents feed the nestlings, "
        "which fledge at 16 days. Pairs raise one brood per year.", S_BODY))
    content.append(Paragraph("SONG & COMMUNICATION", S_HDR))
    content.append(Paragraph(
        "The chickadee has two primary vocalizations. Its contact and alarm call — the iconic "
        "\"chick-a-dee-dee-dee\" — varies in complexity based on context and threat level. "
        "Its territorial song is a clear, whistled two-note \"fee-bee\" (or \"fee-bee-bee\"), "
        "the first note higher than the second, heard most often on mild late-winter days as "
        "males begin to establish breeding territories. Chickadees also produce a variety of "
        "soft gargling calls within their flocks.", S_BODY))
    content.append(Paragraph("CONSERVATION STATUS", S_HDR))
    tbl = Table([[
        Paragraph("IUCN Red List:", sp("x","Helvetica-Bold",9,CREAM,13)),
        Paragraph("Least Concern", sp("x","Helvetica-Bold",9,G_LIGHT,13)),
        Paragraph("Population trend:", sp("x","Helvetica-Bold",9,CREAM,13)),
        Paragraph("Stable", sp("x","Helvetica",9,G_LIGHT,13)),
    ]], colWidths=[CW*0.22,CW*0.28,CW*0.25,CW*0.25])
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),8)]))
    content += [tbl, Spacer(1,6)]
    content.append(Paragraph(
        "The Black-capped Chickadee remains abundant across its vast range, with an estimated "
        "population exceeding 100 million individuals. It adapts well to suburban and urban "
        "environments and benefits from nest box programs and winter feeding.", S_BODY))
    content.append(Paragraph("FEEDER TIPS", S_HDR))
    for t in ["Tube feeders or small hopper feeders work best",
              "Black-oil sunflower seeds are strongly preferred over striped",
              "Chickadees can be hand-tamed with patience over several weeks",
              "Place a nest box (1 1/8\" hole diameter) near woodland edge",
              "Suet feeders are especially valued from October through March"]:
        content.append(Paragraph(f"<bullet>•</bullet>  {t}", S_BUL))
    content.append(Paragraph("COLORING GUIDE", S_HDR))

    GUIDE_H = 6*0.22*inch+0.28*inch
    guide_y = MB+GUIDE_H+0.15*inch
    fr = Frame(ML, guide_y+0.08*inch, CW,
               H-MT-(guide_y+0.08*inch)-0.12*inch,
               leftPadding=0,rightPadding=0,topPadding=0.1*inch,bottomPadding=0,showBoundary=0)
    fr.addFromList(content, c)
    draw_color_guide(c, ML, guide_y, CW)

def page3(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    HDR_H=0.65*inch
    c.setFillColor(G_DARK); c.rect(0,H-HDR_H,W,HDR_H,fill=1,stroke=0)
    c.setFillColor(CREAM);  c.setFont("Helvetica-Bold",16)
    c.drawCentredString(W/2,H-0.38*inch,"COLOR ME!")
    c.setFillColor(G_LIGHT); c.setFont("Helvetica",9)
    c.drawCentredString(W/2,H-0.56*inch,"Black-capped Chickadee  •  Poecile atricapillus  •  Module 02")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD);   c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM);  c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 6")
    pad=0.18*inch
    c.drawImage(IMG_PATH, ML-pad, FTR_H+pad,
                width=W-2*(ML-pad), height=H-HDR_H-FTR_H-2*pad,
                preserveAspectRatio=True, mask="auto")

cv = canvas.Canvas(OUTPUT, pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
