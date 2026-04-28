from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module26_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/26_blackcapped_chickadee.jpg"

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
    c.drawCentredString(W/2,0.28*inch,f"— {pnum} —")

def draw_stats(c,x,y,bw):
    stats=[("Length","4.7 – 5.9 in  (12 – 15 cm)"),
           ("Wingspan","6.3 – 8.3 in  (16 – 21 cm)"),
           ("Weight","0.3 – 0.5 oz  (9 – 14 g)"),
           ("Lifespan","Up to 12 years (avg. 2–3 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Cap","Glossy black"),
          ("Bib","Black — extends to upper breast"),
          ("Cheeks","Bright white"),
          ("Back & wings","Gray — soft, medium tone"),
          ("Breast & belly","White to pale buff on flanks"),
          ("Bill","Short, stout, black")]
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
    chrome(c,76,"Module 26 of 40")
    content=[Table([[Paragraph("MODULE  26  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Black-capped Chickadee",S_TITLE),
              Paragraph("Poecile atricapillus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Black-capped Chickadee is arguably the most beloved feeder bird "
            "in North America — a tiny, round, endlessly cheerful bird whose bold "
            "black cap, crisp white cheeks, and fearless curiosity have made it a "
            "symbol of winter resilience and backyard birding joy. It is one of the "
            "few wild birds that can be trained to take seeds from an outstretched "
            "hand, and it often does so with remarkable boldness. Despite its tiny "
            "size — barely heavier than two nickels — it is superbly adapted to "
            "survive the harshest northern winters, capable of lowering its body "
            "temperature at night to conserve energy and maintaining thousands of "
            "cached food items whose locations it can remember for weeks.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Black-capped Chickadee is found year-round across the northern "
            "United States and most of Canada, from Alaska east to Newfoundland and "
            "south through the northern tier of states, the Appalachians, and the "
            "Pacific Northwest. It inhabits deciduous and mixed forests, forest edges, "
            "suburban parks, and wooded gardens wherever there are trees large enough "
            "to provide nesting cavities and foraging opportunities. It is a permanent "
            "resident throughout its range, though it may make short irruptive "
            "movements in years when northern food supplies fail.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Black-oil sunflower seeds — the absolute top choice at feeders",
              "Sunflower chips and safflower seeds",
              "Suet cakes — especially important in cold winter months",
              "Peanut pieces and whole peanuts",
              "Nyjer seed — taken occasionally",
              "Insects, spiders, and their eggs gleaned from bark — dominant summer food"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,77,"Black-capped Chickadee")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Black-capped Chickadees live in stable winter flocks of 6–10 birds "
            "with a fixed dominance hierarchy. The dominant pair leads the flock and "
            "gets priority access to the best food. Subordinate birds are pushed to "
            "the flock's periphery, where predator risk is higher. Flock members "
            "communicate constantly with a complex vocabulary of calls. They are "
            "among the most important \"nuclear species\" in winter mixed-species "
            "flocks — nuthatches, Downy Woodpeckers, and kinglets follow chickadee "
            "flocks and respond to their alarm calls. Chickadees are extraordinary "
            "food cachers, hiding thousands of seeds in bark crevices, leaves, "
            "and soil, and relocating each cache within weeks.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Black-capped Chickadees excavate their own nest cavities in soft, "
            "rotting wood — a capability unique among small songbirds. They also "
            "readily use nest boxes. The female builds a soft cup nest inside the "
            "cavity using moss, plant fibers, and a thick lining of mammal fur "
            "and plant down. Clutches of 6–8 white eggs with reddish-brown spots "
            "are incubated by the female for 12–13 days. Both parents feed the "
            "nestlings, which fledge at 16 days. One brood per season.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Black-capped Chickadee has one of the most complex vocal "
            "systems of any North American bird. Its familiar \"chick-a-dee-dee-dee\" "
            "call varies in the number of \"dee\" notes to encode the urgency of "
            "predator threats — more \"dees\" mean a more dangerous predator nearby. "
            "The male's clear, two-note whistled \"fee-bee\" song is one of the "
            "first sounds of late winter, often heard on warm days in January "
            "or February.",S_BODY),
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
        Paragraph("The Black-capped Chickadee population is estimated at 41 million "
            "individuals and is broadly stable. It is one of the most studied birds "
            "in North America, with long-term research revealing remarkable cognitive "
            "abilities including episodic-like memory and the ability to expand the "
            "hippocampus (the brain's memory center) in autumn to accommodate "
            "increased caching demands. It benefits strongly from backyard feeders "
            "and nest box programs.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Black-oil sunflower seeds in any feeder style — chickadees use all types",
              "They cache seeds — expect rapid, repeated visits as they store for winter",
              "Hand-feeding is achievable: stand still near the feeder with seeds in palm",
              "Install a nest box (1.25-inch entrance) on a tree or post — they will use it",
              "Suet in a cage feeder is especially valued during cold snaps below freezing"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Black-capped Chickadee  •  Poecile atricapillus  •  Module 26")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 78")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
