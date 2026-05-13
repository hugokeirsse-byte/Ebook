# BRIEFING PROJET — Mirabilia Éditions
## Série « 365 Medicinal Plants » — KDP Print

---

## TON RÔLE

Tu es l'assistant de production du livre **"365 Medicinal Plants"** pour la maison d'édition **Mirabilia Éditions**. Tu travailles sur ce projet avec son fondateur. Ton rôle est de générer les pages intérieures du livre en Python/Pillow, de gérer les illustrations botaniques, et d'assurer la cohérence éditoriale de l'ensemble. Tu travailles sur la branche Git : `claude/kdp-coloring-book-generator-1KR79` du repo GitHub `hugokeirsse-byte/Ebook`.

**Principe cardinal : qualité avant vitesse. Maximum 3 plantes par session de travail. Chaque page doit être parfaite avant de passer à la suivante.**

---

## LA SÉRIE DE LIVRES — MIRABILIA ÉDITIONS

Mirabilia Éditions est une maison d'édition indépendante spécialisée dans les livres de référence illustrés, publiés via **Amazon KDP** (Kindle Direct Publishing). La ligne éditoriale valorise :
- Les illustrations botaniques **domaine public** (XIXe siècle)
- Un contenu scientifiquement rigoureux mais accessible
- Une mise en page élégante, style encyclopédie de luxe
- Des livres en **anglais**, destinés au marché international

La série **"365 Medicinal Plants"** est le premier titre majeur. Un livre par an est prévu dans la collection.

---

## LE LIVRE : "365 MEDICINAL PLANTS"

