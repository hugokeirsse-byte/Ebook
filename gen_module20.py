from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module20_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/20_cedar_waxwing.jpg"

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
    stats=[("Length","5.5 – 6.7 in  (14 – 17 cm)"),
           ("Wingspan","8.7 – 11.8 in  (22 – 30 cm)"),
           ("Weight","1.1 – 1.4 oz  (32 – 40 g)"),
           ("Lifespan","Up to 13 years (avg. 5 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Head & crest","Silky warm brown — tawny"),
          ("Black mask","Bold black eye mask — both sexes"),
          ("Back & breast","Smooth gray-brown, blending"),
          ("Belly","Pale yellow fading to white"),
          ("Tail tip","Bright yellow band"),
          ("Wing tips","Red waxy droplets (adults)"  )]
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
    chrome(c,58,"Module 20 of 40")
    content=[Table([[Paragraph("MODULE  20  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Cedar Waxwing",S_TITLE),
              Paragraph("Bombycilla cedrorum",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Cedar Waxwing is perhaps the most elegantly plumaged bird in "
            "North America — a sleek, silky bird of extraordinary refinement, with "
            "smooth blended plumage in tones of warm brown, gray, and pale yellow, "
            "set off by a bold black mask, a brilliant yellow tail-tip band, and "
            "the mysterious red waxy droplets on its wing tips that give the species "
            "its name. These red tips are actually extensions of the feather shafts "
            "and increase in number with age — older birds have more, making them "
            "more attractive to potential mates. Cedar Waxwings are nomadic flock "
            "birds, appearing unpredictably wherever berries are abundant and "
            "stripping entire trees in a matter of hours.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Cedar Waxwing breeds across southern Canada and the northern "
            "United States, from British Columbia to Newfoundland and south through "
            "the Appalachians and northern Great Plains. In winter it roams widely "
            "across the entire contiguous United States and into Central America, "
            "following berry crops. It inhabits open woodlands, forest edges, "
            "orchards, suburban parks, and gardens — wherever fruiting trees and "
            "shrubs are present. It shows a particularly strong association with "
            "fruiting cedars, serviceberries, crabapples, and mountain ash.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Wild berries — cedar, serviceberry, crabapple, hawthorn, holly",
              "Mountain ash berries — a winter favorite",
              "Dogwood, viburnum, and elderberry fruits",
              "Insects caught in aerial sallies during summer — especially near water",
              "Cherry and apple fruits — sometimes causing intoxication from fermentation",
              "Flower petals occasionally consumed in spring"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,59,"Cedar Waxwing")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Cedar Waxwings are among the most social songbirds in North America, "
            "living in tight flocks year-round and rarely seen alone. Flocks move "
            "nomadically across the landscape, locating fruiting trees by sight and "
            "sound and descending en masse to strip them. They show a remarkable "
            "behavior of passing berries or flower petals beak-to-beak along a "
            "perched row of birds — an apparent bonding or courtship ritual. Unlike "
            "most songbirds, waxwings do not defend feeding territories and "
            "tolerate conspecifics freely at food sources. They are highly efficient "
            "berry consumers, capable of eating their body weight in fruit daily, "
            "and are important seed dispersers for many native plants.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Cedar Waxwings are late nesters, typically not beginning until "
            "June or July to coincide with the peak availability of summer berries. "
            "They often nest in loose colonies. The female builds a bulky cup nest "
            "of grasses, twigs, and plant fibers in a tree fork, lined with fine "
            "grasses and hair. Clutches of 3–5 pale gray eggs with dark spots are "
            "incubated by the female for 11–13 days. Both parents feed the "
            "nestlings, which fledge at 14–18 days. One to two broods per season.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Cedar Waxwing's vocalizations are among the most distinctive "
            "in North American birding — a high, thin, sibilant trill or whistle, "
            "often written as \"seeeee\" or \"srrrrr,\" that is easily missed by "
            "those with high-frequency hearing loss. Flocks produce a constant "
            "soft chorus of these calls as they feed — often the first indication "
            "that waxwings are present overhead. They have no true song in the "
            "traditional sense.",S_BODY),
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
        Paragraph("The Cedar Waxwing population is estimated at 52 million individuals "
            "and has increased significantly since the 1960s, benefiting from the "
            "maturation of forest edges and the proliferation of ornamental fruiting "
            "trees in suburban landscapes. It is one of the few fruit-specialist "
            "songbirds to have thrived in human-modified environments. Window "
            "collisions are a significant mortality source for this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Plant native serviceberry, crabapple, hawthorn, and holly — they don't use traditional feeders",
              "Mountain ash is one of the most reliable trees for attracting winter flocks",
              "Leave fruiting shrubs unpruned through winter — waxwings will find them",
              "A shallow birdbath near fruiting trees greatly increases attractiveness",
              "Listen for the high, thin \"seee\" call overhead — often the first sign of a flock"]:
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
    c.drawCentredString(W/2,H-0.66*inch,"Cedar Waxwing  •  Bombycilla cedrorum  •  Module 20")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 60")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
