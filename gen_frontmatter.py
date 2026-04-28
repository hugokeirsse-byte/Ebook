from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import Paragraph, Frame, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas

OUTPUT = "/home/user/Ebook/frontmatter.pdf"

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

# ── Page 1: Half-title (recto) ───────────────────────────────────────────────
def page_halftitle(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,H-1.1*inch,W,1.1*inch,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,0.6*inch,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,H-0.38*inch,"BACKYARD BIRDS OF NORTH AMERICA")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    c.drawRightString(W-MR,H-0.38*inch,"Vol. 1")
    # Centered title block
    c.setFillColor(G_DARK); c.setFont("Helvetica-Bold",36)
    c.drawCentredString(W/2, H/2+1.0*inch, "BACKYARD BIRDS")
    c.setFillColor(G_MID); c.setFont("Helvetica-Bold",36)
    c.drawCentredString(W/2, H/2+0.45*inch, "OF NORTH AMERICA")
    c.setStrokeColor(GOLD); c.setLineWidth(1.2)
    c.line(ML, H/2+0.28*inch, W-MR, H/2+0.28*inch)
    c.setFillColor(GREY); c.setFont("Helvetica-Oblique",14)
    c.drawCentredString(W/2, H/2+0.04*inch, "A Coloring & Field Guide Book")
    c.setFillColor(DARK); c.setFont("Helvetica",11)
    c.drawCentredString(W/2, H/2-0.28*inch, "Volume 1  •  40 Birds  •  120 Coloring Pages")

# ── Page 2: Blank (verso) ────────────────────────────────────────────────────
def page_blank(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)

# ── Page 3: Full title page (recto) ─────────────────────────────────────────
def page_title(c):
    c.setFillColor(G_DARK); c.rect(0,0,W,H,fill=1,stroke=0)
    # Gold top band
    c.setFillColor(GOLD); c.rect(0,H-0.18*inch,W,0.18*inch,fill=1,stroke=0)
    c.setFillColor(GOLD); c.rect(0,0,W,0.18*inch,fill=1,stroke=0)
    # Cream inner panel
    pad=0.55*inch
    c.setFillColor(CREAM); c.roundRect(pad,pad,W-2*pad,H-2*pad,10,fill=1,stroke=0)
    # Title text
    c.setFillColor(G_DARK); c.setFont("Helvetica-Bold",42)
    c.drawCentredString(W/2, H/2+2.4*inch, "BACKYARD")
    c.drawCentredString(W/2, H/2+1.75*inch, "BIRDS")
    c.setFillColor(G_MID); c.setFont("Helvetica-Bold",24)
    c.drawCentredString(W/2, H/2+1.2*inch, "OF NORTH AMERICA")
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.line(ML+0.5*inch, H/2+0.98*inch, W-MR-0.5*inch, H/2+0.98*inch)
    c.setFillColor(DARK); c.setFont("Helvetica-Oblique",15)
    c.drawCentredString(W/2, H/2+0.66*inch, "A Coloring & Field Guide Book")
    c.setFillColor(GREY); c.setFont("Helvetica",11)
    c.drawCentredString(W/2, H/2+0.36*inch, "Volume 1")
    # Divider ornament
    c.setStrokeColor(GOLD); c.setLineWidth(0.6)
    c.line(ML+1.0*inch, H/2+0.06*inch, W-MR-1.0*inch, H/2+0.06*inch)
    # Bird list teaser
    c.setFillColor(G_MID); c.setFont("Helvetica-Bold",8.5)
    c.drawCentredString(W/2, H/2-0.22*inch, "40 SPECIES  •  120 PAGES  •  EDUCATIONAL & ARTISTIC")
    # Bottom block
    c.setFillColor(G_DARK); c.setFont("Helvetica",10)
    c.drawCentredString(W/2, pad+0.55*inch, "Suitable for adults and older children")
    c.setFillColor(G_MID); c.setFont("Helvetica-Bold",9)
    c.drawCentredString(W/2, pad+0.28*inch, "www.BackyardBirdsBook.com")

