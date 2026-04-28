from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module16_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/16_carolina_wren.jpg"

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
    stats=[("Length","4.7 – 5.5 in  (12 – 14 cm)"),
           ("Wingspan","11.4 in  (29 cm)"),
           ("Weight","0.6 – 0.8 oz  (18 – 22 g)"),
           ("Lifespan","Up to 6 years (avg. 2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Crown & back","Rich warm brown — rufous tones"),
          ("Wings & tail","Brown with fine dark barring"),
          ("Supercilium","Bold white eyebrow stripe"),
          ("Throat & breast","Buffy white to warm buff"),
          ("Flanks & belly","Deeper buffy-orange wash"),
          ("Bill","Long, slender, curved, dark")]
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
    chrome(c,46,"Module 16 of 40")
    content=[Table([[Paragraph("MODULE  16  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Carolina Wren",S_TITLE),
              Paragraph("Thryothorus ludovicianus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Carolina Wren is one of the most surprising birds in the backyard "
            "— a tiny, round-bodied bird with a cocked tail and a bold white eyebrow "
            "stripe that produces one of the loudest songs of any North American bird "
            "relative to its size. Its rich, warm rufous plumage, perpetually upturned "
            "tail, and restless, energetic movements make it instantly endearing. Unlike "
            "most wrens, the Carolina Wren is a year-round resident that forms "
            "permanent pair bonds, with mates staying in close contact throughout the "
            "year. Pairs duet frequently — the male belting out his ringing \"teakettle-"
            "teakettle-teakettle\" while the female responds with a dry chatter — a "
            "remarkable coordination between mates.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Carolina Wren is found year-round across the eastern United States, "
            "from Nebraska and southern Iowa east to the Atlantic coast, and from "
            "southern Ontario south through Florida and into Central America. It "
            "inhabits dense, brushy undergrowth in deciduous and mixed forests, "
            "forest edges, thickets, vine tangles, brushy gardens, and overgrown "
            "fields. It thrives in suburban and rural gardens with dense shrubs, "
            "brush piles, and woody debris. It is highly sensitive to cold winters — "
            "severe ice storms can cause dramatic local population crashes, "
            "from which recovery takes several years.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Suet cakes — the top feeder food for Carolina Wrens",
              "Peanut butter and peanut pieces",
              "Mealworms — live or dried, eagerly taken",
              "Insects and spiders — the bulk of the natural diet year-round",
              "Small berries and seeds occasionally in winter",
              "Bark butter (peanut butter-fat mixture) spread on tree trunks"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,47,"Carolina Wren")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Carolina Wrens are intensely curious and remarkably bold for their size. "
            "They investigate every nook and cranny of their territory — peering into "
            "flowerpots, exploring open garages and porches, and probing bark and leaf "
            "litter for insects with their long, curved bills. Unlike many songbirds, "
            "Carolina Wrens maintain their pair bond year-round. The male and female "
            "remain in constant vocal contact, often duetting together. They are "
            "non-migratory and fiercely territorial, defending their home range "
            "against other wrens with loud singing and aggressive chases. They roost "
            "communally in cold weather, sometimes piling into nest boxes or dense "
            "vegetation to conserve warmth.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Carolina Wrens are famously eclectic nesters, placing their domed "
            "cup nests in almost any sheltered cavity — natural tree holes, old "
            "woodpecker cavities, nest boxes, flowerpots, hanging baskets, boots left "
            "on a porch, or gaps in outbuildings. The male builds several \"dummy\" "
            "nests that are never used, while the female selects and completes the "
            "final nest. Clutches of 4–6 white eggs with reddish-brown speckles are "
            "incubated by the female for 12–16 days. Both parents feed the nestlings, "
            "which fledge at 12–14 days. Pairs raise 2–3 broods per season.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Carolina Wren's song is extraordinarily loud for such a small bird "
            "— a clear, ringing \"teakettle-teakettle-teakettle\" or \"cheery-cheery-"
            "cheery\" that carries 100 meters or more. Males have a repertoire of "
            "27–40 distinct song types and switch between them constantly. Females "
            "respond with a buzzy chatter, creating antiphonal duets. Both sexes "
            "give a variety of sharp \"jimp\" and churring alarm calls when disturbed. "
            "Song is heard year-round, with intensity peaking in early spring.",S_BODY),
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
        Paragraph("The Carolina Wren population is estimated at approximately 14 million "
            "individuals and has been expanding northward over recent decades, aided "
            "by warming winters. However, it remains vulnerable to severe cold snaps "
            "and ice storms — a single harsh winter can eliminate local populations. "
            "Providing dense shrub cover, brush piles, suet, and nest boxes are "
            "among the most effective ways to support this species through winter.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Suet cakes near dense shrubs are the most reliable attraction",
              "Offer live or dried mealworms in a shallow dish — they adore them",
              "Brush piles and log piles near the feeder provide essential cover",
              "A low platform feeder with peanut pieces works well",
              "Carolina Wrens nest in boxes — a 1.5-inch entrance box near cover often works"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Carolina Wren  •  Thryothorus ludovicianus  •  Module 16")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 48")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
