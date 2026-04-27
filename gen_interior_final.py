"""
Assemble the complete interior PDF for KDP upload.

Structure:
  - 8 pages front matter  (half-title / blank / title / copyright / TOC×2 / intro×2)
  - 40 modules × 4 pages  (info-p1 / info-p2 / coloring / BLANK)
  = 168 pages total

The blank page after each coloring illustration ensures that
markers and felt-tip pens cannot bleed through onto adjacent content.
"""
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

W, H = letter

def make_blank_page():
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    from reportlab.lib import colors
    c.setFillColor(colors.HexColor("#FDFBF5"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.showPage()
    c.save()
    buf.seek(0)
    return PyPDF2.PdfReader(buf).pages[0]

writer = PyPDF2.PdfWriter()

# ── Front matter (8 pages) ───────────────────────────────────────────────────
fm = PyPDF2.PdfReader("frontmatter.pdf")
for p in fm.pages:
    writer.add_page(p)

# ── 40 modules × 4 pages ────────────────────────────────────────────────────
blank = make_blank_page()
for i in range(1, 41):
    reader = PyPDF2.PdfReader(f"module{i:02d}_preview.pdf")
    pages = reader.pages
    writer.add_page(pages[0])   # info page 1  (recto)
    writer.add_page(pages[1])   # info page 2  (verso)
    writer.add_page(pages[2])   # coloring     (recto)
    writer.add_page(blank)      # blank        (verso)
    print(f"  Module {i:02d} added")

with open("interior_final.pdf", "wb") as out:
    writer.write(out)

total = 8 + 40 * 4
print(f"\nDone -> interior_final.pdf  ({total} pages)")
print(f"KDP spine width estimate (60# cream paper @ 0.002252 in/page): "
      f"{total * 0.002252:.3f} in")