# ── Page 4: Copyright (verso) ────────────────────────────────────────────────
def page_copyright(c):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,H-MT,W,MT,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    styles=[
        sp("ct","Helvetica-Bold",10,G_DARK,15,align=TA_LEFT,sb=0,sa=6),
        sp("cb","Helvetica",9,DARK,14,align=TA_LEFT,sb=0,sa=4),
        sp("ci","Helvetica-Oblique",9,GREY,13,align=TA_LEFT,sb=0,sa=2),
    ]
    ST,SB,SI=styles
    content=[
        Spacer(1,0.6*inch),
        Paragraph("Backyard Birds of North America — Vol. 1",ST),
        Paragraph("A Coloring &amp; Field Guide Book",SB),
        Spacer(1,0.18*inch),
        Paragraph("First published 2025",SB),
        Spacer(1,0.18*inch),
        Paragraph("© 2025 All rights reserved.",SB),
        Paragraph("No part of this publication may be reproduced, distributed, or transmitted "
            "in any form or by any means, including photocopying, recording, or other "
            "electronic or mechanical methods, without the prior written permission of "
            "the publisher, except for personal, non-commercial use.",SB),
        Spacer(1,0.18*inch),
        Paragraph("The coloring illustrations in this book are original artworks created "
            "for educational and artistic purposes. All bird data, range descriptions, "
            "and natural history information have been compiled from peer-reviewed "
            "ornithological sources and reflect the best available knowledge at the "
            "time of publication.",SB),
        Spacer(1,0.18*inch),
        Paragraph("Printed in the United States of America",SI),
        Paragraph("ISBN: [to be assigned by KDP]",SI),
        Spacer(1,0.28*inch),
        Paragraph("A note on coloring:",sp("cn","Helvetica-Bold",9,G_MID,13)),
        Paragraph("Each coloring illustration is printed on a single page with a blank "
            "reverse side, so that markers and felt-tip pens will not bleed through "
            "onto adjacent content. Colored pencils, watercolor pencils, and fine-tip "
            "markers are recommended.",SB),
        Spacer(1,0.28*inch),
        Paragraph("Conservation data sourced from the IUCN Red List and the North American "
            "Breeding Bird Survey (BBS). Population estimates are approximate and subject "
            "to ongoing revision.",SI),
    ]
    Frame(ML,MB,CW,H-MT-MB,leftPadding=0,rightPadding=0,
          topPadding=0.1*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)

# ── Pages 5–6: Table of Contents (recto + verso) ────────────────────────────
MODULES = [
    (1,"American Goldfinch","Spinus tristis",1),
    (2,"Black-capped Chickadee","Poecile atricapillus",4),
    (3,"Northern Cardinal","Cardinalis cardinalis",7),
    (4,"Mourning Dove","Zenaida macroura",10),
    (5,"Blue Jay","Cyanocitta cristata",13),
    (6,"House Sparrow","Passer domesticus",16),
    (7,"European Starling","Sturnus vulgaris",19),
    (8,"Dark-eyed Junco","Junco hyemalis",22),
    (9,"White-breasted Nuthatch","Sitta carolinensis",25),
    (10,"House Finch","Haemorhous mexicanus",28),
    (11,"Song Sparrow","Melospiza melodia",31),
    (12,"Tufted Titmouse","Baeolophus bicolor",34),
    (13,"Red-winged Blackbird","Agelaius phoeniceus",37),
    (14,"Hairy Woodpecker","Picoides villosus",40),
    (15,"Eastern Towhee","Pipilo erythrophthalmus",43),
    (16,"Carolina Wren","Thryothorus ludovicianus",46),
    (17,"Purple Finch","Haemorhous purpureus",49),
    (18,"Pine Siskin","Spinus pinus",52),
    (19,"Red-breasted Nuthatch","Sitta canadensis",55),
    (20,"Common Grackle","Quiscalus quiscula",58),
    (21,"Baltimore Oriole","Icterus galbula",61),
    (22,"Cedar Waxwing","Bombycilla cedrorum",64),
    (23,"Eastern Phoebe","Sayornis phoebe",67),
    (24,"Chipping Sparrow","Spizella passerina",70),
    (25,"White-throated Sparrow","Zonotrichia albicollis",73),
    (26,"Brown-headed Cowbird","Molothrus ater",76),
    (27,"Eastern Bluebird","Sialia sialis",79),
    (28,"American Robin","Turdus migratorius",82),
    (29,"Hermit Thrush","Catharus guttatus",85),
    (30,"Northern Mockingbird","Mimus polyglottos",88),
    (31,"Ruby-throated Hummingbird","Archilochus colubris",91),
    (32,"Steller's Jay","Cyanocitta stelleri",94),
    (33,"Rose-breasted Grosbeak","Pheucticus ludovicianus",97),
    (34,"Gray Catbird","Dumetella carolinensis",100),
    (35,"House Wren","Troglodytes aedon",103),
    (36,"Downy Woodpecker","Dryobates pubescens",106),
    (37,"Northern Flicker","Colaptes auratus",109),
    (38,"Brown Creeper","Certhia americana",112),
    (39,"Common Yellowthroat","Geothlypis trichas",115),
    (40,"American Kestrel","Falco sparverius",118),
]

