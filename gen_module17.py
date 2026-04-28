from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module17_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/17_american_crow.jpg"

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
    stats=[("Length","17.5 – 21.0 in  (44 – 53 cm)"),
           ("Wingspan","33.5 – 39.4 in  (85 – 100 cm)"),
           ("Weight","11.2 – 21.9 oz  (316 – 620 g)"),
           ("Lifespan","Up to 16 years (avg. 7–8 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Entire body","Jet black — uniform and glossy"),
          ("Iridescence","Blue-violet sheen in sunlight"),
          ("Bill","Heavy, curved, black"),
          ("Legs & feet","Black"),
          ("Eye","Dark brown — appears black"),
          ("Juvenile plumage","Duller black; blue eye at first")]
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
    chrome(c,49,"Module 17 of 40")
    content=[Table([[Paragraph("MODULE  17  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("American Crow",S_TITLE),
              Paragraph("Corvus brachyrhynchos",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The American Crow is one of the most intelligent, adaptable, and "
            "ecologically important birds in North America — a large, all-black bird "
            "with a heavy bill, fan-shaped tail, and an extraordinary capacity for "
            "learning, problem-solving, and social organization. Crows can recognize "
            "individual human faces, use tools, pass information between generations, "
            "and hold \"funerals\" for fallen flock members — behaviors once thought "
            "exclusive to primates. Their loud, familiar \"caw\" is one of the most "
            "iconic sounds of the North American landscape. Highly social and "
            "opportunistic, they thrive in virtually every habitat from wilderness "
            "to city centers.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The American Crow is found year-round across most of North America, "
            "from southern Canada through the entire contiguous United States except "
            "for the driest desert regions. It occupies an extraordinary range of "
            "habitats: farmland, forest edges, river valleys, coastal shorelines, "
            "suburban neighborhoods, parks, and city centers. It is one of the few "
            "species that has benefited from human landscape changes, thriving wherever "
            "there is a mix of open foraging areas and trees for roosting and nesting. "
            "Northern populations move south in winter, often forming massive communal "
            "roosts of thousands to hundreds of thousands of birds.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Virtually omnivorous — one of the broadest diets of any bird",
              "Grain, corn, and seeds scavenged from fields and feeders",
              "Insects, earthworms, and small mammals",
              "Carrion and roadkill — an important ecological scavenger",
              "Eggs and nestlings of other birds",
              "Fruit, berries, nuts, and human food scraps"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,50,"American Crow")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("American Crows are among the most socially complex birds in the world. "
            "They live in extended family groups where offspring from previous years "
            "help their parents raise subsequent broods — a behavior called cooperative "
            "breeding. Family groups maintain tight bonds year-round, foraging together, "
            "mobbing predators collectively, and communicating with a rich vocabulary "
            "of calls. Crows can recognize and remember individual human faces for "
            "years, and will \"hold grudges\" against people who have threatened them "
            "while tolerating those who have been kind. In winter, unrelated crows "
            "gather in communal roosts that can number in the millions, providing "
            "warmth and safety in numbers.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Crows nest in late winter and early spring, building large, bulky "
            "cup nests of sticks lined with bark strips, grass, and soft material "
            "in the crotch of a tall tree. Clutches of 3–6 pale green or blue-gray "
            "eggs with brown spots are incubated by the female for 17–19 days. Both "
            "parents and often \"helper\" offspring from previous years feed the "
            "nestlings. Young fledge at 28–35 days but remain with the family group "
            "for 1–5 years. Breeding pairs mate for life.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The American Crow has one of the most complex vocal repertoires of "
            "any North American bird — researchers have identified over 20 distinct "
            "call types. The familiar \"caw\" varies in pitch, repetition, and "
            "rhythm to convey different messages: alarm, aggression, assembly, and "
            "contact. Crows also produce a remarkable array of rattles, coos, "
            "clicks, and mimicked sounds. Family members recognize each other's "
            "voices individually.",S_BODY),
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
        Paragraph("The American Crow population is estimated at 27 million individuals "
            "and is broadly stable. It suffered dramatic declines during the initial "
            "spread of West Nile Virus in the early 2000s — crows are among the most "
            "susceptible species — but has largely recovered in most areas. It remains "
            "one of the most abundant and visible large birds in North America.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Crows rarely use traditional feeders — offer food on the ground or a large platform",
              "Whole corn, peanuts in shell, and kitchen scraps attract them reliably",
              "They are wary — place food in an open area where they can watch for danger",
              "Crows remember generous feeding spots and return reliably for years",
              "Avoid feeding near songbird feeders — crows can intimidate smaller birds"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"American Crow  •  Corvus brachyrhynchos  •  Module 17")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 51")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
