from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT   = "/home/user/Ebook/module39_preview.pdf"
IMG_PATH = "/home/user/Ebook/images/39_common_yellowthroat.jpg"

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
    stats=[("Length","4.3 – 5.1 in  (11 – 13 cm)"),
           ("Wingspan","5.9 – 7.5 in  (15 – 19 cm)"),
           ("Weight","0.3 – 0.3 oz  (9 – 10 g)"),
           ("Lifespan","Up to 11 years (avg. 1–2 in wild)")]
    rh=0.26*inch; bh=len(stats)*rh+0.28*inch
    c.setFillColor(G_DARK); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",8); c.drawString(x+8,y-0.22*inch,"QUICK STATS")
    for i,(lbl,val) in enumerate(stats):
        ry=y-0.28*inch-(i+0.5)*rh
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5); c.drawString(x+8,ry,lbl)
        c.setFillColor(G_LIGHT); c.setFont("Helvetica",8.5); c.drawString(x+bw*0.42,ry,val)
    return bh

def draw_color_guide(c,x,y,bw):
    rows=[("Throat & breast (male)","Bright yellow"),
          ("Black mask (male)","Bold, bordered above by white"),
          ("Back & wings","Olive-green"),
          ("Belly & flanks","Yellow-buff, fading to whitish"),
          ("Female — face","Plain olive — no mask"),
          ("Bill","Short, slender, dark — warbler style")]
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
    chrome(c,115,"Module 39 of 40")
    content=[Table([[Paragraph("MODULE  39  /  40",sp("m","Helvetica-Bold",8,G_DARK,11))]],colWidths=[CW])]
    content[0].setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),G_LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10)]))
    content+=[Spacer(1,8),Paragraph("Common Yellowthroat",S_TITLE),
              Paragraph("Geothlypis trichas",S_LAT),GoldLine(CW),Spacer(1,6)]
    Frame(ML,MB,CW,H-MT-MB-0.12*inch,leftPadding=0,rightPadding=0,
          topPadding=0.14*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)
    stats_y=H-MT-0.14*inch-1.52*inch
    stats_h=draw_stats(c,ML,stats_y,CW)
    c2=[Paragraph("PRESENTATION",S_HDR),
        Paragraph("The Common Yellowthroat is one of the most widespread and abundant "
            "warblers in North America — a small, energetic bird of marshes, "
            "wet thickets, and weedy fields whose masked male is instantly "
            "recognizable. The bold black mask bordered by white above, "
            "vivid yellow throat, and olive-green back give the male an "
            "almost comical appearance — like a tiny, feathered bandit. "
            "Its loud, emphatic song — \"witchety-witchety-witchety\" — is "
            "one of the most familiar sounds of summer wetlands and "
            "overgrown fields across the continent, and is often the "
            "first warbler song a beginning birder learns to identify "
            "by ear.",S_BODY),
        Paragraph("HABITAT & RANGE",S_HDR),
        Paragraph("The Common Yellowthroat breeds across virtually all of North "
            "America, from Alaska and Canada south through the entire "
            "United States to Mexico, making it one of the most broadly "
            "distributed warblers on the continent. It winters along the "
            "Gulf Coast, in Florida, and through Central America. It "
            "inhabits a wide variety of dense, low vegetation near water: "
            "cattail marshes, sedge meadows, wet thickets, stream margins, "
            "and overgrown fields. It is rarely found far from dense, "
            "low cover — it is a skulker by nature.",S_BODY),
        Paragraph("DIET & FEEDING",S_HDR)]
    for f in ["Insects — the near-exclusive diet: beetles, flies, ants, aphids",
              "Caterpillars and moth larvae gleaned from low vegetation",
              "Spiders and small invertebrates from dense stem bases",
              "Damselflies and small dragonflies near wetland edges",
              "Occasionally small seeds in late summer and fall",
              "Does not visit feeders — dense native plantings near water attract it"]:
        c2.append(Paragraph(f"<bullet>•</bullet>  {f}",S_BUL))
    fy=stats_y-stats_h-0.1*inch
    Frame(ML,MB,CW,fy-MB,leftPadding=0,rightPadding=0,
          topPadding=0,bottomPadding=0,showBoundary=0).addFromList(c2,c)

