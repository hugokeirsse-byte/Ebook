from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module40_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/40_american_kestrel.jpg"

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
    stats=[("Length","8.7 – 12.2 in  (22 – 31 cm)"),
           ("Wingspan","20.1 – 24.0 in  (51 – 61 cm)"),
           ("Weight","2.8 – 5.8 oz  (80 – 165 g)"),
           ("Lifespan","Up to 17 years (avg. 3–5 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back (male)","Rufous-chestnut with black barring"),
          ("Wings (male)","Blue-gray — striking contrast with back"),
          ("Head","Blue-gray crown, white cheek, two black sideburns"),
          ("Breast & belly","Pale buff with dark spots"),
          ("Tail (male)","Rufous with black subterminal band"),
          ("Female — wings","Rufous-brown, heavily barred")]
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
    chrome(c,118,"Module 40 of 40")
    content=[Table([[Paragraph("MODULE  40  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("American Kestrel",S_TITLE),
              Paragraph("Falco sparverius",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The American Kestrel is the smallest and most colorful falcon in "
            "North America — a jewel-like bird of open country whose exquisite "
            "plumage and spirited hovering flight make it one of the most "
            "charismatic raptors on the continent. The male is unmistakable: "
            "a blue-gray wing against a rufous-chestnut back, a spotted "
            "buff breast, and two bold black \"sideburn\" marks on a "
            "white-cheeked face create a pattern unlike any other North "
            "American bird. Despite being a raptor, it is robin-sized, "
            "and its habit of perching on telephone wires along roadsides "
            "makes it one of the most commonly observed hawks in North "
            "America — a familiar sight to travelers across the continent.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The American Kestrel is a year-round resident across most of "
            "North America, breeding from Alaska and Canada south through "
            "the entire United States, Mexico, and Central America, and "
            "into South America. Northern populations migrate south in "
            "winter. It inhabits open and semi-open habitats: farmland, "
            "roadsides, grasslands, desert edges, suburban areas, and "
            "any open land with perch sites and prey. It is cavity-nesting "
            "and readily accepts nest boxes, making it one of the most "
            "successfully managed raptor species.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Grasshoppers and large insects — the primary summer food",
              "Mice, voles, and shrews — dominant prey in winter",
              "Small birds taken occasionally, especially in winter",
              "Lizards, small snakes, and frogs in warm climates",
              "Earthworms and beetles gleaned from open ground",
              "Hovers 20–30 feet above the ground to spot prey below"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,119,"American Kestrel")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("The American Kestrel is renowned for its hovering ability — "
            "it can hang nearly motionless in the air, facing into the "
            "wind, scanning the ground below with extraordinary visual "
            "acuity. Kestrels can see ultraviolet light, which allows "
            "them to detect the urine trails of voles — invisible to "
            "humans — leading directly to prey burrows. They are "
            "aggressive hunters despite their small size, taking prey "
            "as large as themselves. Outside the breeding season they "
            "are largely solitary and territorial. In winter, females "
            "tend to remain farther north than males.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("American Kestrels are obligate cavity nesters — they cannot "
            "excavate their own holes and depend entirely on existing "
            "cavities: natural tree hollows, old woodpecker holes, "
            "cliff crevices, and nest boxes. No nesting material is "
            "added. Clutches of 4–5 white to pale pink eggs with "
            "brown spotting are incubated by both parents for 29–31 "
            "days. Both parents feed the nestlings, which fledge at "
            "28–31 days. One brood per season. Nest box programs "
            "have successfully reversed local population declines.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The American Kestrel's call is a rapid, high-pitched "
            "\"klee-klee-klee\" or \"killy-killy-killy\" — a sharp, "
            "excited series that carries well across open farmland. "
            "It is frequently given in flight and when alarmed near "
            "the nest. Males give a softer \"whining\" call during "
            "courtship. The call is one of the most distinctive "
            "raptor vocalizations in North America and immediately "
            "announces the bird's presence even before it is seen.",S_BODY),
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
        Paragraph("The American Kestrel population has declined by approximately "
            "47% since 1966 — one of the steepest declines of any North "
            "American raptor. Loss of open farmland and grassland habitat, "
            "reduction in large insects from pesticide use, competition "
            "with European Starlings for nest cavities, and secondary "
            "poisoning from rodenticides are the primary drivers. "
            "Nest box programs along roadsides and field edges have "
            "demonstrated significant success in reversing local "
            "declines.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Kestrels do not visit bird feeders — open habitat and nest boxes are the key",
              "Install a kestrel nest box on a pole 10–30 feet high at the edge of open land",
              "Entrance hole should be 3 inches in diameter; box interior 9 x 9 x 12 inches",
              "Maintain open grassland or meadow nearby — essential foraging habitat",
              "Avoid rodenticides — poisoned prey causes secondary poisoning in kestrels"]:
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
    c.drawCentredString(W/2,H-0.66*inch,"American Kestrel  •  Falco sparverius  •  Module 40")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 120")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
