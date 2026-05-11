"""
Kraken Mandala — 2626×2626px KDP coloring page
Perfect 8-fold symmetry, all lines closed, bold outlines.
"""
from PIL import Image, ImageDraw
import numpy as np
import math

SIZE = 2626
CX = CY = SIZE // 2
N  = 8          # 8-fold symmetry
LW = 7          # main stroke
LWS = 5         # secondary stroke
LWX = 3         # thin accent

BG  = (255, 255, 255)
INK = (8, 8, 8)


# ── Geometry helpers ──────────────────────────────────────────────────────────

def rot(x, y, deg):
    a = math.radians(deg)
    dx, dy = x - CX, y - CY
    return (CX + dx*math.cos(a) - dy*math.sin(a),
            CY + dx*math.sin(a) + dy*math.cos(a))

def rpts(pts, deg):
    return [rot(x, y, deg) for x, y in pts]

def ip(p):   return (round(p[0]), round(p[1]))
def ips(ps): return [ip(p) for p in ps]

def cpoly(cx, cy, r, n=80, a0=0, a1=360):
    """Circle / arc polygon points (standard math convention)."""
    end = abs(a1 - a0) < 359.9
    angs = np.linspace(math.radians(a0), math.radians(a1), n, endpoint=end)
    return [(cx + r*math.cos(a), cy + r*math.sin(a)) for a in angs]

def epoly(cx, cy, rx, ry, n=80, a0=0, a1=360):
    """Ellipse polygon points."""
    end = abs(a1 - a0) < 359.9
    angs = np.linspace(math.radians(a0), math.radians(a1), n, endpoint=end)
    return [(cx + rx*math.cos(a), cy + ry*math.sin(a)) for a in angs]

def stroke(draw, pts, lw=None, closed=True):
    """Draw outline (polyline or closed polygon)."""
    lw = lw or LW
    p = ips(pts)
    if closed: p = p + [p[0]]
    draw.line(p, fill=INK, width=lw)

def fill_shape(draw, pts):
    """White-fill a polygon (erases underlying lines inside it)."""
    draw.polygon(ips(pts), fill=BG)

def ring(draw, r, lw=None):
    lw = lw or LW
    draw.ellipse([CX-r, CY-r, CX+r, CY+r], outline=INK, width=lw)

def circ(draw, cx, cy, r, lw=None):
    lw = lw or LWS
    draw.ellipse([round(cx-r), round(cy-r), round(cx+r), round(cy+r)],
                 outline=INK, width=lw)

def dot(draw, cx, cy, r):
    draw.ellipse([round(cx-r), round(cy-r), round(cx+r), round(cy+r)], fill=INK)

def sym(draw, fn, offset=0, **kw):
    """Call fn(draw, arm_angle, **kw) N times around the circle."""
    for i in range(N):
        fn(draw, i * (360/N) + offset, **kw)


# ── Drawing elements ──────────────────────────────────────────────────────────

def draw_inner_petal(draw, angle):
    pts = epoly(CX, CY-143, 36, 68)
    pts_r = rpts(pts, angle)
    fill_shape(draw, pts_r)
    stroke(draw, pts_r, lw=LW)

def draw_diamond(draw, angle):
    pts = [(CX, CY-136), (CX+27, CY-174), (CX, CY-212), (CX-27, CY-174)]
    pts_r = rpts(pts, angle)
    fill_shape(draw, pts_r)
    stroke(draw, pts_r, lw=LWS)
    dx, dy = rot(CX, CY-174, angle)
    dot(draw, dx, dy, 6)

def draw_outer_petal(draw, angle):
    pts = epoly(CX, CY-297, 46, 90)
    pts_r = rpts(pts, angle)
    fill_shape(draw, pts_r)
    stroke(draw, pts_r, lw=LWS)
    # Inner detail curve
    pts2 = epoly(CX, CY-297, 28, 55)
    stroke(draw, rpts(pts2, angle), lw=LWX)

def tentacle_poly(r0=402, r1=878, w0=108, w1=14, n=55):
    left, right = [], []
    for i in range(n+1):
        t  = i / n
        rr = r0 + (r1-r0)*t
        ww = (w0*(1-t)**0.62 + w1*t**0.62) * (1 - 0.08*math.sin(t*math.pi))
        left.append( (CX - ww/2, CY - rr))
        right.append((CX + ww/2, CY - rr))
    return left + list(reversed(right))

