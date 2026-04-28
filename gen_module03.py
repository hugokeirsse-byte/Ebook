from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module03_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/03_blue_jay.jpg"

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
    c.drawString(ML,H-0.40*inch,"BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    if sub: c.drawRightString(W-MR,H-0.40*inch,sub)
    c.setFillColor(CREAM); c.rect(0,0,W,H-MT,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica",8)
    c.drawCentredString(W/2,0.35*inch,f"— {pnum} —")

def draw_stats(c, x, y, bw):
    stats=[("Length","9.8 – 11.8 in  (25 – 30 cm)"),
           ("Wingspan","13.4 – 16.9 in  (34 – 43 cm)"),
           ("Weight","2.5 – 3.5 oz  (70 – 100 g)"),
           ("Lifespan","Up to 26 years (avg. 7 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c, x, y, bw):
    rows=[("Crest & upper wings","Bright blue with black bars"),
          ("Tail","Blue with black barring, white tips"),
          ("Face & nape","White with bold black necklace"),
          ("Breast & belly","White to pale gray"),
          ("Back","Blue-gray"),
          ("Bill & legs","Black")]
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
    chrome(c, 7, "Module 03 of 40")
    content=[Table([[Paragraph("MODULE  03  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Blue Jay",S_TITLE),Paragraph("Cyanocitta cristata",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Blue Jay is one of the most striking and intelligent birds to visit North "
            "American gardens. Its bold blue, white, and black plumage makes it instantly "
            "recognizable at any feeder. Despite its reputation as a bully — it dominates most "
            "other species at feeding stations — the Blue Jay plays a vital ecological role as "
            "one of the continent's most important seed dispersers. Highly adaptable and "
            "extraordinarily vocal, it produces a wide variety of calls including convincing "
            "imitations of hawks, which it uses to clear feeders of competing birds.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Blue Jay is found throughout the eastern half of North America, from "
            "southern Canada (Alberta east to Nova Scotia and Newfoundland) south through "
            "Florida and west to the edge of the Great Plains. It inhabits a wide range of "
            "wooded environments including deciduous and mixed forests, forest edges, suburban "
            "neighborhoods, city parks, and gardens with mature oak trees. Northern populations "
            "are partially migratory, with large flocks moving south in autumn along coastlines "
            "and ridges, though many individuals remain year-round even in cold climates.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Acorns — by far the most important food source",
              "Whole and shelled peanuts — a feeder favorite",
              "Sunflower seeds (black-oil and striped)",
              "Corn (cracked or whole kernel)",
              "Insects, grasshoppers, beetles during summer",
              "Occasionally: eggs and nestlings of other birds"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c, 8, "Blue Jay")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Blue Jays are highly social outside the breeding season, gathering in "
            "loose flocks and traveling together through the forest canopy. They are among "
            "the most vocal birds in North America, producing a rich repertoire of calls "
            "including their signature loud \"jay-jay-jay\" alarm, musical liquid gurgles, "
            "whisper songs, and remarkably accurate mimicry of Red-shouldered and Red-tailed "
            "Hawks. This mimicry serves multiple purposes: alerting other jays to hawk "
            "presence and, controversially, potentially clearing feeders so the jay can feed "
            "undisturbed. Blue Jays have demonstrated problem-solving abilities and "
            "tool use in laboratory settings, ranking among the most cognitively "
            "advanced birds studied.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Blue Jays form monogamous pairs that often mate for life. Both sexes "
            "participate in nest building, constructing a bulky open cup of twigs, bark "
            "strips, mud, and grass in the fork of a tree or shrub, typically 10–25 feet "
            "above ground. Clutches of 2–7 eggs (usually 4–5) are incubated for 17–18 days "
            "by both parents. Nestlings are fed by both parents and fledge at 17–21 days. "
            "Pairs typically raise one brood per year. Both parents aggressively mob and "
            "chase away predators, including owls, hawks, cats, and humans.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Blue Jay's vocal repertoire is one of the most varied of any North "
            "American bird. Its primary call is a loud, harsh \"jay\" or \"jeer,\" used as "
            "an alarm. It also produces a bell-like \"tool-tool\" call, soft musical "
            "whisper songs audible only at close range, and uncannily accurate imitations "
            "of at least three hawk species. Researchers believe jays use hawk mimicry both "
            "as a warning system and as a competitive strategy at feeders.",S_BODY),
        Paragraph("CONSERVATION STATUS",S_HDR)]
    tbl=Table([[Paragraph("IUCN Red List:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Least Concern",sp("x","Helvetica-Bold",9,G_LIGHT,13)),
                Paragraph("Population trend:",sp("x","Helvetica-Bold",9,CREAM,13)),
                Paragraph("Stable",sp("x","Helvetica",9,G_LIGHT,13))]],
              colWidths=[CW*0.22,CW*0.28,CW*0.25,CW*0.25])
    tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),8)]))
    content+=[tbl,Spacer(1,6),
        Paragraph("Blue Jay populations are stable across their range, with an estimated "
            "45 million individuals in North America. The species has benefited from "
            "suburban expansion and the planting of oak trees in urban environments.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Platform feeders or large hopper feeders accommodate their size",
              "Whole peanuts in the shell are irresistible and provide great viewing",
              "Scatter cracked corn on the ground — jays readily feed at ground level",
              "Plant oak trees: a single oak can produce thousands of acorns annually",
              "Expect jays to cache food — they may visit and depart rapidly with full beaks"]:
        content.append(Paragraph(f"<bullet>•</bullet>  {t}",S_BUL))
    content.append(Paragraph("COLORING GUIDE",S_HDR))
    GUIDE_H=6*0.22*inch+0.28*inch; guide_y=MB+GUIDE_H+0.15*inch
    Frame(ML,guide_y+0.08*inch,CW,H-MT-(guide_y+0.08*inch)-0.12*inch,
          leftPadding=0,rightPadding=0,topPadding=0.1*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    draw_color_guide(c,ML,guide_y,CW)

def page3(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    HDR_H=0.80*inch
    c.setFillColor(G_DARK); c.rect(0,H-HDR_H,W,HDR_H,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica-Bold",16); c.drawCentredString(W/2,H-0.48*inch,"COLOR ME!")
    c.setFillColor(G_LIGHT); c.setFont("Helvetica",9)
    c.drawCentredString(W/2,H-0.66*inch,"Blue Jay  •  Cyanocitta cristata  •  Module 03")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5); c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5); c.drawRightString(W-MR,0.35*inch,"Page 9")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
