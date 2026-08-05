# Journal des modifications

Notes destinées aux **contributeurs** (chaîne de compilation, structure du dépôt,
outils). Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/).

## [Non publié] — depuis v1.0

175 commits entre `v1.0` (2025-03-28) et aujourd'hui.

### Ajouté

- **Chaîne de compilation dockerisée.** Quarto s'exécute dans l'image
  `mlsysbook-linux:quarto-1.9.38` (voir `docker/linux/Dockerfile`,
  `docker/dependencies/{requirements.txt,install_packages.R,tl_packages}`).
  Le host n'est plus utilisé pour les rendus reproductibles. Détails dans
  `CLAUDE.md`.
- **`process.sh`** : script de build complet (HTML + PDF + diapositives +
  export notebooks/marimo), toutes les commandes quarto/marimo passant par un
  helper `q()` docker.
- **Diapositives revealjs** : un jeu par chapitre (`slides/00–05`, `index.qmd`,
  `theme.scss`, `slides/_quarto.yml`). Sortie HTML uniquement.
- **Sortie PDF/LaTeX** : `tex-hacks/*` (callouts, police de code, tables
  colorées, correctifs Unicode, image de page titre) et
  `lua/callout_custom_pdf.lua`. Profil de production dans `_quarto-production.yml`.
- **Sortie Typst** (expérimentale) : `_quarto-typst.yml`, `make-typst-zip.sh`.
- **Outils Python** (stdlib, testés) :
  - `clean_notebooks.py` — nettoie les notebooks exportés (en-tête YAML,
    directives `#|`, blocs `bloc_*`, images, ancres de titre). Tests :
    `tests/test_clean_notebooks.py`.
  - `make_exercices.py` — génère `08-Exercices.qmd` à partir des blocs
    `bloc_exercice` de chaque chapitre. Tests : `tests/test_make_exercices.py`.
- **Quiz par chapitre** : `quiz/Chap00–05.yml`, rendus via
  `code_complementaire/quizz_functions.py` (HTML seulement).
- **Assistant IA** : widget de clavardage `assets/ia-companion/`
  (`widget.js` + `lib.js`), injecté par `_quarto.yml`
  (`include-after-body`), adossé à un worker Cloudflare externe.
- **Données vectorielles** : section GeoPandas/leafmap (ch01), cartes statiques
  contextily (ch02).

### Modifié

- **Contenu des chapitres** substantiellement enrichi (+2 512 / −354 lignes) :
  ch00 (prise en main), ch01 (importation + vectoriel), ch02 (réhaussement,
  cercle des corrélations ACP, étirement par décorrélation), ch03 (spectral),
  ch04 (spatial), ch05 (classifications).
- `08-Exercices.qmd` désormais **généré** — ne pas éditer à la main ; modifier
  les exercices dans les chapitres.
- `_quarto.yml`, `css/r4ds.scss`, `references.bib`, `.gitignore`, `README.md`
  mis à jour.

### Supprimé

- Artefacts générés qui étaient versionnés par erreur (l'essentiel des ~48 000
  lignes retirées, **pas** du contenu) : `get-pip.py`, un
  `_quarto_internal_scss_error.scss` résiduel, les `.tex`/`.docx`/`.ipynb`
  compilés, `_quarto.yml.bak`.

### Notes pour contribuer

- Ne pas versionner les sous-dossiers `**/figure-docx/` (gitignorés) ni les
  artefacts `*.npy`/`*.npz`.
- `docs/` est la sortie publiée (régénérée à chaque build) ; le PDF y est
  committé en entier — surveiller sa taille (limite GitHub 50 Mo).
- Après un build : vérifier `build.log` (process.sh renvoie 0 même en cas
  d'échec) et confirmer que `docs/…​.pdf` existe toujours avant de committer.

## [1.0] — 2025-03-28

Version initiale.
