from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module12_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/12_whitethroated_sparrow.jpg"

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
    c.drawCentredString(W/2,0.28*inch,f"— {pnum} —")

def draw_stats(c,x,y,bw):
    stats=[("Length","6.3 – 7.1 in  (16 – 18 cm)"),
           ("Wingspan","7.9 – 9.1 in  (20 – 23 cm)"),
           ("Weight","0.8 – 1.1 oz  (22 – 32 g)"),
           ("Lifespan","Up to 9 years (avg. 3 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Crown stripes","Bold black & white alternating"),
          ("Yellow lore spot","Bright yellow — above bill/eye"),
          ("Throat patch","Clean white — sharply defined"),
          ("Back & wings","Brown, streaked dark"),
          ("Breast & belly","Gray-white, unstreaked"),
          ("Bill","Short, conical, pale gray-pink")]
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
    chrome(c,34,"Module 12 of 40")
    content=[Table([[Paragraph("MODULE  12  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("White-throated Sparrow",S_TITLE),
              Paragraph("Zonotrichia albicollis",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The White-throated Sparrow is a large, handsome sparrow and a beloved "
            "winter visitor to feeders across eastern and southern North America. Its bold "
            "head pattern — alternating black and white crown stripes, a tiny yellow spot "
            "between bill and eye, and a sharply defined white throat — makes it one of "
            "the easiest sparrows to identify. Its haunting, whistled song, often "
            "transcribed as \"Oh sweet Canada Canada Canada,\" is one of the most "
            "evocative sounds of the northern forest. The species comes in two distinct "
            "color morphs — white-striped and tan-striped — that interbreed freely "
            "but almost always choose mates of the opposite morph.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The White-throated Sparrow breeds in the boreal forests of Canada "
            "and the northeastern United States, from British Columbia east to "
            "Newfoundland, south through the northern Great Lakes states and New "
            "England. It winters across the eastern half of the United States south "
            "to Florida and the Gulf Coast, and in smaller numbers west to California. "
            "On its breeding grounds it inhabits the edges of boreal forests, "
            "regenerating clear-cuts, and shrubby bogs. In winter it frequents "
            "woodland edges, brushy thickets, hedgerows, and suburban gardens with "
            "dense shrub cover.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["White millet — the top choice at feeders",
              "Black-oil sunflower seeds and hulled chips",
              "Cracked corn scattered on the ground",
              "Wild weed seeds: ragweed, smartweed, knotweed",
              "Wild berries: dogwood, sumac, bayberry",
              "Insects and spiders during the breeding season"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,35,"White-throated Sparrow")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("White-throated Sparrows are gregarious in winter, foraging in flocks "
            "of 10–50 birds, often mixed with Dark-eyed Juncos, Song Sparrows, and "
            "other ground-feeding species. They are primarily ground feeders, scratching "
            "vigorously through leaf litter with a characteristic double-foot kick to "
            "expose buried seeds. The two color morphs — white-striped and tan-striped — "
            "represent a remarkable genetic polymorphism. White-striped birds are more "
            "aggressive and sing more frequently; tan-striped birds are better parents. "
            "Remarkably, nearly all mated pairs consist of one bird of each morph, "
            "a pattern maintained across the entire species.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("White-throated Sparrows nest on or near the ground in dense "
            "boreal shrub habitat. The female builds a cup nest of grasses, moss, "
            "and pine needles, hidden beneath shrubs or at the base of small trees. "
            "Clutches of 4–5 pale blue or greenish eggs with brown spotting are "
            "incubated by the female for 11–14 days. Both parents feed the nestlings, "
            "which fledge at 7–12 days. The species raises 1–2 broods per season. "
            "It is a frequent cowbird host on its breeding grounds.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The White-throated Sparrow's song is one of the most distinctive "
            "and beloved in North American birding — a clear, pure whistle often "
            "rendered as \"Old Sam Peabody Peabody Peabody\" or \"Oh sweet Canada "
            "Canada Canada.\" It consists of 2–3 long introductory notes followed "
            "by a series of triplets on a different pitch. Males sometimes sing on "
            "warm winter days, though song peaks on the breeding grounds. The call "
            "is a sharp, metallic \"chink.\"",S_BODY),
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
        Paragraph("The White-throated Sparrow population is estimated at 140 million "
            "individuals but has declined significantly — by roughly 30% — since 1970, "
            "largely due to loss of boreal forest breeding habitat from logging and "
            "climate change. Maintaining dense shrub cover in winter gardens and "
            "reducing window collisions are meaningful ways to help this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Scatter white millet on the ground beneath feeders",
              "Dense shrub thickets nearby are essential — they retreat to cover constantly",
              "Low platform feeders or ground trays are preferred over tube feeders",
              "White-throated Sparrows often linger at feeders well into spring",
              "Reduce window collisions with decals — this species is particularly vulnerable"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"White-throated Sparrow  •  Zonotrichia albicollis  •  Module 12")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 36")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
