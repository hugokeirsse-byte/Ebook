from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module24_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/24_eastern_towhee.jpg"

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
    stats=[("Length","6.8 – 8.2 in  (17 – 21 cm)"),
           ("Wingspan","7.9 – 11.0 in  (20 – 28 cm)"),
           ("Weight","1.1 – 1.8 oz  (32 – 53 g)"),
           ("Lifespan","Up to 12 years (avg. 3 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Head & back (male)","Glossy black"),
          ("Breast sides & flanks","Rich rufous-orange"),
          ("Belly","White — clean and contrasting"),
          ("Tail corners","White spots — flash in flight"),
          ("Female — head & back","Warm brown replacing black"),
          ("Eye","Red — striking in both sexes")]
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
    chrome(c,70,"Module 24 of 40")
    content=[Table([[Paragraph("MODULE  24  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Eastern Towhee",S_TITLE),
              Paragraph("Pipilo erythrophthalmus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Eastern Towhee is one of the most boldly plumaged and charismatic "
            "ground birds of the eastern United States — a large, striking sparrow "
            "whose jet-black hood, warm rufous-orange flanks, and clean white belly "
            "create one of the most elegant color combinations of any North American "
            "songbird. Its vivid red eye is startling at close range. The Eastern "
            "Towhee is primarily a bird of dense undergrowth, heard far more often "
            "than it is seen — its loud, emphatic \"drink-your-teeeeea\" song rings "
            "from thickets across the eastern woodlands from spring through summer. "
            "At feeders it appears mainly in winter, scratching vigorously beneath "
            "shrubs for spilled seed.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Eastern Towhee is found across the eastern United States, from "
            "southern Canada south to Florida and west to the Great Plains. It "
            "inhabits dense shrubby undergrowth: forest edges with thick brush, "
            "overgrown fields, bramble thickets, woodland clearings, suburban "
            "gardens with dense native plantings, and pine-oak barrens. It is "
            "a permanent resident in the South and a summer resident in the "
            "North, with northern populations moving south in winter. It is "
            "closely associated with areas of deep leaf litter beneath dense "
            "low vegetation.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["White millet and cracked corn scattered on the ground",
              "Black-oil sunflower seeds picked up from beneath feeders",
              "Wild weed seeds and grass seeds scratched from leaf litter",
              "Wild berries: blackberry, blueberry, serviceberry, pokeweed",
              "Insects, spiders, millipedes, and earthworms",
              "Acorns and small nuts broken open on the ground"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,71,"Eastern Towhee")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("The Eastern Towhee's most characteristic behavior is its vigorous "
            "double-scratch foraging technique — a powerful two-footed backward "
            "kick that hurls leaf litter aside to expose seeds and invertebrates "
            "hidden beneath. This scratching can be heard from a considerable "
            "distance and is often the first indication that a towhee is nearby. "
            "Towhees are mostly solitary outside the breeding season, spending "
            "their time in dense undergrowth where they are difficult to observe. "
            "Males are territorial and persistent singers, often delivering their "
            "song from the top of a tall shrub — one of the few occasions when "
            "this secretive species is easily visible.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Eastern Towhees nest on or very near the ground, placing their "
            "bulky cup nest of leaves, bark strips, and grasses in a shallow "
            "depression concealed beneath dense shrubs or in a grass clump. "
            "The female builds the nest and incubates 3–4 creamy white eggs "
            "with reddish-brown spots for 12–13 days. Both parents feed the "
            "nestlings, which fledge at 10–12 days. The species raises 2–3 "
            "broods per season. Eastern Towhees are frequent cowbird hosts, "
            "and their ground-level nests suffer high predation rates.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Eastern Towhee's song is one of the most recognizable in "
            "eastern North America — a clear, emphatic \"drink-your-teeeeea\" "
            "with the final note a long, buzzy trill rising in pitch. Males "
            "sing persistently from spring through midsummer. The call is a "
            "sharp, rising \"chewink\" or \"towhee\" — the source of both the "
            "common name and its former name, \"Rufous-sided Towhee.\" A soft "
            "\"mew\" contact call is given in dense cover.",S_BODY),
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
        Paragraph("The Eastern Towhee population is estimated at 26 million individuals "
            "but has declined by roughly 50% since 1970 — one of the steeper declines "
            "among common eastern songbirds. The primary cause is the loss of dense "
            "shrubby edge habitat as forests mature and close canopy, eliminating the "
            "open undergrowth this species requires. Maintaining brush piles, bramble "
            "patches, and dense native shrubs is the most effective way to support "
            "towhees in the garden.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Scatter white millet and cracked corn on bare ground beneath dense shrubs",
              "A brush pile near the feeding area is essential — towhees need escape cover",
              "They rarely use elevated feeders — ground feeding is their only mode",
              "Plant native blackberries, serviceberries, and viburnums for natural food",
              "Listen for vigorous leaf-scratching sounds in thickets — the first sign of a towhee"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Eastern Towhee  •  Pipilo erythrophthalmus  •  Module 24")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 72")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
