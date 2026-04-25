from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module07_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/07_downy_woodpecker.jpg"

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

S_TITLE = sp("T",  "Helvetica-Bold",   28, G_DARK, 34)
S_LAT   = sp("L",  "Helvetica-Oblique",11, GREY,   16, sa=6)
S_HDR   = sp("H",  "Helvetica-Bold",    9, G_MID,  13, sb=10, sa=3)
S_BODY  = sp("B",  "Helvetica",        10, DARK,   15, align=TA_JUSTIFY)
S_BUL   = sp("BU", "Helvetica",        10, DARK,   14, sb=1)

class GoldLine(Flowable):
    def __init__(self, w):
        super().__init__(); self.width=w; self.height=10
    def draw(self):
        c=self.canv; c.setStrokeColor(GOLD); c.setLineWidth(0.8)
        c.line(0,5,self.width,5); c.setFillColor(GOLD); m=self.width/2
        p=c.beginPath(); p.moveTo(m,10); p.lineTo(m+5,5); p.lineTo(m,0); p.lineTo(m-5,5); p.close()
        c.drawPath(p,fill=1,stroke=0)

def chrome(c, pnum, sub=""):
    c.setFillColor(G_DARK); c.rect(0,H-MT,W,MT,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,H-0.32*inch,"BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    if sub: c.drawRightString(W-MR,H-0.32*inch,sub)
    c.setFillColor(CREAM); c.rect(0,0,W,H-MT,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica",8)
    c.drawCentredString(W/2,0.16*inch,f"— {pnum} —")

def draw_stats(c, x, y, bw):
    stats=[("Length","5.5 – 6.7 in  (14 – 17 cm)"),
           ("Wingspan","9.8 – 11.8 in  (25 – 30 cm)"),
           ("Weight","0.7 – 1.0 oz  (20 – 33 g)"),
           ("Lifespan","Up to 11 years (avg. 1–2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c, x, y, bw):
    rows=[("Crown & back","Solid black"),
          ("Wing spots","Black with white dots/bars"),
          ("White back stripe","Pure white center stripe"),
          ("Underparts","White to pale buff"),
          ("Red nape patch (male)","Bright red — rear of crown only"),
          ("Bill","Short, dark gray, chisel-shaped")]
    rh=0.22*inch; hh=0.28*inch; bh=len(rows)*rh+hh
    c.setFillColor(G_DARK); c.rect(x,y-bh,bw,bh,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8)
    c.drawString(x+8,y-0.2*inch,"ZONE"); c.drawString(x+bw*0.5,y-0.2*inch,"RECOMMENDED COLOR")
    for i,(z,col) in enumerate(rows):
        ry=y-hh-(i+0.5)*rh
        bg=colors.HexColor("#1B4332") if i%2==0 else colors.HexColor("#163D2C")
        c.setFillColor(bg); c.rect(x,y-hh-i*rh-rh,bw,rh,fill=1,stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica",8.5); c.drawString(x+8,ry-3,z)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica-Oblique",8.5); c.drawString(x+bw*0.5,ry-3,col)
    c.setStrokeColor(GOLD); c.setLineWidth(0.5); c.rect(x,y-bh,bw,bh,fill=0,stroke=1)
    return bh

def page1(c):
    chrome(c, 19, "Module 07 of 40")
    content=[Table([[Paragraph("MODULE  07  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Downy Woodpecker",S_TITLE),
              Paragraph("Dryobates pubescens",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Downy Woodpecker is the smallest woodpecker in North America and one "
            "of the most familiar visitors to backyard feeders across the continent. Despite "
            "its diminutive size, it is a bold and active bird, clinging to suet cages, "
            "sunflower feeders, and tree trunks with equal ease. Its crisp black-and-white "
            "plumage and the male's bright red nape patch make it easy to identify. The "
            "Downy is often confused with the larger Hairy Woodpecker, but can be "
            "distinguished by its much shorter bill relative to head size and its smaller "
            "overall dimensions. It is one of the most widespread woodpeckers in "
            "North America and a year-round resident throughout its range.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Downy Woodpecker inhabits a remarkable range of forested and "
            "semi-open environments across North America, from Alaska and northern Canada "
            "south through most of the United States, absent only from the arid Southwest "
            "and parts of the Great Plains. It thrives in deciduous and mixed forests, "
            "orchards, riparian corridors, suburban parks, and gardens with mature trees. "
            "Unlike many woodpeckers, it readily adapts to fragmented and urban habitats "
            "and is a common year-round feeder visitor across most of its range.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Suet cakes — the single most effective food to offer",
              "Black-oil sunflower seeds and hulled chips",
              "Peanut butter (plain, no additives) smeared on bark",
              "Bark insects: beetle larvae, ants, moth cocoons",
              "Wild berries and plant galls in winter",
              "Poison ivy berries — an important winter food source"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c, 20, "Downy Woodpecker")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Downy Woodpeckers are active, acrobatic birds that forage across a "
            "wide variety of surfaces — tree trunks, large branches, weed stems, and "
            "even corn stalks. Their small size allows them to exploit foraging niches "
            "unavailable to larger woodpeckers, including the tips of small branches and "
            "slender plant stems where insect eggs and larvae overwinter. Outside breeding "
            "season, Downies frequently join mixed-species foraging flocks with chickadees, "
            "nuthatches, and kinglets, benefiting from the collective vigilance of the group. "
            "Males and females partition foraging habitat even within a territory: males "
            "tend to forage on smaller branches and weed stems, females on larger trunks.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Downy Woodpeckers excavate their own nest cavities in dead or dying "
            "trees, a process that takes both sexes 1–3 weeks to complete. The entrance "
            "hole is perfectly round, about 1.25 inches in diameter, leading to a gourd-"
            "shaped chamber 6–12 inches deep lined only with wood chips. No nest material "
            "is added. Clutches of 3–8 white eggs are incubated by both parents for "
            "12 days. The male incubates at night. Nestlings are fed by both parents "
            "and fledge at 20–25 days. Old nest cavities are vital for other cavity-"
            "nesting species including chickadees, bluebirds, and small owls.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Downy Woodpecker's primary call is a sharp, flat \"pik\" — shorter "
            "and higher-pitched than the similar Hairy Woodpecker's call. It also produces "
            "a descending whinny call used during territorial interactions and a rattling "
            "\"drum\" — a rapid series of bill strikes on a resonant dead branch — used "
            "to establish territory and attract mates. Drumming rates average about "
            "17 strikes per second. Both sexes drum, though males drum more frequently.",S_BODY),
        Paragraph("CONSERVATION STATUS",S_HDR)]
    tbl=Table([[Paragraph("IUCN Red List:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Least Concern",sp("x","Helvetica-Bold",9,G_LIGHT,13)),
                Paragraph("Population trend:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Stable",sp("x","Helvetica",9,G_LIGHT,13))]],
              colWidths=[CW*0.22,CW*0.28,CW*0.25,CW*0.25])
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8)]))
    content+=[tbl,Spacer(1,6),
        Paragraph("The Downy Woodpecker population is estimated at over 14 million "
            "individuals and remains stable across its range. It benefits from dead "
            "tree retention in managed forests and suburban areas. Its excavated nest "
            "cavities provide essential housing for dozens of other cavity-dependent "
            "species, making it a keystone species in many woodland ecosystems.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Suet cages are the most reliable way to attract Downy Woodpeckers",
              "Offer suet year-round — especially critical in cold winters",
              "Upside-down suet feeders deter starlings while Downies feed easily",
              "Hang feeders near tree trunks — Downies feel safer close to cover",
              "Leave dead trees standing when safe — essential for nesting and foraging"]:
        content.append(Paragraph(f"<bullet>•</bullet>  {t}",S_BUL))
    content.append(Paragraph("COLORING GUIDE",S_HDR))
    GUIDE_H=6*0.22*inch+0.28*inch; guide_y=MB+GUIDE_H+0.15*inch
    Frame(ML,guide_y+0.08*inch,CW,H-MT-(guide_y+0.08*inch)-0.12*inch,
          leftPadding=0,rightPadding=0,topPadding=0.1*inch,
          bottomPadding=0,showBoundary=0).addFromList(content,c)
    draw_color_guide(c,ML,guide_y,CW)

def page3(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    HDR_H=0.65*inch
    c.setFillColor(G_DARK); c.rect(0,H-HDR_H,W,HDR_H,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica-Bold",16)
    c.drawCentredString(W/2,H-0.38*inch,"COLOR ME!")
    c.setFillColor(G_LIGHT); c.setFont("Helvetica",9)
    c.drawCentredString(W/2,H-0.56*inch,"Downy Woodpecker  •  Dryobates pubescens  •  Module 07")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 21")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
