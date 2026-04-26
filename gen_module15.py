from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module15_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/15_tufted_titmouse.jpg"

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
    stats=[("Length","5.5 – 6.3 in  (14 – 16 cm)"),
           ("Wingspan","7.9 – 10.2 in  (20 – 26 cm)"),
           ("Weight","0.6 – 0.9 oz  (18 – 26 g)"),
           ("Lifespan","Up to 13 years (avg. 2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Crest","Gray — tall and pointed"),
          ("Forehead","Black patch just above bill"),
          ("Back & wings","Medium gray"),
          ("Face & throat","White to pale gray"),
          ("Flanks","Warm peach-orange wash"),
          ("Bill","Short, stout, dark gray")]
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
    chrome(c,43,"Module 15 of 40")
    content=[Table([[Paragraph("MODULE  15  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Tufted Titmouse",S_TITLE),
              Paragraph("Baeolophus bicolor",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Tufted Titmouse is one of the most charming and acrobatic visitors "
            "to eastern feeders — a small, perky bird with a distinctive gray crest, "
            "large dark eyes, and a bold black forehead patch that gives it a perpetually "
            "alert, wide-eyed expression. It is closely related to the chickadees and "
            "shares many of their bold, inquisitive behaviors. Like the Black-capped "
            "Chickadee, it readily comes to feeders and is bold enough to take seeds "
            "from an outstretched hand with patience. Its loud, whistled song — a "
            "ringing \"peter-peter-peter\" repeated insistently — is one of the most "
            "recognizable sounds of eastern woodlands from late winter onward.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Tufted Titmouse is a permanent resident of the eastern United States, "
            "from the Great Plains east to the Atlantic coast, and from southern Ontario "
            "and New England south to Florida and the Gulf Coast. Like the Red-bellied "
            "Woodpecker, it has expanded its range significantly northward over the past "
            "50 years, aided by forest maturation, milder winters, and backyard feeders. "
            "It inhabits mature deciduous and mixed forests, forest edges, orchards, "
            "parks, and wooded suburban gardens. It shows a strong preference for areas "
            "with large oaks and other mast-producing trees.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Black-oil sunflower seeds — the clear favorite at feeders",
              "Sunflower chips and safflower seeds",
              "Suet cakes — especially valued in winter",
              "Whole and shelled peanuts",
              "Acorns, beechnuts, and hickory nuts (cached for winter)",
              "Insects, caterpillars, and spiders — critical in breeding season"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,44,"Tufted Titmouse")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Tufted Titmice are bold, curious, and highly social birds. Outside the "
            "breeding season they join mixed foraging flocks with Black-capped Chickadees, "
            "Downy Woodpeckers, and White-breasted Nuthatches, often serving as the "
            "\"nuclear\" species around which the flock organizes. They are dominant over "
            "chickadees at feeders, regularly displacing them for the best seeds. Like "
            "chickadees, they hammer seeds open by holding them with their feet and "
            "striking with the bill. Titmice are avid food cachers, storing seeds and "
            "nuts in bark crevices, soil, and leaf litter within their territory for "
            "retrieval during winter cold snaps.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Tufted Titmice are cavity nesters, using natural holes in trees, old "
            "woodpecker cavities, and nest boxes. The female builds a bulky cup nest "
            "inside the cavity using leaves, moss, bark strips, and an inner lining "
            "of soft material — notably including hair plucked directly from living "
            "animals (mammals and even humans). Clutches of 5–6 white eggs with "
            "reddish-brown spots are incubated by the female for 13–14 days. Both "
            "parents feed the nestlings, which fledge at 15–16 days. Offspring from "
            "the first brood sometimes remain as helpers to assist with subsequent "
            "broods — a rare behavior in North American songbirds.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Tufted Titmouse's song is a loud, clear, whistled \"peter-peter-"
            "peter\" or \"here-here-here\" repeated 4–11 times — one of the earliest "
            "and most persistent bird songs of late winter, often beginning in January "
            "on warm days. It also shares a vocabulary of scolding \"dee\" calls with "
            "chickadees, and the two species understand and respond to each other's "
            "alarm calls. A variety of harsh, churring scold notes are given when "
            "a predator is detected.",S_BODY),
        Paragraph("CONSERVATION STATUS",S_HDR)]
    tbl=Table([[Paragraph("IUCN Red List:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Least Concern",sp("x","Helvetica-Bold",9,G_LIGHT,13)),
                Paragraph("Population trend:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Increasing",sp("x","Helvetica",9,G_LIGHT,13))]],
              colWidths=[CW*0.22,CW*0.28,CW*0.25,CW*0.25])
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8)]))
    content+=[tbl,Spacer(1,6),
        Paragraph("The Tufted Titmouse population is estimated at approximately 8 million "
            "individuals and has been increasing steadily, driven by northward range "
            "expansion. It benefits strongly from backyard feeders, which have allowed "
            "it to survive harsher winters and colonize regions where it was formerly "
            "absent. Retaining mature trees with natural cavities and installing nest "
            "boxes are effective ways to support local populations.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Black-oil sunflower seeds in a tube or hopper feeder are ideal",
              "Offer a suet cage near large trees — titmice use it year-round",
              "Shelled peanuts in a mesh feeder attract them reliably",
              "Install a nest box (1.25-inch entrance) on a tree — they will use it",
              "Titmice are among the boldest feeder birds — hand-feeding is achievable with patience"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Tufted Titmouse  •  Baeolophus bicolor  •  Module 15")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 45")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
