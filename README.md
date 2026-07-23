# Traitement d'images satellites avec Python

* Édition 1 (mars 2025)
* Édition prévue en août 2025

Livre [Quarto](https://quarto.org) (français). Les chapitres sont les fichiers
`NN-*.qmd`; le site généré est écrit dans `docs/`.

## Générer le livre avec Docker

> Quarto s'exécute **dans un conteneur Docker**, pas sur l'hôte. Le Quarto de
> l'hôte est un environnement différent — utilisez le conteneur pour des
> constructions reproductibles.

### Prérequis

* [Docker](https://docs.docker.com/get-docker/) installé et démarré.
* L'image de construction `mlsysbook-linux:v2` (voir ci-dessous pour la bâtir).

### 1. Construire l'image Docker

Nécessaire au premier usage, ou après modification des dépendances
(`docker/dependencies/requirements.txt`, `install_packages.R`, `tl_packages`) :

```bash
docker build -t mlsysbook-linux:v2 -f docker/linux/Dockerfile .
```

L'image contient Quarto, Python (dont `torch` CPU, `opencv`, `rasterio`…), R et
TeX Live. La construction est longue (~20 min, image ~11 Go).

### 2. Générer tout le livre (recommandé)

Le script `process.sh` construit tout : site HTML + PDF, et exporte chaque
chapitre en `.ipynb` (et en script marimo `.py`).

```bash
./process.sh
```

Sorties :

| Dossier      | Contenu                                             |
|--------------|-----------------------------------------------------|
| `docs/`      | Site HTML + le PDF téléchargeable                   |
| `pdf/`       | `Traitement-d-images-satellites-avec-Python.pdf`    |
| `notebooks/` | Chapitres et annexes exportés en `.ipynb`           |
| `marimo/`    | Chapitres convertis en scripts marimo `.py`         |

### 3. Commandes manuelles

Toutes les commandes montent le dépôt sur `/workspace` dans le conteneur.

**Site HTML :**

```bash
docker run --rm -v "$PWD":/workspace mlsysbook-linux:v2 \
  quarto render --to html --output-dir ./docs
```

**PDF** (nécessite le profil `production`, où le format `pdf` est défini) :

```bash
docker run --rm -v "$PWD":/workspace mlsysbook-linux:v2 \
  quarto render --profile production --to pdf --output-dir ./pdf
```

**Aperçu interactif** (rechargement automatique, sur <http://localhost:3508>) :

```bash
docker run --rm --network=host -p 3508:3508 -v "$PWD":/workspace \
  mlsysbook-linux:v2 quarto preview --port 3508 --host 0.0.0.0
```

## Notes et pièges

* **Fichiers appartenant à `root`.** Le conteneur s'exécute en tant que `root`,
  donc les fichiers générés (`docs/`, `pdf/`, notebooks…) appartiennent à `root`
  sur l'hôte. Toute opération de fichier côté hôte sur ces fichiers échoue en
  `EACCES` — c'est pourquoi `process.sh` copie le PDF dans `docs/` **dans** le
  conteneur.
* **Cache d'exécution.** L'exécution des cellules est mise en cache
  (`.jupyter_cache/`, `execute: cache: true`) : les re-rendus réutilisent la
  sortie mise en cache. Supprimez le cache pour forcer une ré-exécution.
* **Nom du PDF.** Basé sur le titre du livre
  (`Traitement-d-images-satellites-avec-Python.pdf`), pas sur le champ `output:`
  de `_quarto-production.yml` (inactif pour les projets `book`).
* **Ajouter une dépendance Python** sans reconstruire toute l'image (~20 min) :
  patch en couche —
  `docker build -t mlsysbook-linux:v2 - <<< $'FROM mlsysbook-linux:v2\nRUN pip install <paquet>'`.
  L'image diverge alors du Dockerfile jusqu'à une reconstruction propre.
