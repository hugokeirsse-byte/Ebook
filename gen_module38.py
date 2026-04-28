from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module38_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/38_brown_creeper.jpg"

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
    stats=[("Length","4.7 – 5.5 in  (12 – 14 cm)"),
           ("Wingspan","6.7 – 7.9 in  (17 – 20 cm)"),
           ("Weight","0.2 – 0.4 oz  (7 – 10 g)"),
           ("Lifespan","Up to 5 years (avg. 1–2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back & crown","Brown with white streaks — bark camouflage"),
          ("Underparts","White — clean, unmarked"),
          ("Eyebrow stripe","Bold white supercilium"),
          ("Rump","Warm rufous-buff — visible in flight"),
          ("Tail","Long, stiff, pointed — prop against bark"),
          ("Bill","Long, strongly downcurved, dark")]
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
    chrome(c,112,"Module 38 of 40")
    content=[Table([[Paragraph("MODULE  38  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Brown Creeper",S_TITLE),
              Paragraph("Certhia americana",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Brown Creeper is a master of invisibility — a tiny, streaked "
            "brown bird whose bark-patterned plumage renders it nearly "
            "indistinguishable from the tree trunks it inhabits. It is the "
            "only North American member of the treecreeper family, and its "
            "foraging method is unique and instantly recognizable: it lands "
            "at the base of a tree trunk and spirals upward in short hops, "
            "probing bark crevices with its long, downcurved bill, then "
            "drops to the base of the next tree and begins again. Despite "
            "being present in wooded areas across much of North America in "
            "winter, it is so cryptic that many birders miss it entirely "
            "until they learn its thin, high-pitched call.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Brown Creeper breeds in mature coniferous and mixed forests "
            "across Canada, the Pacific states, and the Appalachians, and "
            "winters widely across the United States wherever mature trees "
            "are present. In winter it can be found in deciduous and mixed "
            "woodlands, suburban parks, and wooded gardens. It shows a "
            "strong preference for large-diameter trees with deeply furrowed "
            "bark — oaks, ashes, maples, and conifers — that harbor the "
            "insects and spiders it depends on.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Spider eggs and spiders extracted from bark crevices",
              "Insect larvae, pupae, and cocoons hidden under bark",
              "Beetles, ants, and small insects gleaned from bark surfaces",
              "Occasionally visits suet feeders — suet smeared on bark is most effective",
              "Pine seeds taken rarely in winter",
              "Largely insectivorous year-round — does not visit seed feeders"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,113,"Brown Creeper")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("The Brown Creeper's foraging behavior is one of the most "
            "specialized of any North American bird. It invariably starts "
            "at the base of a tree and works upward in a systematic spiral, "
            "using its stiff, pointed tail feathers as a prop — exactly "
            "like a woodpecker. When it reaches the upper trunk or a major "
            "branch, it drops directly to the base of the next tree and "
            "repeats the process. In winter it often joins mixed foraging "
            "flocks with chickadees, nuthatches, and kinglets, benefiting "
            "from the collective vigilance of the flock while maintaining "
            "its own specialized foraging niche on bark surfaces.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("The Brown Creeper builds a unique hammock-shaped nest of "
            "bark strips, mosses, and spider webs tucked behind a slab "
            "of loose bark on a dead or dying tree — one of the most "
            "unusual nest sites of any North American bird. The female "
            "incubates 5–6 white eggs with reddish-brown spots for "
            "13–17 days. Both parents feed the nestlings, which fledge "
            "at 13–16 days. One brood per season. The species requires "
            "large-diameter trees with loose bark for nesting — a "
            "habitat increasingly scarce in managed forests.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Brown Creeper's call is a thin, high-pitched \"seee\" — "
            "a single, almost inaudible note that is easy to overlook. "
            "Once learned, however, it immediately reveals the presence "
            "of this otherwise invisible bird. The song is a sweet, "
            "descending series of thin whistles: \"see-see-see-sissy-see\" "
            "— delicate and ethereal, delivered from high in the canopy "
            "in spring. Both call and song are at the upper frequency "
            "range of human hearing and may be inaudible to some "
            "older birders.",S_BODY),
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
        Paragraph("The Brown Creeper population is estimated at 6.3 million "
            "individuals and has shown modest declines linked to the loss "
            "of old-growth and mature second-growth forest with large-diameter "
            "trees. It is highly dependent on large trees with deeply "
            "furrowed bark for both foraging and nesting. Retaining mature "
            "trees and standing dead snags in woodlands and parks is "
            "the most effective conservation action for this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Smear suet or peanut butter directly onto rough tree bark — the best attractant",
              "Brown Creepers rarely use cage feeders — bark-smeared food is key",
              "Retain large trees with deeply furrowed bark in the yard",
              "Leave dead snags standing — essential for nesting behind loose bark",
              "Listen for the thin 'seee' call in winter mixed flocks near large trees"]:
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
    c.drawCentredString(W/2,H-0.66*inch,"Brown Creeper  •  Certhia americana  •  Module 38")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 114")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
