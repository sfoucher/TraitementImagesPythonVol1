#!/usr/bin/env bash
# Build a zip for compiling the book on https://typst.app/ :
#   index.typ + the images/ and *_files/figure-typst/ assets it references.
# The @preview/orange-book package is auto-fetched by typst.app, and the
# bibliography is inlined via citeproc, so no package or references.bib is needed.
#
# Usage:  ./make-typst-zip.sh            # renders fresh, then zips
#         SKIP_RENDER=1 ./make-typst-zip.sh   # reuse an existing index.typ (faster)
set -euo pipefail

QUARTO_VERSION="${QUARTO_VERSION:-1.9.38}"
IMAGE="${IMAGE:-mlsysbook-linux:quarto-${QUARTO_VERSION}}"
ZIP="typst-out/book-typst-src.zip"

q() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD":/workspace "$IMAGE" "$@"; }

mkdir -p typst-out

# 1. Render the typst book -> index.typ (keep-typ) + figure-typst assets.
if [ "${SKIP_RENDER:-0}" != 1 ]; then
  q quarto render --profile typst --to orange-book-typst --cache --no-clean --output-dir ./typst-out
fi
[ -f index.typ ] || { echo "ERROR: index.typ missing (render failed, or SKIP_RENDER=1 with no prior build)"; exit 1; }

# 2. Zip index.typ + every referenced-and-present image, preserving relative paths.
python3 - "$ZIP" <<'PY'
import re, os, sys, zipfile
src = open('index.typ', encoding='utf-8').read()
# first quoted arg of image(...), tolerating trailing args like , width: 6in
refs = sorted({m for m in re.findall(r'image\("([^"]+)"', src) if os.path.isfile(m)})
out = sys.argv[1]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in refs + ['index.typ']:
        if os.path.isfile(p):
            z.write(p)  # relative path preserved -> typst.app resolves it
names = zipfile.ZipFile(out).namelist()
print(f"{out}: {os.path.getsize(out)/1e6:.1f} MB, {len(names)} files "
      f"(images/: {sum(x.startswith('images/') for x in names)}, "
      f"figure-typst: {sum('figure-typst' in x for x in names)})")
PY

echo "Done. Upload $ZIP to https://typst.app/ (set index.typ as the main file)."
