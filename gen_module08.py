from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module08_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/08_white_nuthatch.jpg"

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
    stats=[("Length","5.1 – 5.5 in  (13 – 14 cm)"),
           ("Wingspan","7.9 – 10.6 in  (20 – 27 cm)"),
           ("Weight","0.6 – 1.1 oz  (18 – 30 g)"),
           ("Lifespan","Up to 10 years (avg. 2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c, x, y, bw):
    rows=[("Crown & nape (male)","Glossy black cap"),
          ("Crown (female)","Dark gray — not black"),
          ("Back & wings","Blue-gray"),
          ("Face & underparts","White to pale"),
          ("Flanks & undertail","Rusty chestnut-orange"),
          ("Bill","Long, pointed, dark gray")]
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
    chrome(c, 22, "Module 08 of 40")
    content=[Table([[Paragraph("MODULE  08  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("White-breasted Nuthatch",S_TITLE),
              Paragraph("Sitta carolinensis",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The White-breasted Nuthatch is one of the most distinctive and entertaining "
            "birds to visit backyard feeders — instantly recognizable by its habit of "
            "walking headfirst down tree trunks, a behavior unique among North American "
            "birds. This remarkable feat is made possible by an unusually large hind toe "
            "that provides a powerful grip regardless of orientation. Compact, neckless, "
            "and boldly patterned in black, white, and blue-gray, it is a year-round "
            "resident that pairs for life and maintains a fixed territory through all "
            "seasons. Its loud, nasal calls are among the most recognizable winter "
            "sounds in eastern North American forests.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The White-breasted Nuthatch is found across most of the United States "
            "and southern Canada, from British Columbia east to Nova Scotia and south "
            "through the Appalachians and into Mexico. It inhabits mature deciduous and "
            "mixed forests, forest edges, orchards, parks, and wooded suburban gardens "
            "with large trees. It shows a strong preference for oak, hickory, and "
            "beech-dominated forests where its primary wild food — acorns and nuts — "
            "is abundant. It is a permanent resident throughout its range and does "
            "not migrate.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Sunflower seeds — black-oil and striped both accepted",
              "Suet cakes — especially valued in winter",
              "Whole and shelled peanuts",
              "Acorns and hickory nuts (cached in bark crevices)",
              "Insects and spiders gleaned from bark year-round",
              "Peanut butter mixtures smeared into bark furrows"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c, 23, "White-breasted Nuthatch")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("White-breasted Nuthatches are monogamous and maintain year-round pair "
            "bonds, with mates staying in close contact through constant soft calls. "
            "They are vigorously territorial, with pairs defending the same woodland "
            "territory across multiple years. Their signature head-down foraging posture "
            "gives them a unique advantage: they can spot insects and cached food items "
            "hidden in bark crevices from angles that upward-foraging birds like "
            "woodpeckers would miss entirely. They are avid food cachers, wedging seeds "
            "and nuts into bark furrows and covering them with lichen or bark fragments "
            "— a behavior that has earned them the folk name \"Devil Downhead\" in "
            "some regions. They often join winter foraging flocks with chickadees "
            "and Downy Woodpeckers.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Breeding begins in March or April. Pairs use natural tree cavities, "
            "old woodpecker holes, or nest boxes, with the female doing most of the "
            "nest building. She constructs a cup of bark strips, grasses, and fur "
            "inside the cavity. A fascinating defensive behavior: the pair rubs "
            "crushed insects (particularly blister beetles) around the entrance hole "
            "— the noxious chemicals may deter squirrels and other predators. Clutches "
            "of 5–9 white eggs speckled with red-brown are incubated by the female "
            "for 13–14 days. Both parents feed the nestlings, which fledge at "
            "26 days — an unusually long nestling period.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The White-breasted Nuthatch is one of the most vocal winter birds. "
            "Its primary call is a loud, nasal \"yank yank yank\" — a rapid series "
            "that carries well through winter woodland. A softer, higher \"ip\" contact "
            "call keeps pairs in touch while foraging. The male's song, heard mostly "
            "in late winter and early spring, is a rapid series of low whistled notes "
            "\"whi-whi-whi-whi\" repeated several times. Females also vocalize "
            "frequently with soft nasal calls.",S_BODY),
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
        Paragraph("The White-breasted Nuthatch population is estimated at approximately "
            "10 million individuals and is considered stable. It benefits from the "
            "retention of large mature trees with natural cavities, and from nest box "
            "programs in managed forests. Forest fragmentation and the loss of old-"
            "growth deciduous woodland are the primary long-term concerns for this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Offer sunflower seeds in a tube or hopper feeder near large trees",
              "A suet cage mounted on a tree trunk is ideal for nuthatches",
              "Smear peanut butter into bark crevices — they will find it quickly",
              "Install a nest box with a 1.25–1.5 inch entrance hole on a large tree",
              "Nuthatches cache seeds — place feeders near rough-barked oaks or maples"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"White-breasted Nuthatch  •  Sitta carolinensis  •  Module 08")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 24")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