def page2(c):
    chrome(c,116,"Common Yellowthroat")
    content=[Paragraph("BEHAVIOR & SOCIAL LIFE",S_HDR),
        Paragraph("The Common Yellowthroat is a restless, secretive bird that "
            "spends most of its time moving through dense low vegetation "
            "just above the water line — difficult to observe but easy "
            "to hear. Males are highly territorial and respond aggressively "
            "to playback of their song, often popping up to a visible "
            "perch to investigate an intruder. The black mask of the "
            "male is a social signal used in mate assessment and male "
            "rivalry. Females choose nesting sites within the male's "
            "territory and are largely responsible for nest construction. "
            "Outside the breeding season, yellowthroats are often found "
            "in loose mixed flocks during migration.",S_BODY),
        Paragraph("NESTING & BREEDING",S_HDR),
        Paragraph("The female builds a bulky, deep cup nest of grasses, sedges, "
            "and plant fibers, placed low in dense vegetation — often "
            "within inches of the ground or water surface, attached "
            "to cattail stems or grass clumps. She incubates 3–5 "
            "white eggs with reddish-brown spots for 12 days. Both "
            "parents feed the nestlings, which fledge at 8–10 days. "
            "Pairs raise 1–2 broods per season. The Common Yellowthroat "
            "is a frequent cowbird host, and cowbird parasitism can "
            "significantly reduce nesting success.",S_BODY),
        Paragraph("SONG & COMMUNICATION",S_HDR),
        Paragraph("The Common Yellowthroat's song is one of the most distinctive "
            "in North America — a loud, emphatic \"witchety-witchety-witchety\" "
            "repeated 3–5 times, carrying well across open marsh and "
            "weedy fields. Geographic variation in song is extensive; "
            "local dialects differ across the continent. The call is "
            "a sharp, dry \"tchek\" — frequently given as the bird "
            "moves through dense cover. The song is heard from May "
            "through August on breeding grounds.",S_BODY),
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
        Paragraph("The Common Yellowthroat population is estimated at 73 million "
            "individuals but has declined by approximately 38% since 1970, "
            "driven primarily by the draining and degradation of wetlands "
            "and the loss of dense, shrubby riparian habitat. It is highly "
            "sensitive to wetland quality. Protecting and restoring wetland "
            "edges, marshes, and dense riparian thickets are the most "
            "effective conservation actions for this species.",S_BODY),
        Paragraph("FEEDER TIPS",S_HDR)]
    for t in ["Common Yellowthroats do not visit feeders — habitat is the key",
              "Plant native cattails, sedges, and willows near any water feature",
              "A garden pond with dense emergent vegetation may attract nesting pairs",
              "Listen for 'witchety-witchety' in May near any wet, weedy area",
              "Dense native shrubs near water provide essential cover during migration"]:
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
    c.drawCentredString(W/2,H-0.56*inch,"Common Yellowthroat  •  Geothlypis trichas  •  Module 39")
    FTR_H=0.45*inch
    c.setFillColor(G_DARK); c.rect(0,0,W,FTR_H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,0.16*inch,"Backyard Birds of North America  •  Vol. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,0.16*inch,"Page 117")
    pad=0.18*inch
    c.drawImage(IMG_PATH,ML-pad,FTR_H+pad,width=W-2*(ML-pad),
                height=H-HDR_H-FTR_H-2*pad,preserveAspectRatio=True,mask="auto")

cv=canvas.Canvas(OUTPUT,pagesize=letter)
page1(cv); cv.showPage()
page2(cv); cv.showPage()
page3(cv); cv.showPage()
cv.save()
print(f"Done -> {OUTPUT}")
