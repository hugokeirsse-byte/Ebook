"""Generate all 90 pages for Q1 (January + February + March)."""
import os
from make_word_book import make_page
from words_q1 import WORDS

OUT_DIR = "/home/user/Ebook/pages_q1"
os.makedirs(OUT_DIR, exist_ok=True)

for w in WORDS:
    make_page(
        day_num       = w["day"],
        date_str      = w["date"],
        word          = w["word"],
        language      = w["language"],
        country       = w["country"],
        capital       = w["capital"],
        pronunciation = w["pronunciation"],
        definition    = w["definition"],
        etymology     = w["etymology"],
        example       = w["example"],
        cultural_note = w["cultural_note"],
        related       = w["related"],
        quote         = w["quote"],
        quote_author  = w["quote_author"],
        out_name      = os.path.join(OUT_DIR, w["out_name"]),
    )

print(f"\n✓ {len(WORDS)} pages generated → {OUT_DIR}/")
