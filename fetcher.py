"""
fetcher.py — Télécharge toutes les planches Köhler depuis Wikimedia Commons
Exécuter sur votre ordinateur : python fetcher.py
Dépendances : pip install requests
"""

import os
import time
import requests

API_URL = "https://commons.wikimedia.org/w/api.php"
CATEGORY = "Köhler's Medizinal-Pflanzen"
OUT_DIR  = "kohler_images"
HEADERS  = {"User-Agent": "MirabiliaEditions-Botanica/1.0 (contact@mirabilia.fr)"}


def get_category_files(category):
    """Récupère la liste de tous les fichiers de la catégorie Wikimedia."""
    files = []
    params = {
        "action":  "query",
        "list":    "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype":  "file",
        "cmlimit": 500,
        "format":  "json",
    }
    while True:
        r = requests.get(API_URL, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        files.extend(data["query"]["categorymembers"])
        if "continue" not in data:
            break
        params["cmcontinue"] = data["continue"]["cmcontinue"]
        time.sleep(0.3)
    return files


def get_file_url(title):
    """Retourne l'URL directe du fichier image."""
    params = {
        "action": "query",
        "titles": title,
        "prop":   "imageinfo",
        "iiprop": "url",
        "format": "json",
    }
    r = requests.get(API_URL, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data  = r.json()
    pages = data["query"]["pages"]
    page  = next(iter(pages.values()))
    return page["imageinfo"][0]["url"]


def safe_filename(title):
    """Transforme le titre Wikimedia en nom de fichier local sûr."""
    name = title.replace("File:", "").strip()
    # Remplace les caractères interdits sur Windows
    for ch in ('/', '\\', ':', '*', '?', '"', '<', '>', '|'):
        name = name.replace(ch, '_')
    return name


def download_all():
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Récupération de la liste depuis Wikimedia Commons…")
    files = get_category_files(CATEGORY)
    total = len(files)
    print(f"{total} fichiers trouvés dans la catégorie '{CATEGORY}'.\n")

    downloaded = 0
    skipped    = 0
    errors     = 0

    for i, f in enumerate(files, 1):
        title    = f["title"]
        filename = safe_filename(title)
        out_path = os.path.join(OUT_DIR, filename)

        if os.path.exists(out_path) and os.path.getsize(out_path) > 10_000:
            print(f"[{i:3}/{total}] SKIP  {filename}")
            skipped += 1
            continue

        try:
            url = get_file_url(title)
            print(f"[{i:3}/{total}] DL    {filename}")
            img = requests.get(url, headers=HEADERS, timeout=60)
            img.raise_for_status()
            with open(out_path, "wb") as fh:
                fh.write(img.content)
            downloaded += 1
            time.sleep(0.5)   # respect rate-limit Wikimedia
        except Exception as e:
            print(f"[{i:3}/{total}] ERR   {filename} — {e}")
            errors += 1
            time.sleep(2)

    print(f"\nTerminé. {downloaded} téléchargés, {skipped} déjà présents, {errors} erreurs.")
    print(f"Images dans le dossier : {os.path.abspath(OUT_DIR)}")


if __name__ == "__main__":
    download_all()
