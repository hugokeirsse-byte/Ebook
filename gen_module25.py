from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module25_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/25_rosebreasted_grosbeak.jpg"

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

def sp(name,font,size,color=DARK,leading=None,align=TA_LEFT,sb=0,sa=0):
    return ParagraphStyle(name,fontName=font,fontSize=size,textColor=color,
        leading=leading or size*1.45,alignment=align,spaceBefore=sb,spaceAfter=sa)

S_TITLE=sp("T","Helvetica-Bold",28,G_DARK,34)
S_LAT  =sp("L","Helvetica-Oblique",11,GREY,16,sa=6)
S_HDR  =sp("H","Helvetica-Bold",9,G_MID,13,sb=10,sa=3)
S_BODY =sp("B","Helvetica",10,DARK,15,align=TA_JUSTIFY)
S_BUL  =sp("BU","Helvetica",10,DARK,14,sb=1)

class GoldLine(Flowable):
    def __init__(self,w):
        super().__init__(); self.width=w; self.height=10
    def draw(self):
        c=self.canv; c.setStrokeColor(GOLD); c.setLineWidth(0.8)
        c.line(0,5,self.width,5); c.setFillColor(GOLD); m=self.width/2
        p=c.beginPath(); p.moveTo(m,10); p.lineTo(m+5,5); p.lineTo(m,0); p.lineTo(m-5,5); p.close()
        c.drawPath(p,fill=1,stroke=0)

def chrome(c,pnum,sub=""):
    c.setFillColor(G_DARK); c.rect(0,H-MT,W,MT,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,H-0.32*inch,"BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    if sub: c.drawRightString(W-MR,H-0.32*inch,sub)
    c.setFillColor(CREAM); c.rect(0,0,W,H-MT,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica",8)
    c.drawCentredString(W/2,0.16*inch,f"— {pnum} —")

def draw_stats(c,x,y,bw):
    stats=[("Length","7.1 – 8.3 in  (18 – 21 cm)"),
           ("Wingspan","11.4 – 13.0 in  (29 – 33 cm)"),
           ("Weight","1.4 – 1.7 oz  (39 – 49 g)"),
           ("Lifespan","Up to 24 years (avg. 7 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Head (male)","Glossy black — hood"),
          ("Breast patch (male)","Rose-red triangle — key field mark"),
          ("Back & wings (male)","Black with white wing patches"),
          ("Belly (male)","White"),
          ("Female — overall","Brown, streaked; white supercilium"),
          ("Bill","Large, conical, pale gray")]
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
    chrome(c,73,"Module 25 of 40")
    content=[Table([[Paragraph("MODULE  25  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Rose-breasted Grosbeak",S_TITLE),
              Paragraph("Pheucticus ludovicianus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Rose-breasted Grosbeak is one of the most stunning birds to "
            "appear at eastern feeders — the male's combination of jet-black head, "
            "bright white body, and brilliant rose-red triangular breast patch is "
            "one of the most striking plumage patterns in North American ornithology. "
            "Its arrival at sunflower feeders in early May, coinciding with peak "
            "spring migration, is one of the most eagerly anticipated events of the "
            "backyard birding year. Adding to its appeal, the male sings a rich, "
            "melodious song described as a \"robin who has had singing lessons\" — "
            "flowing phrases delivered with unusual sweetness and complexity. Females, "
            "by contrast, resemble large streaked sparrows and are often overlooked.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Rose-breasted Grosbeak breeds across southern Canada and the "
            "northeastern United States, from British Columbia east to Nova Scotia "
            "and south through the Appalachians and Great Plains. It is a long-distance "
            "migrant, wintering from Mexico through Central America to northern South "
            "America. It inhabits mature deciduous and mixed forests, forest edges, "
            "riparian woodlands, orchards, and suburban gardens with large trees. "
            "It passes through a broad migratory corridor across the eastern and "
            "central United States each spring and fall.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Black-oil sunflower seeds — the top feeder food, strongly preferred",
              "Sunflower chips and safflower seeds",
              "Wild berries and small fruits during migration and on wintering grounds",
              "Insects and larvae — the bulk of the summer breeding diet",
              "Weed seeds and wild grain in migration",
              "Flower buds and nectar occasionally in spring"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,74,"Rose-breasted Grosbeak")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Rose-breasted Grosbeaks are somewhat shy and deliberate at feeders, "
            "typically visiting in the early morning and late afternoon. Males are "
            "territorial on the breeding grounds but relatively tolerant of other "
            "species. They are powerful seed-crackers — their large, conical bill "
            "can split open hard seeds with ease. During migration they may appear "
            "at feeders in small groups of 5–10 birds, sometimes including both "
            "sexes and immature males with pinkish-orange breast washes. They "
            "spend most of their time in the mid-to-upper canopy and may be "
            "difficult to observe despite their loud song.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Rose-breasted Grosbeaks build a loosely constructed, somewhat "
            "flimsy cup nest of twigs and plant stems in a tree fork or dense "
            "shrub, typically 5–20 feet above the ground. Clutches of 3–5 pale "
            "blue-green eggs with brown spots are incubated by both parents for "
            "13–14 days — a rare behavior in songbirds. Both parents share "
            "equally in brooding and feeding the nestlings, which fledge at "
            "9–12 days. Males sometimes sing softly while incubating. One "
            "brood per season.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Rose-breasted Grosbeak's song is a rich, flowing series of "
            "melodious whistled phrases — sweeter and more polished than an "
            "American Robin's, delivered with a liquid quality that is instantly "
            "recognizable once learned. Both sexes sing — the female's song is "
            "softer but similar in structure. The call is a distinctive, sharp "
            "\"squeaky sneaker\" sound — a useful identification clue in "
            "migration when birds pass overhead.",S_BODY),
        Paragraph("CONSERVATION STATUS",S_HDR)]
    tbl=Table([[Paragraph("IUCN Red List:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Least Concern",sp("x","Helvetica-Bold",9,G_LIGHT,13)),
                Paragraph("Population trend:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Declining",sp("x","Helvetica",9,G_LIGHT,13))]],
              colWidths=[CW*0.22,CW*0.28,CW*0.25,CW*0.25])
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8)]))
    content+=[tbl,Spacer(1,6),
        Paragraph("The Rose-breasted Grosbeak population is estimated at 4.1 million "
            "individuals and has declined by approximately 35% since 1970. Loss of "
            "mature deciduous forest on both breeding and wintering grounds is the "
            "primary threat. Window collisions during migration are a significant "
            "additional mortality source. Planting large native trees and maintaining "
            "sunflower feeders during the May migration window are meaningful ways "
            "to support this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Stock sunflower feeders by late April — males arrive in early May",
              "A large hopper or platform feeder with sunflower seeds is ideal",
              "Rose-breasted Grosbeaks visit feeders most actively at dawn and dusk",
              "Watch for females — they look like large, streaky sparrows with a big pale bill",
              "Apply window decals in May — this species is highly vulnerable to glass strikes"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Rose-breasted Grosbeak  •  Pheucticus ludovicianus  •  Module 25")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 75")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
