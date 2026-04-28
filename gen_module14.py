from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module14_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/14_redbellied_woodpecker.jpg"

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
    stats=[("Length","9.4 in  (24 cm)"),
           ("Wingspan","13.0 – 16.5 in  (33 – 42 cm)"),
           ("Weight","2.0 – 3.2 oz  (56 – 91 g)"),
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
    rows=[("Crown (male)","Full red cap — forehead to nape"),
          ("Crown (female)","Red on nape only; gray forehead"),
          ("Back & wings","Bold black-and-white barring"),
          ("Face & underparts","Pale gray-buff"),
          ("Belly patch","Faint red-orange wash (often hidden)"),
          ("Bill","Long, chisel-tipped, dark gray")]
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
    chrome(c,40,"Module 14 of 40")
    content=[Table([[Paragraph("MODULE  14  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Red-bellied Woodpecker",S_TITLE),
              Paragraph("Melanerpes carolinus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("Despite its name, the Red-bellied Woodpecker's most striking feature is "
            "its brilliant red cap — not its belly, which shows only a faint reddish wash "
            "that is rarely visible in the field. This bold, vocal woodpecker has expanded "
            "dramatically northward over the past century, colonizing new areas of the "
            "northeastern United States and southern Canada as forests have matured. "
            "With its ladder-backed black-and-white barring and loud, rolling \"churr\" "
            "call, it is one of the most conspicuous and entertaining birds at suet feeders "
            "across eastern North America. Its remarkably long, barbed tongue — extending "
            "up to 2 inches beyond the bill — allows it to extract insects from deep "
            "bark crevices and remove seeds from tight spaces.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Red-bellied Woodpecker is found year-round across the eastern "
            "United States, from southern Canada south to Florida and west to the "
            "Great Plains. It inhabits mature deciduous and mixed forests, forest edges, "
            "suburban parks, and wooded gardens with large trees. It shows a preference "
            "for oak-dominated forests where acorns are plentiful, but readily adapts "
            "to suburban environments wherever there are large, established trees. "
            "It is a permanent resident throughout its range and does not migrate.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Suet cakes — the top feeder attraction for this species",
              "Black-oil sunflower seeds and sunflower chips",
              "Whole and shelled peanuts",
              "Acorns and beechnuts (cached in bark crevices)",
              "Insects and larvae extracted from dead wood",
              "Wild berries and small fruits — especially in autumn"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,41,"Red-bellied Woodpecker")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Red-bellied Woodpeckers are bold, assertive birds at feeders, often "
            "dominating smaller species such as Downy Woodpeckers and nuthatches. They "
            "are year-round residents that maintain fixed territories, defended loudly "
            "with calls and drumming. Like other woodpeckers, they are avid food "
            "cachers — storing seeds, acorns, and insects in bark crevices, post holes, "
            "and even the gaps in wooden siding. Their long, sticky tongue is specially "
            "adapted to extract prey from deep crevices, and their stiff tail feathers "
            "act as a prop against tree trunks. They often join mixed foraging flocks "
            "with chickadees and nuthatches in winter.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Red-bellied Woodpeckers excavate nest cavities in dead or dying trees, "
            "typically at heights of 5–70 feet. The male does most of the excavation, "
            "taking 1–2 weeks to complete the cavity. Both parents incubate the 4–5 "
            "white eggs for 12 days. Both parents feed the nestlings, which fledge at "
            "24–27 days. The species raises 2–3 broods per season. Old cavities are "
            "frequently reused in subsequent years and provide critical nesting sites "
            "for secondary cavity nesters such as Eastern Bluebirds and screech-owls.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Red-bellied Woodpecker is one of the most vocal woodpeckers in "
            "eastern North America. Its primary call is a loud, rolling \"churr\" or "
            "\"kwirr\" that carries clearly through the forest. It also gives a sharp "
            "\"chek\" alarm call and a variety of softer conversational notes between "
            "mates. Drumming on resonant dead wood or metal surfaces serves as a "
            "territorial advertisement, with rapid, sustained bursts that can be heard "
            "from considerable distances.",S_BODY),
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
        Paragraph("The Red-bellied Woodpecker has been one of the great conservation "
            "success stories of recent decades. Once largely confined to the southeastern "
            "United States, it has expanded its range steadily northward since the "
            "mid-20th century, benefiting from forest maturation, milder winters, and "
            "the proliferation of backyard feeders. Its population is estimated at "
            "approximately 16 million individuals and continues to grow.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Mount a suet cage directly on a tree trunk — ideal positioning for this species",
              "Offer whole peanuts in a mesh peanut feeder",
              "Large hopper or platform feeders with sunflower seeds attract them readily",
              "Install a nest box with a 2-inch entrance hole on a large dead snag",
              "Red-bellied Woodpeckers cache food — expect them to make repeated quick visits"]:
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
    c.drawCentredString(W/2,H-0.66*inch,"Red-bellied Woodpecker  •  Melanerpes carolinus  •  Module 14")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 42")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
