from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module13_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/13_mourning_dove.jpg"

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
    c.drawString(ML,H-0.40*inch,"BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    if sub: c.drawRightString(W-MR,H-0.40*inch,sub)
    c.setFillColor(CREAM); c.rect(0,0,W,H-MT,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica",8)
    c.drawCentredString(W/2,0.35*inch,f"— {pnum} —")

def draw_stats(c,x,y,bw):
    stats=[("Length","9.1 – 13.4 in  (23 – 34 cm)"),
           ("Wingspan","17.7 in  (45 cm)"),
           ("Weight","3.4 – 6.0 oz  (96 – 170 g)"),
           ("Lifespan","Up to 31 years (avg. 1–2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Body","Warm buffy tan — soft and uniform"),
          ("Wings","Light brown with black spots"),
          ("Neck patch","Iridescent blue-green (male)"),
          ("Tail","Long, pointed; white-tipped edges"),
          ("Bill","Short, slender, dark gray"),
          ("Legs & feet","Red-pink")]
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
    chrome(c,37,"Module 13 of 40")
    content=[Table([[Paragraph("MODULE  13  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Mourning Dove",S_TITLE),
              Paragraph("Zenaida macroura",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Mourning Dove is one of the most abundant and widespread birds in "
            "North America, with a population estimated at 350 million individuals — "
            "making it the most numerous wild bird on the continent. Elegant in its "
            "simplicity, its soft buffy-tan plumage, long pointed tail, and gentle "
            "demeanor make it an instant favorite at feeders. Its mournful, cooing "
            "call — \"ooo-woo-woo-woo\" — is one of the most evocative and widely "
            "recognized sounds of the North American countryside, often mistaken for "
            "an owl by those who first hear it. It is also one of the most important "
            "game birds in North America, legally hunted in most states.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Mourning Dove is found year-round across the entire contiguous "
            "United States, southern Canada, Mexico, and the Caribbean. It is a bird "
            "of open and semi-open habitats: farmland, grasslands, woodland edges, "
            "roadsides, suburban parks, and gardens. It avoids dense, closed-canopy "
            "forest but thrives wherever there are open ground areas for foraging and "
            "scattered trees or shrubs for nesting and roosting. Northern populations "
            "are partially migratory, moving south in cold winters, while southern "
            "birds are permanent residents.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["White millet — the top preference, eagerly consumed on the ground",
              "Black-oil sunflower seeds and cracked corn",
              "Safflower seeds and milo",
              "Wild grass seeds, weed seeds, and waste grain",
              "Occasionally pine seeds and small berries",
              "Grit (small stones) swallowed to aid digestion in the crop"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,38,"Mourning Dove")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Mourning Doves are gregarious birds that gather in large flocks at "
            "productive feeding sites, sometimes numbering in the dozens or even "
            "hundreds. They are ground feeders almost exclusively, walking with a "
            "characteristic bobbing head motion as they pick up seeds. Unlike most "
            "songbirds, they swallow seeds whole and store them in an enlarged crop, "
            "then digest them later — allowing them to feed rapidly and retreat to "
            "cover. Their wings produce a loud, distinctive whistling sound when they "
            "take off — a built-in alarm signal for the flock. Despite their gentle "
            "appearance, males can be aggressively competitive at feeding areas, "
            "chasing rivals with bowing displays.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Mourning Doves are prolific breeders, raising up to 6 broods per "
            "year in warm climates — more than almost any other North American bird. "
            "The nest is a remarkably flimsy platform of twigs, so loosely constructed "
            "that eggs are often visible from below. It is placed in a tree, shrub, "
            "or even on the ground. Both parents incubate 2 pure white eggs for "
            "13–15 days. Both parents feed nestlings \"crop milk\" — a protein-rich "
            "secretion produced in the crop — for the first week, then gradually "
            "introduce seeds. Young fledge at 12–15 days.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Mourning Dove's call is a haunting, hollow coo — typically "
            "\"ooo-woo-woo-woo\" with the first note higher in pitch. It is one of "
            "the most widely recognized bird sounds in North America and carries "
            "long distances in still air. The call is given year-round but peaks "
            "during the breeding season. The loud wing whistle produced at takeoff "
            "serves as an alarm signal, alerting nearby birds to a predator. "
            "Males also give a soft courtship coo during pair bonding.",S_BODY),
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
        Paragraph("With an estimated 350 million individuals, the Mourning Dove is the "
            "most abundant game bird and one of the most numerous wild birds in North "
            "America. It is legally hunted in 41 U.S. states, with an annual harvest "
            "exceeding 20 million birds — yet the population remains stable thanks to "
            "its extraordinary reproductive rate. It has benefited from the expansion "
            "of agriculture and suburban habitats across the continent.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Scatter white millet and cracked corn directly on the ground",
              "A large, flat ground tray or platform feeder suits them best",
              "Mourning Doves arrive at feeders early in the morning and at dusk",
              "Keep the feeding area clear of deep snow — they cannot dig through it",
              "They are skittish — minimize foot traffic near the feeding area"]:
        content.append(Paragraph(f"<bullet>•</bullet>  {t}",S_BUL))
    content.append(Paragraph("COLORING GUIDE",S_HDR))
    GUIDE_H=6*0.22*inch+0.28*inch; guide_y=MB+GUIDE_H+0.15*inch
    Frame(ML,guide_y+0.08*inch,CW,H-MT-(guide_y+0.08*inch)-0.12*inch,
          leftPadding=0,rightPadding=0,topPadding=0.1*inch,
          bottomPadding=0,showBoundary=0).addFromList(content,c)
    draw_color_guide(c,ML,guide_y,CW)

def page3(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    HDR_H=0.80*inch
    c.setFillColor(G_DARK); c.rect(0,H-HDR_H,W,HDR_H,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica-Bold",16)
    c.drawCentredString(W/2,H-0.48*inch,"COLOR ME!")
    c.setFillColor(G_LIGHT); c.setFont("Helvetica",9)
    c.drawCentredString(W/2,H-0.66*inch,"Mourning Dove  •  Zenaida macroura  •  Module 13")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 39")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
