from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module29_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/29_hermit_thrush.jpg"

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
    stats=[("Length","5.5 – 7.1 in  (14 – 18 cm)"),
           ("Wingspan","9.8 – 11.4 in  (25 – 29 cm)"),
           ("Weight","0.8 – 1.3 oz  (23 – 37 g)"),
           ("Lifespan","Up to 11 years (avg. 4 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Back & head","Warm olive-brown"),
          ("Rump & tail","Bright rufous — key field mark"),
          ("Breast","White with bold dark spots"),
          ("Flanks","Buff-gray wash"),
          ("Eye ring","Pale white — distinct"),
          ("Bill","Slender, slightly curved, dark")]
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
    chrome(c,85,"Module 29 of 40")
    content=[Table([[Paragraph("MODULE  29  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Hermit Thrush",S_TITLE),
              Paragraph("Catharus guttatus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Hermit Thrush is widely considered to produce the most beautiful "
            "song of any North American bird — a series of ethereal, flute-like "
            "phrases of haunting purity, each beginning on a long introductory note "
            "and cascading through a series of spiraling harmonics. Walt Whitman "
            "immortalized it in \"When Lilacs Last in the Dooryard Bloom'd,\" and "
            "it is the state bird of Vermont. Despite its modest, spotted brown "
            "plumage, the Hermit Thrush is instantly distinguished from similar "
            "thrushes by its habit of slowly raising and lowering its bright rufous "
            "tail — a unique, meditative gesture that no other North American thrush "
            "performs.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Hermit Thrush breeds across the boreal forests of Canada and "
            "Alaska, and in montane coniferous forests south through the Appalachians, "
            "Rockies, and Sierra Nevada. It is the only spotted thrush to winter "
            "widely in the United States — a critical identification clue in winter "
            "when other Catharus thrushes have departed for the tropics. In winter "
            "it frequents forest understories, dense shrubby thickets, and wooded "
            "gardens with berry-producing shrubs, from the Pacific coast to the "
            "Atlantic seaboard.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Wild berries: holly, dogwood, mistletoe, juniper, serviceberry",
              "Insects and earthworms gleaned from leaf litter",
              "Small fruits: hackberry, pokeweed, wild grape",
              "Spiders and small invertebrates from the forest floor",
              "Mealworms offered in a low platform or ground dish",
              "Rarely visits seed feeders — prefers natural food in dense cover"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,86,"Hermit Thrush")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("The Hermit Thrush earns its name from its solitary, retiring nature "
            "— it is almost always seen alone, quietly foraging through leaf litter "
            "or perching in dense understory vegetation. Its tail-raising behavior "
            "is one of the most distinctive field marks of any North American bird: "
            "the bird slowly lifts its rufous tail to a near-vertical position, "
            "holds it briefly, then lowers it gradually — a behavior repeated "
            "constantly while the bird is perched. On the breeding grounds males "
            "are territorial, singing from high perches at dawn and dusk. In "
            "winter it is among the most solitary of thrushes, defending individual "
            "berry-producing shrubs against all comers.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("The Hermit Thrush nests on or near the ground in dense boreal or "
            "montane forest. The female builds a bulky cup nest of leaves, grass, "
            "and bark, well concealed beneath a low conifer or shrub. Clutches of "
            "3–4 pale blue eggs are incubated by the female for 11–13 days. Both "
            "parents feed the nestlings, which fledge at 10–15 days. Pairs raise "
            "1–2 broods per season. The species is generally a poor cowbird host "
            "due to the remoteness of its nesting habitat.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Hermit Thrush's song stands alone in North American ornithology "
            "for its otherworldly beauty — a long, clear introductory whistle "
            "followed by a spiraling cascade of pure, harmonically rich phrases, "
            "each at a different pitch. No two phrases are alike. The song carries "
            "through dense forest with extraordinary clarity. The call is a soft, "
            "rising \"veer\" or a sharp \"chuck\" alarm note. Song is heard "
            "primarily at dawn and dusk on the breeding grounds.",S_BODY),
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
        Paragraph("The Hermit Thrush population is estimated at 22 million individuals "
            "and is broadly stable. As the only Catharus thrush to winter in North "
            "America, it is less threatened by tropical deforestation than its "
            "relatives. Climate change poses a long-term threat by shifting boreal "
            "forest composition. Window collisions during migration are a significant "
            "mortality factor, as this species migrates at night.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Plant native holly, dogwood, and serviceberry — essential winter food",
              "Offer mealworms in a low, sheltered dish near dense shrubs",
              "A ground-level birdbath near dense cover is highly attractive",
              "Hermit Thrushes are secretive — watch for them creeping along the ground in thickets",
              "The key field mark: watch for the slow, deliberate tail-raising behavior"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Hermit Thrush  •  Catharus guttatus  •  Module 29")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 87")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
