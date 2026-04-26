from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module30_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/30_northern_mockingbird.jpg"

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
    stats=[("Length","8.3 – 10.2 in  (21 – 26 cm)"),
           ("Wingspan","12.2 – 13.8 in  (31 – 35 cm)"),
           ("Weight","1.4 – 2.0 oz  (40 – 58 g)"),
           ("Lifespan","Up to 14 years (avg. 8 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back & head","Medium gray"),
          ("Wings","Dark gray with white wing patches"),
          ("Tail","Long, dark; white outer feathers"),
          ("Underparts","Pale gray-white"),
          ("Eye","Pale yellow — striking"),
          ("Bill","Long, slightly curved, dark")]
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
    chrome(c,88,"Module 30 of 40")
    content=[Table([[Paragraph("MODULE  30  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Northern Mockingbird",S_TITLE),
              Paragraph("Mimus polyglottos",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Northern Mockingbird is one of the most vocally gifted birds in "
            "the world — a medium-sized, gray-and-white songbird capable of learning "
            "and performing the songs of dozens of other species, sometimes singing "
            "continuously for hours without repeating itself. Its scientific name, "
            "Mimus polyglottos, means \"many-tongued mimic,\" and it earns that "
            "title fully: a single male may have a repertoire of over 200 distinct "
            "song types. It is the state bird of five U.S. states — Arkansas, "
            "Florida, Mississippi, Tennessee, and Texas — and its bold, assertive "
            "personality makes it one of the most conspicuous birds in suburban "
            "and urban America.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Northern Mockingbird is a year-round resident across the southern "
            "half of the United States, from California to the Atlantic coast, and "
            "has expanded its range northward over recent decades, now regularly "
            "breeding in southern Canada. It thrives in open and semi-open habitats: "
            "suburban gardens, parks, hedgerows, roadsides, forest edges, and "
            "agricultural areas with scattered shrubs and trees. It shows a "
            "particular affinity for fruiting shrubs such as holly, pyracantha, "
            "and multiflora rose.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Wild berries: holly, pyracantha, pokeweed, multiflora rose, elderberry",
              "Insects and earthworms — dominant in warm months",
              "Small fruits: crabapple, grape, hackberry",
              "Suet and mealworms occasionally at feeders",
              "Lizards and small frogs taken occasionally",
              "Flower nectar and fruit juice probed directly in summer"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,89,"Northern Mockingbird")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Northern Mockingbirds are famously bold and aggressive, fearlessly "
            "attacking birds many times their size — hawks, crows, and even cats "
            "and dogs — that venture near their nesting or feeding territories. "
            "They maintain separate territories in summer (for breeding) and winter "
            "(for berry supplies), and defend both vigorously. Males are among the "
            "most persistent singers in North America, sometimes singing through "
            "the night during the full moon — a behavior that can test the patience "
            "of neighboring humans. Their wing-flashing display — spreading the "
            "wings suddenly to reveal white patches — may startle insects into "
            "movement, making them easier to catch.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Northern Mockingbirds build bulky cup nests of twigs and plant "
            "material, lined with grasses and rootlets, typically in a dense "
            "shrub or small tree 3–10 feet above the ground. Both parents "
            "build the nest. Clutches of 3–5 pale blue-green eggs with brown "
            "spots are incubated primarily by the female for 12–13 days. Both "
            "parents feed the nestlings, which fledge at 11–13 days. Pairs "
            "raise 2–3 broods per season and are aggressively defensive "
            "near the nest.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Northern Mockingbird's song is a continuous, exuberant medley "
            "of imitated and original phrases, each repeated 3–5 times before "
            "switching to the next. A male may mimic cardinals, jays, hawks, "
            "frogs, car alarms, and squeaky gates — anything it hears repeatedly. "
            "Unmated males sing most persistently, sometimes all night. The call "
            "is a sharp \"chuck\" or harsh \"chat.\" Song is heard year-round "
            "in warm climates.",S_BODY),
        Paragraph("CONSERVATION STATUS",S_HDR)]
    tbl=Table([[Paragraph("IUCN Red List:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Least Concern",sp("x","Helvetica-Bold",9,G_LIGHT,13)),
                Paragraph("Population trend:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Declining slightly",sp("x","Helvetica",9,G_LIGHT,13))]],
              colWidths=[CW*0.22,CW*0.28,CW*0.25,CW*0.25])
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8)]))
    content+=[tbl,Spacer(1,6),
        Paragraph("The Northern Mockingbird population is estimated at 31 million "
            "individuals but has declined by roughly 21% since 1970. Loss of "
            "dense fruiting shrub habitat through suburban development and the "
            "removal of \"weedy\" hedgerows and thickets are the primary drivers. "
            "Planting native fruiting shrubs — especially holly and native roses — "
            "and maintaining dense hedges are the most effective ways to support "
            "this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Plant native holly, pyracantha, and beautyberry — far more effective than feeders",
              "Mockingbirds rarely visit seed feeders; offer fruit pieces or mealworms on a platform",
              "They aggressively defend berry shrubs — plant enough for multiple birds",
              "A heated birdbath in winter is strongly attractive to them",
              "Expect them to chase other birds away from feeders — give them their own space"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Northern Mockingbird  •  Mimus polyglottos  •  Module 30")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 90")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