def chrome_fm(c,pnum,sub=""):
    c.setFillColor(G_DARK); c.rect(0,H-MT,W,MT,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,H-0.32*inch,"BACKYARD BIRDS OF NORTH AMERICA  —  VOL. 1")
    c.setFillColor(CREAM); c.setFont("Helvetica",7.5)
    if sub: c.drawRightString(W-MR,H-0.32*inch,sub)
    c.setFillColor(CREAM); c.rect(0,0,W,H-MT,fill=1,stroke=0)
    c.setFillColor(G_DARK); c.rect(0,0,W,MB,fill=1,stroke=0)
    c.setFillColor(CREAM); c.setFont("Helvetica",8)
    c.drawCentredString(W/2,0.28*inch,f"— {pnum} —")

def draw_toc_page(c,pnum,entries,page_label):
    chrome_fm(c,page_label,"Table of Contents")
    c.setFillColor(G_DARK); c.setFont("Helvetica-Bold",13)
    c.drawString(ML,H-MT-0.42*inch,"TABLE OF CONTENTS")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(ML,H-MT-0.54*inch,W-MR,H-MT-0.54*inch)
    # Column headers
    y=H-MT-0.78*inch
    c.setFillColor(G_MID); c.setFont("Helvetica-Bold",7.5)
    c.drawString(ML,y,"#"); c.drawString(ML+0.32*inch,y,"SPECIES")
    c.drawString(ML+3.2*inch,y,"SCIENTIFIC NAME"); c.drawRightString(W-MR,y,"PAGE")
    c.setStrokeColor(G_LIGHT); c.setLineWidth(0.4)
    c.line(ML,y-0.06*inch,W-MR,y-0.06*inch)
    rh=0.215*inch
    for idx,(num,name,latin,pg) in enumerate(entries):
        ry=y-0.18*inch-idx*rh
        bg=CREAM if idx%2==0 else colors.HexColor("#F3F0E8")
        c.setFillColor(bg); c.rect(ML-4,ry-0.05*inch,CW+8,rh,fill=1,stroke=0)
        c.setFillColor(G_MID); c.setFont("Helvetica-Bold",8.5)
        c.drawString(ML,ry,f"{num:02d}")
        c.setFillColor(DARK); c.setFont("Helvetica-Bold",8.5)
        c.drawString(ML+0.32*inch,ry,name)
        c.setFillColor(GREY); c.setFont("Helvetica-Oblique",7.5)
        c.drawString(ML+3.2*inch,ry,latin)
        c.setFillColor(DARK); c.setFont("Helvetica",8.5)
        c.drawRightString(W-MR,ry,str(pg))

def page_toc1(c):
    draw_toc_page(c,"v",MODULES[:20],"v")

def page_toc2(c):
    draw_toc_page(c,"vi",MODULES[20:],"vi")

# ── Pages 7–8: Introduction (recto + verso) ─────────────────────────────────
def page_intro1(c):
    chrome_fm(c,"vii","Introduction")
    c.setFillColor(G_DARK); c.setFont("Helvetica-Bold",13)
    c.drawString(ML,H-MT-0.42*inch,"INTRODUCTION")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(ML,H-MT-0.54*inch,W-MR,H-MT-0.54*inch)
    SB=sp("ib","Helvetica",10,DARK,15,align=TA_JUSTIFY)
    SH=sp("ih","Helvetica-Bold",9,G_MID,13,sb=10,sa=3)
    content=[
        Spacer(1,0.1*inch),
        Paragraph("Welcome to <i>Backyard Birds of North America — Volume 1</i>, "
            "a coloring and field guide book featuring forty of the most "
            "beloved and commonly encountered birds across the continent. "
            "This book is designed for anyone who loves birds — whether you "
            "are a seasoned birder, a curious beginner, or simply someone "
            "who enjoys the meditative practice of coloring.",SB),
        Paragraph("HOW THIS BOOK IS ORGANIZED",SH),
        Paragraph("Each bird is presented across three sections: two facing pages "
            "of natural history information followed by a full-page coloring "
            "illustration. The information pages cover the bird's appearance, "
            "habitat and range, diet, behavior, nesting, song, conservation "
            "status, and practical tips for attracting it to your garden. "
            "A coloring guide at the bottom of the second information page "
            "identifies the key plumage zones and suggests colors to use "
            "for an accurate rendering.",SB),
        Paragraph("The coloring illustrations are printed on a single side of "
            "the page with a blank reverse, so that felt-tip markers and "
            "pens will not bleed through onto the facing text. Colored "
            "pencils, watercolor pencils, and fine-tip markers all work "
            "beautifully on this paper.",SB),
        Paragraph("ABOUT THE SPECIES SELECTION",SH),
        Paragraph("The forty species in this volume were selected to represent "
            "the full range of backyard birds encountered across North "
            "America — from coast to coast and from the boreal forests "
            "of Canada to the subtropical gardens of Florida and the "
            "desert Southwest. The selection spans a wide range of "
            "families, habitats, and ecological roles, and includes "
            "both year-round residents and seasonal visitors. Together "
            "they form a portrait of the extraordinary avian diversity "
            "that surrounds us every day.",SB),
        Paragraph("CONSERVATION NOTE",SH),
        Paragraph("Many of the species featured in this book are in decline. "
            "Population trend data from the North American Breeding Bird "
            "Survey shows that more than two-thirds of the birds in this "
            "volume have experienced measurable population decreases since "
            "1970. The most effective actions any individual can take are "
            "simple: plant native trees and shrubs, reduce or eliminate "
            "lawn pesticides, keep cats indoors, and place decals on large "
            "windows to reduce fatal collisions.",SB),
    ]
    Frame(ML,MB,CW,H-MT-MB-0.65*inch,leftPadding=0,rightPadding=0,
          topPadding=0.05*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)

