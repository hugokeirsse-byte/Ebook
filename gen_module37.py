from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module37_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/37_northern_flicker.jpg"

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
    stats=[("Length","11.0 – 12.2 in  (28 – 31 cm)"),
           ("Wingspan","16.5 – 20.1 in  (42 – 51 cm)"),
           ("Weight","3.9 – 5.6 oz  (110 – 160 g)"),
           ("Lifespan","Up to 9 years (avg. 4–5 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back & wings","Brown with bold black barring"),
          ("Breast & belly","Pale buff with bold black spots"),
          ("Chest crescent","Bold black — key field mark"),
          ("Rump","White — flashes in flight"),
          ("Wing/tail linings","Yellow (East) or red (West)"),
          ("Head (male)","Gray crown, red nape, black moustache")]
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
    chrome(c,109,"Module 37 of 40")
    content=[Table([[Paragraph("MODULE  37  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Northern Flicker",S_TITLE),
              Paragraph("Colaptes auratus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Northern Flicker is one of the most distinctive and elaborately "
            "patterned woodpeckers in North America — a large, brown, heavily "
            "spotted bird that is unlike any other woodpecker in its preference "
            "for foraging on the ground rather than on tree trunks. In flight, "
            "its white rump patch flashes conspicuously, and the undersides of "
            "its wings and tail glow bright yellow (in the Yellow-shafted form "
            "of the East) or red (in the Red-shafted form of the West). "
            "The bold black chest crescent, spotted breast, and colorful "
            "wing linings make it unmistakable. It is the most terrestrial "
            "of all North American woodpeckers, spending much of its time "
            "probing lawns and open ground for ants.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Northern Flicker is a year-round resident across most of "
            "North America, from Alaska and northern Canada south through "
            "virtually all of the United States and into Central America. "
            "Northern populations are partially migratory. It inhabits open "
            "woodlands, forest edges, suburban parks, and any area combining "
            "open ground for foraging with trees for nesting. It readily "
            "visits suburban lawns and is one of the most widespread "
            "woodpeckers on the continent.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Ants — the dominant food; digs them from lawns and soil with its long tongue",
              "Beetles, grubs, and insect larvae from rotting wood",
              "Wild berries: dogwood, elderberry, sumac, poison ivy, hackberry",
              "Sunflower seeds and suet at feeders — less common than other woodpeckers",
              "Grasshoppers and crickets taken from open ground",
              "Occasionally visits platform feeders for peanuts or corn"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,110,"Northern Flicker")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("The Northern Flicker is the only woodpecker that regularly hops "
            "across open ground, using its long, barbed, sticky tongue to "
            "extract ants from their underground colonies. It consumes more "
            "ants than any other North American bird — a single stomach may "
            "contain over 5,000 ants. Despite spending much time on the "
            "ground, it is also an accomplished tree climber and excavates "
            "nest cavities like other woodpeckers. In spring, males drum "
            "loudly on resonant surfaces — including metal gutters, chimney "
            "caps, and utility poles — to establish territory, producing "
            "a territorial din that can be heard from great distances.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Northern Flickers excavate nest cavities in dead trees, snags, "
            "and wooden structures, typically 6–15 feet above the ground. "
            "The entrance hole is about 2.5 inches in diameter. Both sexes "
            "excavate over 1–4 weeks. Clutches of 5–8 white eggs are "
            "incubated by both parents for 11–16 days, with the male "
            "incubating at night. Both parents feed the nestlings, which "
            "fledge at 25–28 days. One brood per season. Old cavities "
            "are widely used by other cavity-nesting species.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Northern Flicker is one of the most vocal woodpeckers, "
            "producing a loud, ringing \"wicka-wicka-wicka\" call that "
            "carries through open woodland and suburban neighborhoods. "
            "It also gives a loud, single \"kleer\" call — an emphatic "
            "note used in territorial and courtship contexts. Spring "
            "drumming is rapid and powerful, often directed at metal "
            "surfaces for maximum resonance and volume. The \"flicker\" "
            "name derives from the flickering flash of color visible "
            "in flight.",S_BODY),
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
        Paragraph("The Northern Flicker population is estimated at 9 million "
            "individuals but has declined by roughly 49% since 1970 — "
            "one of the steeper declines among North American woodpeckers. "
            "Competition with European Starlings for nest cavities, loss "
            "of dead trees and snags, and pesticide-driven declines in "
            "ant populations are the primary drivers. Retaining snags, "
            "installing large nest boxes, and avoiding lawn pesticides "
            "are the most effective conservation actions.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Flickers rarely use feeders — suet and peanuts are occasionally taken",
              "The best attraction is a lawn with moist soil and abundant ants",
              "Retain dead trees and large snags — essential for nesting",
              "Install a large nest box (2.5-inch hole, 16 inches deep) on a pole",
              "Avoid lawn insecticides — ants are the flicker's primary food source"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Northern Flicker  •  Colaptes auratus  •  Module 37")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 111")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
