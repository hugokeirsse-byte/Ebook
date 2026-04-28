from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module11_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/11_song_sparrow.jpg"

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
    stats=[("Length","4.7 – 6.7 in  (12 – 17 cm)"),
           ("Wingspan","7.1 – 9.4 in  (18 – 24 cm)"),
           ("Weight","0.4 – 1.9 oz  (11 – 53 g)"),
           ("Lifespan","Up to 11 years (avg. 3 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Crown","Brown with gray central stripe"),
          ("Back & wings","Brown, heavily streaked dark"),
          ("Breast & sides","White with bold brown streaks"),
          ("Central breast spot","Dark brown — diagnostic dot"),
          ("Supercilium (eyebrow)","Gray-white stripe above eye"),
          ("Bill","Short, conical, pale gray")]
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
    chrome(c,31,"Module 11 of 40")
    content=[Table([[Paragraph("MODULE  11  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Song Sparrow",S_TITLE),
              Paragraph("Melospiza melodia",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Song Sparrow is one of the most widespread and variable songbirds "
            "in North America, found in nearly every habitat from Alaska to Mexico. "
            "Despite its streaky brown plumage that many birders initially dismiss as "
            "\"just a sparrow,\" it is a remarkably accomplished singer — the male "
            "begins his rich, complex song as early as February, often singing from "
            "an exposed perch even in snow and freezing temperatures. The Song Sparrow "
            "is also one of the most scientifically studied birds in the world, with "
            "research spanning over a century that has illuminated fundamental principles "
            "of ecology, behavior, and evolution.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Song Sparrow occupies an extraordinary range of habitats across "
            "North America, from the Aleutian Islands of Alaska south through Canada "
            "and across the entire continental US to central Mexico. It inhabits "
            "wetland edges, marshes, shrubby fields, forest edges, riparian thickets, "
            "coastal dunes, gardens, and suburban parks. It shows remarkable geographic "
            "variation: over 50 subspecies have been described, ranging from tiny pale "
            "desert birds to large dark subspecies in the Pacific Northwest. Many "
            "northern populations migrate south in winter, while southern and coastal "
            "populations are permanent residents.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["White millet — the most attractive seed at feeders",
              "Black-oil sunflower seeds and cracked corn",
              "Weed seeds: crabgrass, ragweed, smartweed, knotweed",
              "Insects and spiders — critical during breeding season",
              "Wild berries and small fruits in autumn",
              "Primarily forages on the ground or in low vegetation"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,32,"Song Sparrow")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Song Sparrows are loosely territorial and moderately social. Males "
            "defend breeding territories through song, often countersinging with "
            "neighboring males in elaborate vocal exchanges. Outside the breeding "
            "season they become more gregarious, joining mixed sparrow flocks. "
            "They forage primarily on the ground, scratching through leaf litter "
            "with a characteristic double-scratch hop. When startled, they fly low "
            "and briefly pump their rounded tail — a distinctive behavior that helps "
            "identify them in flight. Song Sparrows show strong site fidelity, "
            "returning to the same territories year after year.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Song Sparrows are among the earliest breeders in North America, "
            "with males singing on territory as early as late January in the South. "
            "The female builds a well-hidden cup nest of grasses, weeds, and bark "
            "strips, placed on the ground or low in dense vegetation. Clutches of "
            "3–5 pale greenish eggs with brown speckles are incubated by the female "
            "for 12–14 days. Both parents feed nestlings, which fledge at 10–12 days. "
            "Song Sparrows are frequent hosts of Brown-headed Cowbird eggs — a "
            "brood parasite that lays its eggs in other birds' nests. Pairs raise "
            "2–3 broods per season.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Song Sparrow earns its name through one of the most complex and "
            "beautiful songs of any North American sparrow. Each male learns a "
            "repertoire of 8–20 distinct song types and switches between them "
            "throughout the day. Songs typically begin with 2–3 short notes, "
            "followed by a trill and then a complex jumble of notes. The song is "
            "often described as beginning with \"Maids! Maids! Maids! Pick up your "
            "teakettle-ettle-ettle.\" Each male's songs are slightly different, "
            "allowing individual recognition by neighbors.",S_BODY),
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
        Paragraph("The Song Sparrow population is estimated at 130 million individuals "
            "and remains broadly stable, though some regional populations have declined "
            "due to wetland loss and habitat fragmentation. It is one of the most "
            "studied birds in the world — research on Song Sparrow populations on "
            "Mandarte Island, British Columbia has been ongoing since 1975.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Scatter white millet on the ground or a low platform feeder",
              "Dense shrubs and brush piles near feeders provide essential cover",
              "Song Sparrows often arrive at feeders early in the morning",
              "A shallow ground-level birdbath is strongly attractive to them",
              "Leave native grasses and weedy patches in the garden for natural foraging"]:
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
    c.drawCentredString(W/2,H-0.66*inch,"Song Sparrow  •  Melospiza melodia  •  Module 11")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 33")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
