from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module22_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/22_pine_siskin.jpg"

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
    stats=[("Length","4.3 – 5.5 in  (11 – 14 cm)"),
           ("Wingspan","7.1 – 8.7 in  (18 – 22 cm)"),
           ("Weight","0.4 – 0.6 oz  (12 – 18 g)"),
           ("Lifespan","Up to 9 years (avg. 2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Overall body","Brown, heavily streaked dark"),
          ("Yellow wing flash","Pale yellow — base of flight feathers"),
          ("Yellow tail base","Yellow at base of tail — both sexes"),
          ("Crown","Dark brown with fine streaking"),
          ("Underparts","Whitish, streaked brown"),
          ("Bill","Short, sharply pointed, dark")]
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
    chrome(c,64,"Module 22 of 40")
    content=[Table([[Paragraph("MODULE  22  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Pine Siskin",S_TITLE),
              Paragraph("Spinus pinus",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Pine Siskin is a small, heavily streaked finch of the boreal "
            "and montane forests — an irruptive winter visitor whose appearances at "
            "feeders are excitingly unpredictable. In years when conifer seed crops "
            "fail across the North, Pine Siskins erupt southward in enormous numbers, "
            "descending on nyjer feeders and birch trees across the continent. In "
            "other years they are virtually absent. The subtle yellow flash in the "
            "wings and at the base of the tail is the key field mark that separates "
            "this species from other streaked finches. Despite its plain appearance, "
            "the Pine Siskin is a remarkably hardy bird, capable of surviving "
            "temperatures as low as -94°F (-70°C) by raising its metabolic rate.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Pine Siskin breeds across the boreal forests of Canada and Alaska, "
            "and in montane conifer forests south through the Rockies, Cascades, and "
            "Sierra Nevada into Mexico. In winter it moves south and east in variable "
            "numbers, potentially appearing anywhere in the contiguous United States "
            "during irruption years. It inhabits coniferous and mixed forests, forest "
            "edges, weedy fields, and alder and birch stands. In irruption years it "
            "frequently visits nyjer feeders in suburban gardens far outside its "
            "normal range.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Nyjer (thistle) seed — the top feeder choice, attracts large flocks",
              "Black-oil sunflower seeds and sunflower chips",
              "Conifer seeds extracted from open cones — the core wild food",
              "Alder and birch catkin seeds in late winter",
              "Weed seeds: thistle, dandelion, ragweed",
              "Salt and mineral deposits — regularly visits salt licks and road salt"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,65,"Pine Siskin")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Pine Siskins are intensely gregarious, almost always found in "
            "flocks — sometimes mixed with American Goldfinches, Common Redpolls, "
            "and other small finches. They are acrobatic feeders, clinging to the "
            "tips of conifer branches and hanging upside-down from seed heads with "
            "ease. At feeders they can be surprisingly aggressive for their size, "
            "using a threatening wing-spread display to dominate larger birds. "
            "During irruption years they may appear at feeders by the dozen or "
            "even the hundred. They have a remarkable ability to cache seeds and "
            "to increase their food intake dramatically before cold nights.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Pine Siskins breed in loose colonies in coniferous forests. The "
            "female builds a well-concealed shallow cup nest of twigs, grass, "
            "and rootlets on a horizontal conifer branch, lined with fur, "
            "feathers, and plant down. Clutches of 3–5 pale blue-green eggs "
            "with dark spots are incubated by the female for 13 days, while "
            "the male feeds her. Both parents feed the nestlings regurgitated "
            "seeds. Young fledge at 14–15 days. Pairs raise 1–2 broods per "
            "season, with breeding timed to conifer seed availability.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Pine Siskin's calls are highly distinctive — a rising, "
            "buzzy \"zreeeee\" or \"skreee\" that is unlike any other small "
            "finch and carries a characteristic ascending quality. Flocks "
            "produce a constant chatter of these calls and short musical "
            "twitters. The song is a rambling series of musical and buzzy "
            "phrases, similar to an American Goldfinch but harsher and "
            "more variable.",S_BODY),
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
        Paragraph("The Pine Siskin population is estimated at 35 million individuals "
            "but has declined significantly — by roughly 80% — since 1970, making "
            "it one of the most steeply declining songbirds in North America. Loss "
            "of boreal forest, changes in conifer seed production linked to climate "
            "change, and Salmonella outbreaks at contaminated feeders are the "
            "primary threats. Keeping nyjer feeders scrupulously clean is critical "
            "during irruption years.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Stock nyjer feeders before November — irruptions can arrive suddenly",
              "Clean nyjer feeders weekly — Pine Siskins are highly susceptible to Salmonella",
              "A thistle sock or fine-mesh nyjer tube is ideal; they cling well",
              "In irruption years, expect them to arrive with American Goldfinch flocks",
              "Check wing and tail bases for yellow flash — the key ID mark in mixed flocks"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Pine Siskin  •  Spinus pinus  •  Module 22")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 66")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