def draw_tentacle(draw, angle):
    pts = tentacle_poly()
    pts_r = rpts(pts, angle)
    fill_shape(draw, pts_r)
    stroke(draw, pts_r, lw=LW)
    # Thin center spine
    p0 = ip(rot(CX, CY-402, angle))
    p1 = ip(rot(CX, CY-878, angle))
    draw.line([p0, p1], fill=INK, width=LWX)

def draw_suckers(draw, angle):
    data = [(448,24), (532,22), (616,20), (700,17), (782,14), (858,11)]
    for rr, sz in data:
        sx, sy = rot(CX, CY-rr, angle)
        # White fill then double ring
        draw.ellipse([round(sx-sz), round(sy-sz), round(sx+sz), round(sy+sz)], fill=BG)
        circ(draw, sx, sy, sz,    lw=4)
        circ(draw, sx, sy, sz//2, lw=3)

def draw_between_deco(draw, angle):
    # Outer C-scroll
    pts1 = epoly(CX, CY-620, 52, 38, n=32, a0=222, a1=318)
    stroke(draw, rpts(pts1, angle), lw=LWS-1, closed=False)
    # Inner inverted C-scroll
    pts2 = epoly(CX, CY-570, 38, 28, n=32, a0=42, a1=138)
    stroke(draw, rpts(pts2, angle), lw=LWS-1, closed=False)
    # Dot
    dx, dy = rot(CX, CY-595, angle)
    dot(draw, dx, dy, 9)
    # Small oval accent near tentacle base
    pts3 = epoly(CX, CY-462, 22, 36, n=28)
    pts3r = rpts(pts3, angle)
    fill_shape(draw, pts3r)
    stroke(draw, pts3r, lw=LWX)

def draw_border_scallop(draw, angle):
    # Large scallop on arm axis (outward arc, 215°→325°)
    pts = cpoly(CX, CY-997, 55, n=36, a0=215, a1=325)
    stroke(draw, rpts(pts, angle), lw=LW, closed=False)
    dx, dy = rot(CX, CY-997, angle)
    circ(draw, dx, dy, 18, lw=3)
    dot(draw, dx, dy, 8)

def draw_border_scallop_sm(draw, angle):
    # Small scallop between arms
    pts = cpoly(CX, CY-987, 35, n=28, a0=220, a1=320)
    stroke(draw, rpts(pts, angle), lw=LWS, closed=False)
    dx, dy = rot(CX, CY-987, angle)
    dot(draw, dx, dy, 5)


# ── Assemble mandala ──────────────────────────────────────────────────────────

def make():
    img  = Image.new("RGB", (SIZE, SIZE), BG)
    d    = ImageDraw.Draw(img)

    # Outer border first (bottom layer)
    ring(d, 1056, lw=LW)
    sym(d, draw_border_scallop)
    sym(d, draw_border_scallop_sm, offset=22.5)

    # Outer band rings
    ring(d, 945, lw=LW)
    ring(d, 924, lw=LWS)

    # Dots on outer band
    for i in range(N):
        dx, dy = rot(CX, CY-934, i*45)
        circ(d, dx, dy, 17, lw=4); dot(d, dx, dy, 8)
    for i in range(N):
        dx, dy = rot(CX, CY-934, i*45+22.5)
        circ(d, dx, dy, 11, lw=3); dot(d, dx, dy, 5)

    # Between-tentacle decorations
    sym(d, draw_between_deco, offset=22.5)

    # Tentacles + suckers (with white fills to cut through rings)
    ring(d, 402, lw=LW)          # base ring — drawn before tentacles
    sym(d, draw_tentacle)         # white fill covers ring inside each tentacle
    sym(d, draw_suckers)

    # Outer-petal ring (between arms, before mid ring)
    ring(d, 402, lw=LW)          # redraw base ring (cleanly on top of tentacle fill)
    sym(d, draw_outer_petal, offset=22.5)
    ring(d, 402, lw=LW)          # one more pass to close any gaps

    # Mid separation ring
    ring(d, 225, lw=LW)

    # Inner diamonds (between inner petals)
    sym(d, draw_diamond, offset=22.5)

    # Inner petals
    sym(d, draw_inner_petal)

    # Inner rings
    ring(d, 225, lw=LW)
    ring(d, 82,  lw=LWS)
    ring(d, 52,  lw=LW)

    # Center dot
    dot(d, CX, CY, 22)

    img.save("/home/user/Ebook/mandala_kraken.png")
    print("✓ Kraken mandala saved → mandala_kraken.png")


make()
