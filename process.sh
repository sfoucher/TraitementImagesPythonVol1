#!/usr/bin/env bash
# Build book (HTML + LaTeX PDF + Typst PDF) in the mlsysbook docker container, export notebooks.
set -euo pipefail

# Image tag encodes the Quarto version. Override: QUARTO_VERSION=1.10.x ./process.sh
# (or set IMAGE directly). Build it: docker build --build-arg QUARTO_VERSION=$QUARTO_VERSION -t $IMAGE -f docker/linux/Dockerfile .
QUARTO_VERSION="${QUARTO_VERSION:-1.9.38}"
IMAGE="${IMAGE:-mlsysbook-linux:quarto-${QUARTO_VERSION}}"
PDF_NAME="Traitement-d-images-satellites-avec-Python.pdf"

# Auto version stamped on the PDF title page (subtitle). Major fixed at 1,
# minor = git commit count (monotonic, no upkeep). Overridable: BOOK_VERSION=1.2 ./process.sh
BOOK_VERSION="${BOOK_VERSION:-1.$(git rev-list --count HEAD 2>/dev/null || echo 0)}"

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

# Run a command inside the build container (repo mounted at /workspace).
# --user maps container output to the host user (no more root-owned docs/pdf).
# HOME=/tmp gives quarto/jupyter/matplotlib a writable config dir (image HOME
# is /root, unwritable for a non-root uid).
q() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD":/workspace "$IMAGE" "$@"; }

mkdir -p docs pdf notebooks marimo typst-out

# 1. HTML site (landing-page subtitle carries the version alongside the edition)
q quarto render --cache --to html \
  -M subtitle="Première édition · Version ${BOOK_VERSION}" --output-dir ./docs

# 2. PDF -> publish into docs for the download link
q quarto render --profile production --cache --no-clean --to pdf \
  -M subtitle="Version ${BOOK_VERSION}" --output-dir ./pdf
cp -f "./pdf/$PDF_NAME" ./docs/

# 2b. Typst PDF (experimental, orange-book layout) -> typst-out/.
# Not published to docs (LaTeX PDF stays canonical); non-fatal so an
# experimental-format failure never aborts the HTML/PDF build.
q quarto render --profile typst --to orange-book-typst --cache --no-clean \
  -M subtitle="Version ${BOOK_VERSION}" --output-dir ./typst-out \
  || echo "WARN: typst render failed (experimental format); continuing"

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
