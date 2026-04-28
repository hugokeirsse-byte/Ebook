from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module27_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/27_eastern_bluebird.jpg"

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
    stats=[("Length","6.3 – 8.3 in  (16 – 21 cm)"),
           ("Wingspan","9.8 – 12.6 in  (25 – 32 cm)"),
           ("Weight","1.0 – 1.1 oz  (28 – 32 g)"),
           ("Lifespan","Up to 10 years (avg. 2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back & wings (male)","Brilliant royal blue"),
          ("Breast & flanks (male)","Rich chestnut-orange"),
          ("Belly (male)","White"),
          ("Female — back","Blue-gray with blue tinge on wings"),
          ("Female — breast","Pale orange-buff, washed"),
          ("Bill","Short, slightly curved, dark")]
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
    chrome(c,79,"Module 27 of 40")
    content=[Table([[Paragraph("MODULE  27  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Eastern Bluebird",S_TITLE),
              Paragraph("Sialia sialis",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Eastern Bluebird is one of the most beloved birds in North America "
            "— a small thrush whose brilliant royal-blue back, warm chestnut breast, "
            "and pure white belly create one of the most beautiful color combinations "
            "in the natural world. Henry David Thoreau wrote that \"the bluebird carries "
            "the sky on his back,\" a description that remains apt. Once in severe "
            "decline due to competition from introduced House Sparrows and European "
            "Starlings for nest cavities, the Eastern Bluebird staged one of the most "
            "dramatic conservation comebacks in North American history — driven almost "
            "entirely by the efforts of volunteers erecting nest box trails across "
            "the continent.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Eastern Bluebird is found year-round across the eastern United "
            "States, from the Great Plains east to the Atlantic coast, and from "
            "southern Canada south to Nicaragua. Northern populations are partially "
            "migratory, moving south in winter. It inhabits open country with "
            "scattered trees: orchards, golf courses, roadsides, parks, open "
            "woodlands, pastures with fence posts, and suburban gardens with "
            "short grass and nearby trees. It is a cavity nester that depends "
            "entirely on pre-existing holes in trees or nest boxes.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Live or dried mealworms — the single most effective food offering",
              "Wild berries: holly, dogwood, viburnum, pokeweed, Virginia creeper",
              "Insects and earthworms — the dominant food in warm months",
              "Bluebird-specific feeders with mealworm dishes",
              "Small fruits: serviceberry, hackberry, wild grape",
              "Rarely visits seed feeders — mealworms are essential"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,80,"Eastern Bluebird")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Eastern Bluebirds are gentle, sociable birds that form family groups "
            "through the breeding season, with offspring from earlier broods sometimes "
            "helping feed their younger siblings. In winter they gather in loose "
            "flocks of 10–20 birds that roam open country in search of berry crops. "
            "They hunt insects by perching on a low branch or fence post, scanning "
            "the ground below, then dropping to capture prey — a hunting style called "
            "\"drop-hunting\" or \"flycatching from a perch.\" They communicate with "
            "each other constantly using soft, melodious warbling calls that carry "
            "a quality of gentle contentment.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Eastern Bluebirds are cavity nesters, using old woodpecker holes "
            "and nest boxes. The female builds a neat cup of grasses and pine needles "
            "inside the cavity. Clutches of 4–6 pale blue (or occasionally white) "
            "eggs are incubated by the female for 13–16 days. Both parents and "
            "sometimes helper birds feed the nestlings, which fledge at 17–21 days. "
            "Pairs raise 2–3 broods per season. Aggressive monitoring and eviction "
            "of House Sparrows from nest boxes is essential for bluebird nesting "
            "success.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Eastern Bluebird's song is a soft, rich, melodious warble — "
            "a series of flowing phrases with a gentle, liquid quality. It is one "
            "of the most pleasant sounds of early spring in eastern North America, "
            "beginning on warm late-winter days. The call is a distinctive, "
            "soft \"tru-ly\" or \"chur-wi\" whistle that is easily recognized "
            "once learned. Males sing persistently from exposed perches "
            "throughout the breeding season.",S_BODY),
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
        Paragraph("The Eastern Bluebird population is estimated at 22 million individuals "
            "and has increased dramatically since the 1970s, rebounding from severe "
            "mid-20th-century declines. This recovery is one of the great citizen "
            "science success stories — driven by thousands of volunteers maintaining "
            "nest box trails across the continent. Installing and actively managing "
            "nest boxes remains the single most impactful action any individual can "
            "take for this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Offer live or dried mealworms in a shallow dish feeder near open grass",
              "Use a bluebird-specific feeder with a small entry hole to exclude starlings",
              "Install a nest box (1.5-inch entrance) on a post in open area, 5 ft high",
              "Monitor boxes weekly — evict House Sparrow nests immediately",
              "Plant native berry-producing shrubs: holly, dogwood, and serviceberry"]:
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
    c.drawCentredString(W/2,H-0.66*inch,"Eastern Bluebird  •  Sialia sialis  •  Module 27")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 81")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
