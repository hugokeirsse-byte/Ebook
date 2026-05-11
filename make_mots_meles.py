"""
Générateur de mots mêlés — thème Animaux, niveau facile
Sortie : 2626×2626px KDP-ready PNG
"""
from PIL import Image, ImageDraw, ImageFont
import random, os

SIZE   = 2626
MARGIN = 160

FXB  = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
FB   = "/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf"
FREG = "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf"

PURPLE  = (90,  40, 160)
LPURPLE = (230, 220, 248)
GRAY    = (130, 120, 150)
INK     = (25,  20,  40)

WORDS = [
    "CHAT", "CHIEN", "LAPIN", "LION", "TIGRE", "OURS",
    "LOUP", "VACHE", "CHEVAL", "MOUTON", "POULE", "CANARD",
    "SINGE", "RENARD", "AIGLE", "CERF",
]

GRID_N   = 14          # 14×14 — confortable pour niveau facile
DIRS     = [(0,1),(1,0)]   # horizontal + vertical seulement (pas de diagonale)
FILL_CHARS = "AAABBCCDDEEEFFFGGHHIIJJKLLMMNNOOOPPQRRSSTTTUUUVVWXYZ"


# ── Algorithme grille ─────────────────────────────────────────────────────────

def can_place(grid, word, r, c, dr, dc):
    n = len(grid)
    for i, ch in enumerate(word):
        nr, nc = r+i*dr, c+i*dc
        if not (0 <= nr < n and 0 <= nc < n): return False
        if grid[nr][nc] and grid[nr][nc] != ch: return False
    return True

def place(grid, word, r, c, dr, dc):
    for i, ch in enumerate(word):
        grid[r+i*dr][c+i*dc] = ch

def make_grid(words, n=GRID_N, seed=42):
    random.seed(seed)
    grid = [['']*n for _ in range(n)]
    placed = []
    for word in sorted(words, key=len, reverse=True):
        cands = [(r,c,dr,dc)
                 for dr,dc in DIRS
                 for r in range(n)
                 for c in range(n)
                 if can_place(grid, word, r, c, dr, dc)]
        if cands:
            r,c,dr,dc = random.choice(cands)
            place(grid, word, r, c, dr, dc)
            placed.append((word, r, c, dr, dc))
    for r in range(n):
        for c in range(n):
            if not grid[r][c]:
                grid[r][c] = random.choice(FILL_CHARS)
    return grid, placed


# ── Rendu PNG ─────────────────────────────────────────────────────────────────

def draw_page(words, puzzle_num=1, seed=42):
    img  = Image.new("RGB", (SIZE, SIZE), "white")
    d    = ImageDraw.Draw(img)
    cx   = SIZE // 2

    fn_title = ImageFont.truetype(FXB,  115)
    fn_num   = ImageFont.truetype(FREG,  52)
    fn_cell  = ImageFont.truetype(FXB,   74)
    fn_label = ImageFont.truetype(FB,    58)
    fn_word  = ImageFont.truetype(FB,    50)

    # ── Bandeau titre ────────────────────────────────────────────────────────
    d.rectangle([0, 0, SIZE, 240], fill=LPURPLE)
    d.text((cx, 30),  "MOTS MÊLÉS — ANIMAUX", fill=PURPLE, font=fn_title, anchor="mt")
    d.rectangle([0, 240, SIZE, 248], fill=PURPLE)

    d.text((cx, 262), f"Puzzle n°{puzzle_num}", fill=GRAY, font=fn_num, anchor="mt")

    # ── Grille ───────────────────────────────────────────────────────────────
    grid, placed = make_grid(words, n=GRID_N, seed=seed)
    n = GRID_N

    GRID_PX   = 1480          # taille totale de la grille en pixels
    CELL      = GRID_PX // n  # ≈ 105px par cellule
    GRID_LEFT = (SIZE - GRID_PX) // 2
    GRID_TOP  = 330

    # Fond légèrement teinté pour la grille
    d.rectangle([GRID_LEFT-4, GRID_TOP-4,
                 GRID_LEFT+GRID_PX+4, GRID_TOP+GRID_PX+4],
                fill=(245, 242, 252))

    for r in range(n):
        for c in range(n):
            x0 = GRID_LEFT + c*CELL
            y0 = GRID_TOP  + r*CELL
            # Alternance très légère de fond
            if (r+c) % 2 == 0:
                d.rectangle([x0+1, y0+1, x0+CELL-1, y0+CELL-1],
                             fill=(255, 255, 255))
            # Lettre centrée
            d.text((x0 + CELL//2, y0 + CELL//2),
                   grid[r][c], fill=INK, font=fn_cell, anchor="mm")

    # Lignes de grille
    for i in range(n+1):
        lw = 3 if i == 0 or i == n else 1
        col = PURPLE if (i == 0 or i == n) else (200, 192, 225)
        # Horizontales
        y = GRID_TOP + i*CELL
        d.line([(GRID_LEFT, y), (GRID_LEFT+GRID_PX, y)], fill=col, width=lw)
        # Verticales
        x = GRID_LEFT + i*CELL
        d.line([(x, GRID_TOP), (x, GRID_TOP+GRID_PX)], fill=col, width=lw)

    # ── Liste des mots ────────────────────────────────────────────────────────
    WL_TOP = GRID_TOP + GRID_PX + 52
    d.text((cx, WL_TOP), "MOTS À TROUVER :", fill=PURPLE, font=fn_label, anchor="mt")

    COLS   = 4
    COL_W  = (SIZE - 2*MARGIN) // COLS
    sorted_words = sorted(words)
    for i, word in enumerate(sorted_words):
        col = i % COLS
        row = i // COLS
        wx  = MARGIN + col*COL_W + COL_W//2
        wy  = WL_TOP + 72 + row*64
        # Puce colorée
        colors = [(255,80,80),(255,170,0),(80,190,80),(80,130,255)]
        d.ellipse([wx-COL_W//2+2, wy+18, wx-COL_W//2+22, wy+38],
                  fill=colors[col])
        d.text((wx-COL_W//2+32, wy), word, fill=INK, font=fn_word, anchor="lt")

    # ── Pied de page ─────────────────────────────────────────────────────────
    d.rectangle([0, SIZE-52, SIZE, SIZE], fill=LPURPLE)
    d.text((cx, SIZE-46), "Lumi Doodle  ·  Mots Mêlés Animaux",
           fill=PURPLE, font=fn_num, anchor="lt")

    return img


# ── Génération ────────────────────────────────────────────────────────────────
img = draw_page(WORDS, puzzle_num=1, seed=42)
img.save("/home/user/Ebook/mots_meles_demo.png")
print("✓ mots_meles_demo.png")
