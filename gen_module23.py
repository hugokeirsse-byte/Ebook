from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module23_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/23_chipping_sparrow.jpg"

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
    stats=[("Length","4.7 – 5.9 in  (12 – 15 cm)"),
           ("Wingspan","8.3 in  (21 cm)"),
           ("Weight","0.4 – 0.6 oz  (11 – 16 g)"),
           ("Lifespan","Up to 9 years (avg. 2–3 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Crown (breeding)","Bright rufous chestnut"),
          ("White supercilium","Bold white eyebrow stripe"),
          ("Black eye line","Sharp black line through eye"),
          ("Back & wings","Brown, streaked dark"),
          ("Face & underparts","Clean pale gray — unstreaked"),
          ("Bill","Short, conical, dark gray")]
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
    chrome(c,67,"Module 23 of 40")
    content=[Table([[Paragraph("MODULE  23  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Chipping Sparrow",S_TITLE),
              Paragraph("Spizella passerina",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Chipping Sparrow is one of the most familiar and confiding small "
            "sparrows in North America — a trim, clean-looking bird whose bright rufous "
            "cap, bold white eyebrow, and unstreaked gray breast make it one of the "
            "easiest sparrows to identify in breeding plumage. It is a common inhabitant "
            "of suburban gardens, parks, and open woodlands, often nesting close to "
            "human activity and readily visiting feeders scattered with white millet. "
            "Its song — a long, mechanical trill on a single pitch — is one of the "
            "most familiar sounds of North American spring and summer, frequently "
            "confused with the trill of an insect. It is sometimes called the \"hair "
            "bird\" for its habit of lining its nest with animal hair.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Chipping Sparrow breeds across most of North America, from "
            "the Yukon and Northwest Territories east to Newfoundland and south "
            "through virtually the entire United States into Mexico and Central "
            "America. It inhabits open and semi-open environments with scattered "
            "trees: suburban gardens, parks, orchards, forest edges, open pine "
            "woodlands, and grassy areas with shrubs. It shows a particular "
            "affinity for lawns edged with conifers. Northern populations migrate "
            "south in winter, when the rufous cap is replaced by a duller, "
            "streaked brown crown.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["White millet — the top feeder food, eagerly taken from the ground",
              "Black-oil sunflower chips and cracked corn",
              "Wild grass seeds — the dominant natural food",
              "Weed seeds: crabgrass, chickweed, smartweed",
              "Insects and spiders — essential during breeding season",
              "Primarily forages on the ground beneath feeders and shrubs"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,68,"Chipping Sparrow")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("Chipping Sparrows are tame and approachable birds, often allowing "
            "close observation as they forage quietly on lawns and garden paths. "
            "During the breeding season males are territorial, singing persistently "
            "from a tree or shrub perch. Outside the breeding season they become "
            "gregarious, forming loose flocks with other sparrows and juncos. "
            "They forage almost exclusively on the ground, moving with quick, "
            "darting hops and picking up seeds with precise bill movements. "
            "Their small size and unobtrusive manner mean they are often "
            "overlooked despite being remarkably common in suburban areas.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("Chipping Sparrows build compact, neatly woven cup nests of "
            "grasses and rootlets, almost always lined with fine animal hair — "
            "deer hair, horse hair, or even human hair collected near stables "
            "and farms. Nests are placed in shrubs or small conifers, typically "
            "3–10 feet above the ground. The female lays 3–5 pale blue eggs "
            "with dark spots and incubates them alone for 11–14 days. Both "
            "parents feed the nestlings, which fledge at 9–12 days. Pairs "
            "raise 2 broods per season. They are frequent cowbird hosts.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Chipping Sparrow's song is a prolonged, rapid, mechanical "
            "trill on a single pitch — \"chrrrrrrrrrrr\" — lasting 3–4 seconds "
            "and remarkably insect-like in quality. It is one of the commonest "
            "sounds of suburban spring mornings. The call is a sharp, high \"tsip\" "
            "— thin and easily overlooked. Males sing persistently from dawn to "
            "mid-morning throughout the breeding season.",S_BODY),
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
        Paragraph("The Chipping Sparrow population is estimated at 230 million "
            "individuals but has declined by roughly 27% since 1970. The primary "
            "threats are brood parasitism by Brown-headed Cowbirds, habitat loss "
            "through suburban development eliminating open grassy areas with "
            "scattered trees, and pesticide use reducing insect availability "
            "during the breeding season.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Scatter white millet on the ground or a low platform feeder",
              "Chipping Sparrows forage directly beneath tube feeders — no platform needed",
              "They are tame and often approach within a few feet of a patient observer",
              "Leave short-mown lawn areas near feeders — they love to forage on grass",
              "A small birdbath on or near the ground is strongly attractive to them"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Chipping Sparrow  •  Spizella passerina  •  Module 23")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.35*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.35*inch,"Page 69")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
