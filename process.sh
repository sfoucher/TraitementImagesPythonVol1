#!/usr/bin/env bash
# Build book (HTML + PDF) in the mlsysbook docker container, export notebooks.
set -euo pipefail

# Image tag encodes the Quarto version. Override: QUARTO_VERSION=1.10.x ./process.sh
# (or set IMAGE directly). Build it: docker build --build-arg QUARTO_VERSION=$QUARTO_VERSION -t $IMAGE -f docker/linux/Dockerfile .
QUARTO_VERSION="${QUARTO_VERSION:-1.9.38}"
IMAGE="${IMAGE:-mlsysbook-linux:quarto-${QUARTO_VERSION}}"
PDF_NAME="Traitement-d-images-satellites-avec-Python.pdf"

# Chapters exported to ipynb (+marimo) and stashed under notebooks/
CHAPTERS=(
  00-PriseEnMainPython
  01-ImportationManipulationImages
  02-RehaussementVisualisationImages
  03-TransformationSpectrales
  04-TransformationSpatiales
  05-ClassificationsSupervisees
)
# Aux pages: export and stash under notebooks/ (not marimo-converted)
AUX=(index 00-auteurs references)

# Run a command inside the build container (repo mounted at /workspace)
q() { docker run --rm -v "$PWD":/workspace "$IMAGE" "$@"; }

mkdir -p docs pdf notebooks marimo

# 1. HTML site
q quarto render --cache --to html --output-dir ./docs

# 2. PDF -> publish into docs for the download link
q quarto render --profile production --cache --no-clean --to pdf --output-dir ./pdf
# copy inside container: docs/ is root-owned, host cp would hit EACCES
q cp -f "./pdf/$PDF_NAME" ./docs/

# 3. DOCX (optional)
# mkdir -p docx
# q quarto render --cache --no-clean --to docx --output-dir ./docx
# mv -f "./docx/${PDF_NAME%.pdf}.docx" .

# Detect marimo in the container once (present after adding it to
# docker/dependencies/requirements.txt and rebuilding the image).
HAVE_MARIMO=0
q bash -lc 'command -v marimo >/dev/null 2>&1' && HAVE_MARIMO=1 || true
[ "$HAVE_MARIMO" = 1 ] || echo "WARN: marimo not in image; skipping marimo export (rebuild image to enable)"

# 4. Export chapters -> ipynb (+marimo if available), stash under notebooks/
for ch in "${CHAPTERS[@]}"; do
  q quarto convert "$ch.qmd"
  q python3 clean_notebooks.py "$ch.ipynb"
  [ "$HAVE_MARIMO" = 1 ] && q marimo convert "$ch.ipynb" -o "./marimo/$ch.py"
  mv -f "$ch.ipynb" ./notebooks/
done

# 5. Aux pages: export and stash under notebooks/
for ch in "${AUX[@]}"; do
  q quarto convert "$ch.qmd"
  q python3 clean_notebooks.py "$ch.ipynb"
  mv -f "$ch.ipynb" ./notebooks/
done

# 6. Publish (manual)
# git add . && git commit -m 'new content' && git push