def page_intro2(c):
    chrome_fm(c,"viii","Introduction")
    SB=sp("ib","Helvetica",10,DARK,15,align=TA_JUSTIFY)
    SH=sp("ih","Helvetica-Bold",9,G_MID,13,sb=10,sa=3)
    SBU=sp("ibu","Helvetica",10,DARK,14,sb=1)
    content=[
        Spacer(1,0.1*inch),
        Paragraph("HOW TO USE THE COLORING GUIDE",SH),
        Paragraph("At the bottom of each bird's second information page you will "
            "find a color guide table listing the key plumage zones and a "
            "suggested color for each. These suggestions reflect the actual "
            "colors of the living bird and are a useful starting point — "
            "but feel free to experiment. Many birds show geographic "
            "variation in color, and individual birds vary with age, "
            "season, and light. There is no single \"correct\" coloring.",SB),
        Paragraph("TIPS FOR BEST RESULTS",SH),
        Paragraph("• <b>Colored pencils</b> give the finest detail and are ideal "
            "for the intricate feather patterns of woodpeckers, warblers, "
            "and sparrows.",SBU),
        Paragraph("• <b>Watercolor pencils</b> can be applied dry and then "
            "activated with a damp brush for a soft, painterly effect "
            "that suits birds like the Hermit Thrush or Cedar Waxwing.",SBU),
        Paragraph("• <b>Fine-tip markers</b> produce bold, saturated color ideal "
            "for the vivid blues and reds of the Indigo Bunting, Northern "
            "Cardinal, or Baltimore Oriole. The blank reverse page means "
            "bleed-through is not a concern.",SBU),
        Paragraph("• Work from light colors to dark, and leave white areas "
            "untouched rather than coloring them white.",SBU),
        Paragraph("READING THE INFORMATION PAGES",SH),
        Paragraph("Quick Stats boxes give size, weight, and lifespan data in "
            "both imperial and metric units. Population trend data is "
            "sourced from the IUCN Red List and the North American "
            "Breeding Bird Survey. Page numbers run continuously through "
            "the book and correspond to the reference numbers in the "
            "Table of Contents.",SB),
        Spacer(1,0.3*inch),
        Paragraph("We hope this book deepens your appreciation for the birds "
            "outside your window — and inspires you to make your garden "
            "a little more welcoming to them.",
            sp("sig","Helvetica-Oblique",10,G_MID,15,align=TA_CENTER)),
        Spacer(1,0.15*inch),
        Paragraph("— The Editors",
            sp("ed","Helvetica",9,GREY,13,align=TA_CENTER)),
    ]
    Frame(ML,MB,CW,H-MT-MB,leftPadding=0,rightPadding=0,
          topPadding=0.1*inch,bottomPadding=0,showBoundary=0).addFromList(content,c)

# ── Build PDF ────────────────────────────────────────────────────────────────
cv = canvas.Canvas(OUTPUT, pagesize=letter)

page_halftitle(cv);  cv.showPage()   # p1 recto
page_blank(cv);      cv.showPage()   # p2 verso
page_title(cv);      cv.showPage()   # p3 recto
page_copyright(cv);  cv.showPage()   # p4 verso
page_toc1(cv);       cv.showPage()   # p5 recto
page_toc2(cv);       cv.showPage()   # p6 verso
page_intro1(cv);     cv.showPage()   # p7 recto
page_intro2(cv);     cv.showPage()   # p8 verso

cv.save()
print(f"Done -> {OUTPUT}  (8 pages)")
