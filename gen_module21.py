from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module21_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/21_house_finch.jpg"

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
    stats=[("Length","5.1 – 5.5 in  (13 – 14 cm)"),
           ("Wingspan","7.9 – 9.8 in  (20 – 25 cm)"),
           ("Weight","0.6 – 0.9 oz  (16 – 27 g)"),
           ("Lifespan","Up to 11 years (avg. 2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Head & breast (male)","Rosy red — intensity varies by diet"),
          ("Rump (male)","Bright red — key field mark"),
          ("Back & wings","Brown, streaked dark"),
          ("Belly","White with brown streaking"),
          ("Female — overall","Brown, heavily streaked — no red"),
          ("Bill","Short, curved, conical, pale")]
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
    chrome(c,61,"Module 21 of 40")
    content=[Table([[Paragraph("MODULE  21  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("House Finch",S_TITLE),
              Paragraph("Haemorhous mexicanus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The House Finch is one of the most familiar and abundant feeder birds "
            "in North America — a cheerful, sociable finch whose rosy-red male is a "
            "year-round fixture at sunflower feeders from coast to coast. Native to "
            "the western United States and Mexico, the House Finch was illegally sold "
            "as a cage bird (marketed as \"Hollywood Finches\") in New York in the "
            "1940s. When dealers faced prosecution under the Migratory Bird Act, they "
            "released their birds on Long Island — and from that small population, "
            "the species colonized the entire eastern United States within 50 years, "
            "one of the most remarkable range expansions in North American ornithological "
            "history. Today it is among the top five most abundant feeder birds nationally.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The House Finch is now found year-round across virtually the entire "
            "contiguous United States, southern Canada, and Mexico. It thrives in "
            "human-modified landscapes: suburban gardens, parks, farmland, orchards, "
            "and city centers. It is rarely found in dense forest or wilderness, "
            "strongly preferring areas with buildings, feeders, and ornamental "
            "plantings. It is a permanent resident throughout its range and does "
            "not migrate, though local movements occur in response to food availability.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Black-oil sunflower seeds — the top feeder choice",
              "Nyjer (thistle) seed — eagerly taken from tube feeders",
              "Safflower seeds and sunflower chips",
              "Wild weed seeds: dandelion, thistle, mustard, knotweed",
              "Wild berries and small fruits — especially in autumn",
              "Flower buds and petals in spring"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,62,"House Finch")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("House Finches are highly gregarious, forming flocks of up to several "
            "hundred birds outside the breeding season. They are boisterous and "
            "active at feeders, often arriving in chattering waves and dominating "
            "smaller birds. The intensity of the male's red coloration is entirely "
            "diet-dependent — birds with access to carotenoid-rich foods such as "
            "berries and fruits develop deeper, more saturated reds, while those "
            "on poor diets may be pale orange or even yellowish. Females use this "
            "color intensity as a reliable indicator of male quality when choosing "
            "a mate. House Finches are highly adaptable and frequently nest on "
            "buildings, in hanging baskets, and in wreaths.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("House Finches are prolific and flexible nesters. They build compact "
            "cup nests of grasses, leaves, and rootlets in a wide variety of sites "
            "— tree cavities, dense shrubs, building ledges, hanging planters, and "
            "even old nests of other species. The female incubates 2–6 pale blue "
            "eggs with fine dark spots for 13–14 days. The male feeds the female "
            "during incubation. Both parents feed the nestlings regurgitated seeds, "
            "which fledge at 12–19 days. Pairs raise 2–3 broods per season, "
            "sometimes beginning in February in southern areas.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The House Finch's song is a bright, rambling warble of musical "
            "phrases — cheerful, variable, and delivered with great energy from "
            "a prominent perch. Males sing year-round, including on cold winter "
            "days. The call is a sharp \"wheet\" or rising \"wiit.\" House Finches "
            "are one of the most frequent singers at winter feeders, often heard "
            "before they are seen.",S_BODY),
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
        Paragraph("The House Finch population is estimated at 267 million individuals "
            "but has declined noticeably since the mid-1990s, largely due to an "
            "epidemic of Mycoplasmal conjunctivitis — a bacterial eye disease that "
            "spread rapidly through feeder populations beginning in 1994. Keeping "
            "feeders scrupulously clean is the single most important action feeder "
            "owners can take to protect House Finch populations.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Black-oil sunflower seeds in a tube feeder are the top attraction",
              "Clean feeders thoroughly every 1–2 weeks — House Finches are prone to eye disease",
              "Remove and discard any birds seen with swollen, crusty eyes immediately",
              "Nyjer feeders bring in mixed flocks of House Finches and goldfinches",
              "House Finches nest on buildings — a hanging planter may become a nest site"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"House Finch  •  Haemorhous mexicanus  •  Module 21")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 63")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
