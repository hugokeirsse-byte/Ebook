from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module06_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/06_american_robin.jpg"

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
    c.drawCentredString(W/2,0.16*inch,f"— {pnum} —")

def draw_stats(c, x, y, bw):
    stats=[("Length","7.9 – 11.0 in  (20 – 28 cm)"),
           ("Wingspan","12.2 – 15.7 in  (31 – 40 cm)"),
           ("Weight","2.7 – 3.0 oz  (77 – 85 g)"),
           ("Lifespan","Up to 14 years (avg. 2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c, x, y, bw):
    rows=[("Head & back","Dark gray to black"),
          ("Breast & belly","Brick orange-red"),
          ("Throat","White with dark streaks"),
          ("White eye-ring","Pure white crescent"),
          ("Bill","Yellow-orange"),
          ("Legs & feet","Dark brown-gray")]
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
    chrome(c, 16, "Module 06 of 40")
    content=[Table([[Paragraph("MODULE  06  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("American Robin",S_TITLE),
              Paragraph("Turdus migratorius",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The American Robin is one of the most familiar and beloved birds in North "
            "America — a true symbol of spring whose return each year is eagerly anticipated "
            "across the continent. Plump, upright, and boldly patterned with its signature "
            "orange-red breast, it is a consummate garden bird, foraging confidently across "
            "lawns for earthworms and nesting on ledges, trees, and even window sills in "
            "close proximity to humans. Despite being called a robin, it is actually a "
            "thrush — a member of the same family as bluebirds and solitaires — and is "
            "the largest thrush in North America.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The American Robin breeds across virtually all of North America, from "
            "Alaska and northern Canada south through Mexico, making it one of the "
            "continent's most widespread birds. It inhabits an extraordinary range of "
            "environments: lawns, parks, forests, mountains up to the treeline, tundra "
            "edges, and urban centers. Northern populations migrate south in autumn, "
            "though many winter in the southern US where berry-laden trees provide food. "
            "Year-round residents are common throughout much of the contiguous United "
            "States. Large winter flocks of thousands can gather in roosts.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Earthworms — located by sight and sound, not smell",
              "Wild berries: holly, crabapple, juniper, dogwood, cedar",
              "Insects, beetles, grasshoppers, and caterpillars",
              "Fruit: grapes, cherries, plums, serviceberry",
              "Rarely visits seed feeders — prefers open ground foraging",
              "Plant berry-producing shrubs to attract robins to your garden"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c, 17, "American Robin")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("American Robins are highly visible and active birds, spending much of "
            "their time foraging on the ground with a characteristic run-stop-tilt posture "
            "as they listen and watch for earthworms. Contrary to popular belief, they "
            "locate worms primarily by sight rather than hearing, though both senses play "
            "a role. Outside breeding season, robins are highly gregarious, forming "
            "communal roosts of thousands or even millions of birds in woodlands. These "
            "roosts disperse each morning as birds fan out to forage, then reconvene at "
            "dusk. Males arrive on breeding grounds before females each spring and "
            "immediately begin singing to establish territories.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("The American Robin is one of the earliest nesters in North America, "
            "often beginning as soon as late February in the South. The female builds a "
            "robust cup nest of grasses, twigs, and worm castings, reinforced with mud "
            "and lined with fine grasses. Nests are placed on building ledges, in tree "
            "forks, or on fence posts 5–15 feet above ground. The female lays 3–5 eggs "
            "of a vivid, unmistakable sky blue — the origin of the color name \"robin's "
            "egg blue.\" Incubation lasts 12–14 days. Both parents feed nestlings, which "
            "fledge at 13 days. Pairs typically raise 2–3 broods per season.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The robin's song is one of the most recognized sounds of the North "
            "American spring — a rich, melodious caroling of rising and falling phrases "
            "often transcribed as \"cheerily, cheer-up, cheerio.\" Males begin singing "
            "before dawn and continue into dusk, sometimes even singing after dark near "
            "artificial lights. The sharp \"tut-tut-tut\" alarm call warns of ground "
            "predators, while a high thin \"seee\" alerts to aerial threats. Robins are "
            "among the first birds to sing in the morning chorus.",S_BODY),
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
        Paragraph("With an estimated population of 300 million individuals, the American "
            "Robin is one of the most abundant birds in North America. Its adaptability "
            "to human-modified landscapes has helped it thrive despite widespread habitat "
            "changes. It does face localized threats from pesticide use, which reduces "
            "earthworm availability and can cause direct poisoning.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Robins rarely use seed feeders — attract them differently",
              "Install a shallow birdbath: robins love to bathe and drink",
              "Plant holly, crabapple, dogwood, or serviceberry for winter berries",
              "Avoid pesticides on lawns — robins depend on healthy earthworm populations",
              "A platform feeder with mealworms or fruit pieces may attract them"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"American Robin  •  Turdus migratorius  •  Module 06")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 18")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
