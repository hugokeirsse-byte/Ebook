from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module35_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/35_house_wren.jpg"

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
    stats=[("Length","4.3 – 5.1 in  (11 – 13 cm)"),
           ("Wingspan","5.9 in  (15 cm)"),
           ("Weight","0.3 – 0.4 oz  (10 – 12 g)"),
           ("Lifespan","Up to 9 years (avg. 1–2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back & wings","Warm brown with fine dark barring"),
          ("Underparts","Pale buff-gray, washed brown on flanks"),
          ("Tail","Short, often cocked upward — brown, barred"),
          ("Eyebrow stripe","Faint pale supercilium"),
          ("Throat & breast","Pale gray-white"),
          ("Bill","Slender, slightly decurved, dark")]
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
    chrome(c,103,"Module 35 of 40")
    content=[Table([[Paragraph("MODULE  35  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("House Wren",S_TITLE),
              Paragraph("Troglodytes aedon",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The House Wren is one of the most energetic and vocally exuberant "
            "birds in North America — a tiny, plain brown bird that erupts into "
            "a cascading, bubbling song far too large for its small body. "
            "Weighing barely a third of an ounce, it is among the most widely "
            "distributed birds in the Western Hemisphere, breeding from Canada "
            "to the southern tip of South America. Its scientific name, "
            "Troglodytes aedon, means \"cave-dweller singer\" — a fitting "
            "description for a bird that nests in any available cavity and fills "
            "the surrounding area with exuberant song. It is a faithful and "
            "enthusiastic user of nest boxes, making it one of the easiest "
            "cavity-nesting birds to attract to a backyard.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The House Wren breeds across virtually all of North America south "
            "of the boreal tree line, from British Columbia to the Maritime "
            "provinces and south through most of the United States. It winters "
            "along the Gulf Coast, in Florida, and through Mexico and Central "
            "America. It inhabits woodland edges, suburban gardens, orchards, "
            "farmyards, and any area with shrubby vegetation near open land. "
            "It is highly adaptable and readily nests in nest boxes, flower "
            "pots, old boots, and virtually any enclosed cavity near human "
            "habitation.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Insects and insect larvae — the near-exclusive diet",
              "Spiders gleaned from bark, foliage, and wood piles",
              "Beetles, ants, earwigs, and grasshoppers",
              "Caterpillars and moth larvae from leaf surfaces",
              "Occasionally small snails and millipedes",
              "Does not visit seed feeders — mealworms rarely taken"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,104,"House Wren")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Despite its small size, the House Wren is one of the most "
            "assertive and territorially aggressive birds at the nest box. "
            "Males arrive on the breeding grounds before females and immediately "
            "begin filling every available nest cavity with sticks — a behavior "
            "called \"dummy nesting\" that blocks competing species from using "
            "the cavities. They will pierce the eggs of other cavity-nesting "
            "birds — including bluebirds and Tree Swallows — in neighboring "
            "boxes. The male's song, delivered from an exposed perch near the "
            "nest box, is a rapid, bubbling cascade that serves as both a "
            "territorial proclamation and a courtship advertisement.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("The male fills a nest box with small sticks, then the female "
            "selects her preferred cavity and builds the actual nest cup of "
            "fine grasses, feathers, and hair atop the stick base. She lays "
            "3–10 white eggs with reddish-brown speckles and incubates them "
            "alone for 13–15 days. Both parents feed the nestlings, which "
            "fledge at 15–17 days. Pairs typically raise 2 broods per season. "
            "House Wrens will use nest boxes with a 1.25-inch entrance hole, "
            "which excludes European Starlings.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The House Wren's song is a long, exuberant cascade of bubbling, "
            "liquid notes that descends and rises in rapid succession — one of "
            "the most complex and energetic songs produced by any bird of its "
            "size. Males sing persistently throughout the day from April through "
            "July. The call is a sharp, scolding \"chatter\" — a rapid, harsh "
            "rattle given aggressively near the nest. The contrast between the "
            "plain brown plumage and the spectacular vocal performance is one "
            "of the great surprises of backyard birding.",S_BODY),
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
        Paragraph("The House Wren population is estimated at 160 million individuals "
            "across the Western Hemisphere and is broadly stable. In North "
            "America alone, around 9 million breed annually. It has benefited "
            "from the proliferation of nest boxes and the fragmentation of "
            "forest into the shrubby edges it prefers. Maintaining nest boxes "
            "and reducing pesticide use to preserve insect prey are the most "
            "effective ways to support this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Put up a nest box with a 1.25-inch hole — wrens take them readily",
              "Place the box 4–6 feet high on a post or fence, near shrubby cover",
              "House Wrens do not visit seed feeders — focus on habitat, not food",
              "Keep multiple boxes spaced apart to reduce competition with bluebirds",
              "Clean out old nests between broods to reduce parasites and encourage re-nesting"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"House Wren  •  Troglodytes aedon  •  Module 35")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 105")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
