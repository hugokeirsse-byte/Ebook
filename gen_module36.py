from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module36_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/36_downy_woodpecker.jpg"

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
    stats=[("Length","5.5 – 6.7 in  (14 – 17 cm)"),
           ("Wingspan","9.8 – 11.8 in  (25 – 30 cm)"),
           ("Weight","0.7 – 1.0 oz  (21 – 28 g)"),
           ("Lifespan","Up to 11 years (avg. 1–2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back","White stripe down center — key field mark"),
          ("Wings","Black with white spots and bars"),
          ("Head (male)","Black and white with red nape patch"),
          ("Head (female)","Black and white — no red"),
          ("Underparts","Clean white"),
          ("Bill","Short, chisel-shaped, dark gray")]
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
    chrome(c,106,"Module 36 of 40")
    content=[Table([[Paragraph("MODULE  36  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Downy Woodpecker",S_TITLE),
              Paragraph("Dryobates pubescens",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Downy Woodpecker is the smallest woodpecker in North America "
            "and one of the most familiar and beloved backyard birds on the "
            "continent — a crisp black-and-white sprite, barely larger than a "
            "sparrow, that clings acrobatically to suet feeders, sunflower "
            "feeders, and the branches of garden trees throughout the year. "
            "Its bold pattern — white back stripe, spotted wings, and the male's "
            "small red nape patch — makes it immediately recognizable. It is "
            "among the most frequent visitors to backyard feeding stations "
            "across North America, and its gentle, confiding nature makes it "
            "a favorite of beginning and experienced birders alike.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Downy Woodpecker is a year-round resident across most of "
            "North America, from Alaska and southern Canada south through the "
            "entire contiguous United States. It is absent only from the arid "
            "Southwest and treeless grasslands. It inhabits deciduous and mixed "
            "forests, woodland edges, orchards, suburban parks, and backyard "
            "gardens with mature trees. It is the most widespread woodpecker "
            "in North America and one of the few that regularly visits "
            "suburban feeders year-round.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Insect larvae and beetle grubs excavated from bark and wood",
              "Suet — the single most reliable feeder attractant for this species",
              "Black-oil sunflower seeds and sunflower chips",
              "Ants, caterpillars, and spiders gleaned from bark surfaces",
              "Wild berries and small fruits taken occasionally",
              "Sap from sapsucker wells in winter and early spring"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,107,"Downy Woodpecker")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Downy Woodpeckers are among the most acrobatic of feeder birds, "
            "clinging to vertical suet cages, hanging from sunflower feeders, "
            "and working their way along the undersides of small branches with "
            "ease. They use their stiff tail feathers as a prop against bark "
            "surfaces — a trait shared with all woodpeckers. Outside the "
            "breeding season, Downy Woodpeckers often join mixed foraging "
            "flocks with chickadees, nuthatches, and titmice — a strategy "
            "that improves predator detection. Males and females partition "
            "foraging space: males tend to forage on small branches and "
            "weed stems, females on larger trunks and branches.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Both sexes excavate a nest cavity in a dead tree or snag, "
            "typically 5–50 feet above the ground, over 1–3 weeks. The "
            "entrance hole is about 1.25 inches in diameter. No nesting "
            "material is added — eggs are laid on wood chips. Clutches of "
            "3–8 white eggs are incubated by both parents for 11–12 days, "
            "with the male incubating at night. Both parents feed the "
            "nestlings, which fledge at 20–25 days. One brood per season. "
            "Old cavities are used by many other species.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Downy Woodpecker's most distinctive sound is its \"pik\" "
            "call — a sharp, high-pitched single note given frequently as "
            "the bird forages. In spring, both sexes drum on resonant wood "
            "to advertise territory and attract mates — a rapid, even roll "
            "of about 15 beats per second. The whinny call — a descending, "
            "laughing series of notes — is given in territorial encounters. "
            "The Downy's drum is faster and higher-pitched than the "
            "similar Hairy Woodpecker's.",S_BODY),
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
        Paragraph("The Downy Woodpecker population is estimated at 14 million "
            "individuals in North America and has declined modestly in recent "
            "decades, largely due to the loss of dead trees and snags used "
            "for nesting. Retaining dead trees and large snags in yards and "
            "woodlands is the single most effective conservation action. "
            "Suet feeders provide critical winter energy, and planting "
            "native trees that host insect larvae supports year-round "
            "foraging.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Suet in a cage feeder is the top attractant — use year-round",
              "Sunflower chips and black-oil sunflower seeds also readily taken",
              "A tail-prop suet cage (open bottom) mimics natural bark foraging posture",
              "Leave dead branches and snags on trees — essential for nesting and foraging",
              "Downies are often the first woodpecker to discover a new feeder"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Downy Woodpecker  •  Dryobates pubescens  •  Module 36")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 108")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
