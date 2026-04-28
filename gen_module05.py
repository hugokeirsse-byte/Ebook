from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module05_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/05_ruby_hummingbird.jpg"

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

def sp(name, font, size, color=DARK, leading=None, align=TA_LEFT, sb=0, sa=0):
    return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color,
        leading=leading or size*1.45, alignment=align, spaceBefore=sb, spaceAfter=sa)

S_TITLE = sp("T",  "Helvetica-Bold",   28, G_DARK, 34)
S_LAT   = sp("L",  "Helvetica-Oblique",11, GREY,   16, sa=6)
S_HDR   = sp("H",  "Helvetica-Bold",    9, G_MID,  13, sb=10, sa=3)
S_BODY  = sp("B",  "Helvetica",        10, DARK,   15, align=TA_JUSTIFY)
S_BUL   = sp("BU", "Helvetica",        10, DARK,   14, sb=1)

class GoldLine(Flowable):
    def __init__(self, w):
        super().__init__(); self.width=w; self.height=10
    def draw(self):
        c=self.canv; c.setStrokeColor(GOLD); c.setLineWidth(0.8)
        c.line(0,5,self.width,5); c.setFillColor(GOLD); m=self.width/2
        p=c.beginPath(); p.moveTo(m,10); p.lineTo(m+5,5); p.lineTo(m,0); p.lineTo(m-5,5); p.close()
        c.drawPath(p,fill=1,stroke=0)

def chrome(c, pnum, sub=""):
    c.setFillColor(G_DARK); c.rect(0,H-MT,W,MT,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,H-0.32*inch,"BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    if sub: c.drawRightString(W-MR,H-0.32*inch,sub)
    c.setFillColor(CREAM); c.rect(0,0,W,H-MT,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica",8)
    c.drawCentredString(W/2,0.28*inch,f"— {pnum} —")

def draw_stats(c, x, y, bw):
    stats=[("Length","2.8 – 3.5 in  (7 – 9 cm)"),
           ("Wingspan","3.1 – 4.3 in  (8 – 11 cm)"),
           ("Weight","0.07 – 0.21 oz  (2 – 6 g)"),
           ("Lifespan","Up to 9 years (avg. 3–5 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c, x, y, bw):
    rows=[("Back & crown (both)","Iridescent emerald green"),
          ("Gorget — male throat","Ruby red (may look black)"),
          ("Breast & belly","White to pale gray"),
          ("Tail (male)","Forked, dark green-black"),
          ("Female throat","White, no red gorget"),
          ("Bill","Long, straight, black")]
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
    chrome(c, 13, "Module 05 of 40")
    content=[Table([[Paragraph("MODULE  05  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Ruby-throated Hummingbird",S_TITLE),
              Paragraph("Archilochus colubris",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Ruby-throated Hummingbird is the only hummingbird species that regularly "
            "breeds in eastern North America, and one of the most extraordinary birds on the "
            "continent. Weighing less than a nickel, it is a marvel of biological engineering: "
            "its wings beat 53 times per second, its heart beats up to 1,200 times per minute "
            "during flight, and it is the only bird capable of sustained backwards flight. "
            "The male's iridescent ruby-red gorget (throat patch) can appear jet black in "
            "poor lighting, then flash brilliant red as the angle of light changes — "
            "one of nature's most spectacular optical effects.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("During summer, the Ruby-throated Hummingbird breeds across the entire eastern "
            "half of North America, from Nova Scotia and Manitoba south through Florida and "
            "west to the Great Plains. It inhabits forest edges, gardens, orchards, and "
            "meadows with abundant flowering plants. Each fall, it undertakes one of the most "
            "astonishing migrations in the bird world: a non-stop flight of 500–900 miles "
            "across the Gulf of Mexico to its wintering grounds in Mexico and Central America. "
            "It returns north each spring from April through May.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Flower nectar — trumpetvine, salvia, monarda, impatiens",
              "Feeder solution: 1 part white sugar to 4 parts water (no dye)",
              "Tiny insects and spiders — essential protein source",
              "Tree sap from sapsucker wells (used opportunistically)",
              "Never use honey, artificial sweeteners, or red dye in feeders"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c, 14, "Ruby-throated Hummingbird")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Ruby-throated Hummingbirds are among the most aggressively territorial "
            "birds in North America relative to their size. Males fiercely defend feeding "
            "territories, dive-bombing intruders — including birds many times their size — "
            "with surprising ferocity. Outside of courtship and mating, males and females "
            "live entirely solitary lives. To survive cold nights and food shortages, "
            "hummingbirds enter a state of torpor: their body temperature drops from 40°C "
            "to around 18°C, their heart rate falls from 1,200 to just 50 beats per minute, "
            "and their breathing nearly stops. This metabolic shutdown can save up to 60% "
            "of their nightly energy expenditure.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("The female alone builds one of nature's most remarkable nests: a walnut-"
            "sized cup of plant down and spider silk, camouflaged on the outside with "
            "lichens, and expandable as the chicks grow. It is typically placed on a "
            "slender downward-sloping branch 10–20 feet above ground. She lays exactly "
            "2 white eggs the size of peas, incubating them alone for 11–14 days. "
            "She feeds the nestlings by inserting her bill deep into their throats and "
            "regurgitating nectar and insects. Young fledge at 18–22 days. The male "
            "plays no role in nesting or chick-rearing.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("Ruby-throated Hummingbirds are not known for melodious song. Their "
            "primary vocalizations are sharp, rapid chips and chattering calls used during "
            "territorial disputes and pursuit chases. Males perform spectacular U-shaped "
            "or pendulum dive displays during courtship, producing a distinctive "
            "wing-buzz at the bottom of each arc. The wingbeat itself produces the "
            "characteristic humming sound that gives the family its name.",S_BODY),
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
        Paragraph("With a stable population estimated at nearly 34 million individuals, the "
            "Ruby-throated Hummingbird is not currently threatened. However, it faces "
            "pressure from habitat loss on its wintering grounds in Central America and "
            "from climate change affecting the timing of flower blooms relative to migration. "
            "Planting native nectar plants and maintaining clean feeders are the most "
            "impactful ways to support local populations.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Use a red feeder — no need to add dye to the solution",
              "Recipe: boil 1 cup white sugar in 4 cups water, cool completely",
              "Change solution every 2–3 days in hot weather to prevent fermentation",
              "Clean feeders with hot water and a bottle brush — no soap needed",
              "Hang feeders by late April in the South, mid-May in the North",
              "Plant trumpet vine, bee balm, salvia, and cardinal flower nearby"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Ruby-throated Hummingbird  •  Archilochus colubris  •  Module 05")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 15")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
