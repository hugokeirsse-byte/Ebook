from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module31_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/31_rubythroated_hummingbird.jpg"

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
    c.drawCentredString(W/2,0.35*inch,f"— {pnum} —")

def draw_stats(c,x,y,bw):
    stats=[("Length","2.8 – 3.5 in  (7 – 9 cm)"),
           ("Wingspan","3.1 – 4.3 in  (8 – 11 cm)"),
           ("Weight","0.1 – 0.2 oz  (2.4 – 6.1 g)"),
           ("Lifespan","Up to 9 years (avg. 3–5 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back & crown (male)","Iridescent emerald green"),
          ("Throat gorget (male)","Ruby red — iridescent, angle-dependent"),
          ("Underparts","White to pale gray"),
          ("Female — throat","White, may show faint streaking"),
          ("Wings","Dark — blur at 53 beats/second"),
          ("Bill","Long, needle-straight, black")]
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
    chrome(c,91,"Module 31 of 40")
    content=[Table([[Paragraph("MODULE  31  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Ruby-throated Hummingbird",S_TITLE),
              Paragraph("Archilochus colubris",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Ruby-throated Hummingbird is the only hummingbird that breeds "
            "in eastern North America — a gem of iridescent emerald and ruby that "
            "seems too brilliant and too small to be real. Weighing less than a "
            "penny, it beats its wings 53 times per second in normal flight and "
            "up to 200 times per second in a courtship dive, generating the "
            "characteristic humming sound that gives the family its name. It is "
            "a physiological marvel: its heart beats up to 1,260 times per minute "
            "during flight, and it enters torpor each night — dropping its body "
            "temperature dramatically to conserve energy — yet crosses the Gulf "
            "of Mexico in a single non-stop flight of 500 miles during migration.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Ruby-throated Hummingbird breeds across eastern North America, "
            "from southern Canada south through the entire eastern United States "
            "to the Gulf Coast and into Central America. It winters from Mexico "
            "through Central America. It inhabits forest edges, gardens, orchards, "
            "and any open area with flowering plants. It shows a particular "
            "preference for tubular red and orange flowers: trumpet vine, cardinal "
            "flower, bee balm, and salvia. It arrives in the East in late April "
            "and departs by early October.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Nectar — from both flowers and hummingbird feeders (4:1 water:sugar solution)",
              "Small insects and spiders — essential protein, especially for females and nestlings",
              "Tree sap from sapsucker wells — used during early spring before flowers bloom",
              "Trumpet vine, cardinal flower, bee balm, columbine, salvia nectar",
              "Gnats and small flies caught in aerial sallies",
              "Never use red dye in feeders — plain sugar water is safest"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,92,"Ruby-throated Hummingbird")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Ruby-throated Hummingbirds are fiercely territorial and largely "
            "solitary. Males defend feeding territories with aggressive aerial "
            "chases, driving away rival males and often females as well. Their "
            "courtship display is spectacular: the male performs pendulum-like "
            "U-shaped or figure-eight dives in front of a perched female, "
            "the rush of air through the tail feathers creating a distinctive "
            "chirping sound. Outside the breeding season individuals are "
            "independent and non-social. They have extraordinary spatial memory, "
            "returning to the exact same feeders and flowers year after year "
            "within days of their spring arrival date.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("The female builds a tiny, exquisite cup nest the size of a large "
            "thimble, constructed from plant down and bud scales bound together "
            "with spider silk — which allows the nest to expand as the nestlings "
            "grow. It is camouflaged with lichens on the outside and placed on "
            "a downward-sloping branch. She lays 2 white eggs the size of small "
            "jellybeans and incubates them alone for 11–16 days. She feeds the "
            "nestlings regurgitated nectar and insects. Young fledge at 18–22 days. "
            "The male plays no role in nesting.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Ruby-throated Hummingbird's primary sound is its wing hum — "
            "the rapid wingbeats produce a distinctive buzzing tone that varies "
            "with flight speed and behavior. Vocal calls are a rapid, chittering "
            "\"chee-dit\" and a series of sharp chips used in aggressive "
            "encounters. Males produce a distinctive tail-chirp during courtship "
            "dives. The species has no true song.",S_BODY),
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
        Paragraph("The Ruby-throated Hummingbird population is estimated at 34 million "
            "individuals and is broadly stable. It is one of the few migratory "
            "species whose range has benefited from the proliferation of backyard "
            "feeders and native plantings. Threats include pesticide use reducing "
            "insect prey, habitat loss on wintering grounds, and window collisions. "
            "Planting native flowers and keeping feeders clean are the most "
            "effective support actions.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Mix 1 part white sugar to 4 parts water — no red dye, no honey",
              "Clean feeders every 2–3 days in summer heat to prevent mold and fermentation",
              "Put feeders out by late April in the East — males arrive before females",
              "Plant trumpet vine, cardinal flower, bee balm, and salvia for natural nectar",
              "Multiple feeders spaced apart reduce territorial aggression at feeding sites"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Ruby-throated Hummingbird  •  Archilochus colubris  •  Module 31")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 93")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