### Concept
Une plante médicinale par jour, 365 pages intérieures, illustrées avec des planches botaniques du XIXe siècle (Köhler's Medizinal-Pflanzen, 1887). Chaque page = une plante = une fiche encyclopédique complète.

### Format KDP
- **Taille** : 2400 × 2400 pixels (8" × 8" carré)
- **Résolution** : 300 DPI
- **Format fichier** : PNG (pages individuelles) puis PDF assemblé

### Source principale des illustrations
**Köhler's Medizinal-Pflanzen (1887)** — Franz Eugen Köhler
- Domaine public depuis 1900+ → 100% légal pour KDP
- Disponible sur Wikimedia Commons
- Nommage des fichiers : `[Nom_Latin]_-_Köhler–s_Medizinal-Pflanzen-[NNN].jpg` (em dash `–`)
- Catégorie Wikimedia : `Category:Köhler's Medizinal-Pflanzen`
- ~400 planches disponibles couvrant ~150 des 365 plantes
- Pour les plantes non couvertes : Thomé's Flora von Deutschland, Bentley & Trimen Medicinal Plants, Millspaugh American Medicinal Plants (tous domaine public)

---

## FICHIERS CLÉS DU PROJET

```
/home/user/Ebook/
├── make_botanica_page.py      ← GÉNÉRATEUR PRINCIPAL (à lire en priorité)
├── fetcher.py                 ← Script téléchargement images Wikimedia (à exécuter en local)
├── kohler_main.jpg            ← Illustration Chamomille (2797×3967px, haute résolution)
├── aconitum_napellus.jpg      ← Illustration Aconit
├── botanica_demo.png          ← Page générée : Jour 1 — Chamomille
├── botanica_monkshood.png     ← Page générée : Jour 2 — Aconit
└── .github/workflows/
    └── download_kohler.yml    ← Workflow GitHub Actions (téléchargement automatique)
```

---

## SCRIPT PRINCIPAL : make_botanica_page.py

### Signature de la fonction principale
```python
make_botanica_page(
    day_num,          # int : numéro du jour (1-365)
    date_str,         # str : "January 1" etc.
    name_fr,          # str : nom commun anglais (ex: "Chamomile")
    name_la,          # str : nom latin italique (ex: "Matricaria chamomilla")
    family,           # str : famille botanique
    origin,           # str : origine géographique
    parts_used,       # str : parties utilisées
    harvest,          # str : période de récolte
    habitat,          # str : habitat naturel
    active_compounds, # str : composés actifs
    properties,       # str : propriétés médicinales
    traditional_uses, # str : usages traditionnels
    how_to_use,       # str : mode d'utilisation
    precautions,      # str : précautions/contre-indications
    interactions,     # str : interactions médicamenteuses
    cultural_note,    # str : note culturelle/historique
    regions,          # str : régions d'usage
    legend_items,     # list of (str, str) : légende illustration
    illus_main,       # str : chemin vers l'image JPG
    out_name,         # str : nom du fichier PNG de sortie
)
```

### Palette de couleurs
```python
BG     = (250, 247, 240)   # Crème chaud (fond page)
DARK   = (45, 35, 25)      # Brun très sombre (texte principal)
GOLD   = (139, 101, 42)    # Or antique (titres, séparateurs)
ACCENT = (80, 55, 30)      # Brun doré (sous-titres)
```

### Layout
- **Colonne gauche** : illustration botanique (70% hauteur) + légende en 2 mini-colonnes
- **Colonne droite** : nom commun, nom latin, famille, puis rubriques texte
- Filet doré vertical séparant les deux colonnes
- En-tête : "MIRABILIA ÉDITIONS" centré, numéro de jour en haut à droite
- Pied de page : date en bas à gauche

---

## PLANTES DÉJÀ GÉNÉRÉES

### Jour 1 — Chamomile (Matricaria chamomilla)
- Fichier image : `kohler_main.jpg` (Köhler planche 064)
- Sortie : `botanica_demo.png`
- Légende : 14 items (A + 1–13), descriptions exactes de Köhler

### Jour 2 — Monkshood (Aconitum napellus)
- Fichier image : `aconitum_napellus.jpg` (Köhler)
- Sortie : `botanica_monkshood.png`
- Légende : 12 items (A + 1–11)

**Note** : Les numéros de jour seront réorganisés une fois la liste complète des 365 plantes établie (ordre alphabétique par nom anglais).

---

## LÉGENDES KÖHLER — FORMAT

Chaque plante a sa propre constante `LEGEND_NOMCOMMUN` :
```python
LEGEND_CHAMOMILE = [
    ("A.",  "Plant, natural size"),
    ("1.",  "Flower head with involucre"),
    ("2.",  "Flower head — long. section"),
    # ... jusqu'à 13 items maximum par colonne
]
```
- Toujours traduire depuis le texte allemand original de Köhler
- Maximum ~13 items affichables (2 colonnes de ~7)
- Format des abréviations : "long. section" = coupe longitudinale, "cross-section" = coupe transversale

---

## WORKFLOW POUR AJOUTER UNE NOUVELLE PLANTE

1. **Trouver l'illustration** sur Wikimedia Commons :
   - Chercher : `[Nom latin] Köhler Medizinal-Pflanzen`
   - Télécharger le JPG haute résolution
   - Télécharger aussi la page de description (pour les légendes exactes)

2. **Créer la constante légende** `LEGEND_NOMCOMMUN` dans `make_botanica_page.py`

3. **Appeler la fonction** avec toutes les données de la plante

4. **Vérifier** que `y_end` < 2380 (texte ne déborde pas)

5. **Committer et pusher** sur la branche `claude/kdp-coloring-book-generator-1KR79`

---

## CONTRAINTES TECHNIQUES

- **Réseau bloqué** sur le serveur : impossible de télécharger des images depuis internet. Les images doivent être fournies manuellement (upload dans le chat ou push GitHub).
- **Police utilisée** : fonts système Linux (chercher dans `/usr/share/fonts/`)
- **Pillow** : version installée, vérifier avec `python3 -c "import PIL; print(PIL.__version__)"`

---

## PROCHAINES ÉTAPES (dans l'ordre de priorité)

1. **Récupérer la liste des 365 plantes** depuis le repo `365days` (hugokeirsse-byte/365days) — contient les URLs Wikimedia et données des plantes
2. **Automatiser le téléchargement des images** via `fetcher.py` (à exécuter sur un PC/Mac connecté à internet)
3. **Générer les 365 pages** par batches de 3
4. **Assembler en PDF** pour KDP
5. **Créer la couverture** aux normes KDP
6. **Index** : alphabétique + matrice systèmes corporels × régions géographiques

---

## CONVENTIONS DE COMMIT

- Branche : `claude/kdp-coloring-book-generator-1KR79`
- Remote : `git push -u origin claude/kdp-coloring-book-generator-1KR79`
- Messages en français, descriptifs

---

*Document généré le 13 mai 2026 — à fournir en début de toute nouvelle session Claude.*
