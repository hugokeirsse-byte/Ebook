from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module18_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/18_redwinged_blackbird.jpg"

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
    stats=[("Length","6.7 – 9.1 in  (17 – 23 cm)"),
           ("Wingspan","12.2 – 15.8 in  (31 – 40 cm)"),
           ("Weight","1.1 – 2.7 oz  (32 – 77 g)"),
           ("Lifespan","Up to 15 years (avg. 2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Body (male)","Glossy jet black"),
          ("Shoulder patch (male)","Brilliant scarlet-red"),
          ("Shoulder border","Yellow to pale yellow"),
          ("Female — overall","Dark brown, heavily streaked"),
          ("Female — face","Pale buff supercilium stripe"),
          ("Bill","Sharp, pointed, black")]
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
    chrome(c,52,"Module 18 of 40")
    content=[Table([[Paragraph("MODULE  18  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Red-winged Blackbird",S_TITLE),
              Paragraph("Agelaius phoeniceus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Red-winged Blackbird is one of the most abundant birds in North "
            "America — and among the most instantly recognizable. The male's jet-black "
            "plumage set against blazing scarlet-and-yellow shoulder patches is one of "
            "the most vivid color combinations in North American ornithology. Few sights "
            "signal the arrival of spring more dramatically than a male Red-winged "
            "Blackbird perched atop a cattail, wings half-spread to display those "
            "brilliant epaulets, delivering his liquid, bubbling \"conk-la-reeee\" "
            "call. In contrast, females are so heavily streaked and brown that beginners "
            "often fail to recognize them as the same species.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Red-winged Blackbird breeds across virtually all of North America, "
            "from Alaska and Canada south through the United States, Mexico, and into "
            "Central America. It is one of the most widespread breeding birds on the "
            "continent. It shows a strong preference for wetland habitats — cattail "
            "marshes, reed beds, wet meadows, and the edges of ponds and lakes — but "
            "also nests in dry upland fields and roadsides. In winter, northern "
            "populations migrate south and form enormous mixed flocks with other "
            "blackbirds and starlings, sometimes numbering in the millions.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Black-oil sunflower seeds and cracked corn at feeders",
              "White millet scattered on the ground",
              "Wild grass seeds, grain, and weed seeds — the core of the natural diet",
              "Insects, spiders, and aquatic invertebrates during breeding season",
              "Wild berries and small fruits in autumn",
              "Waste grain gleaned from agricultural fields in winter"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,53,"Red-winged Blackbird")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Red-winged Blackbirds are highly polygynous — a single male may "
            "hold a territory with up to 15 females nesting within it, though 2–3 "
            "is more typical. Males arrive on the breeding grounds weeks before "
            "females and spend much of the early season in fierce territorial "
            "battles, displaying their red shoulder patches and singing constantly "
            "from prominent perches. They are remarkably aggressive defenders of "
            "their territories, regularly dive-bombing much larger animals — hawks, "
            "herons, crows, and even humans — that venture too close to active nests. "
            "Outside the breeding season they are highly gregarious, forming enormous "
            "mixed-species flocks that roost communally.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Females build deep, woven cup nests of grasses and aquatic vegetation, "
            "lashed to cattail stems or low shrubs over or near water. Clutches of "
            "3–4 pale blue-green eggs with dark scrawls are incubated by the female "
            "alone for 11–13 days. Both parents feed the nestlings, which fledge at "
            "11–14 days. Pairs raise 2–3 broods per season. Females accept cowbird "
            "eggs at a high rate, making them frequent brood parasite hosts.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Red-winged Blackbird's song is one of the most evocative sounds "
            "of North American wetlands — a liquid, gurgling \"conk-la-reeee\" or "
            "\"oak-a-lee\" delivered with a dramatic wing-spread display. Males have "
            "individual song repertoires used to advertise territory. The sharp \"check\" "
            "call and harsh chattering alarm notes are given by both sexes. Females "
            "produce a scolding chatter when disturbed near the nest.",S_BODY),
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
        Paragraph("Despite being one of the most abundant birds in North America — with "
            "a population estimated at 150 million individuals — the Red-winged "
            "Blackbird has declined significantly since 1970, losing an estimated "
            "30% of its population. Wetland drainage, agricultural intensification, "
            "and the loss of native grasslands are the primary drivers. Protecting "
            "and restoring wetland habitats is critical for this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Scatter cracked corn and white millet on a large ground platform",
              "Red-winged Blackbirds arrive in spring flocks — expect multiple birds at once",
              "They prefer open feeding areas with water or marsh nearby",
              "In winter, mixed blackbird flocks may descend on feeders by the hundreds",
              "Planting native cattails and marsh plants near water attracts nesting pairs"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Red-winged Blackbird  •  Agelaius phoeniceus  •  Module 18")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 54")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
