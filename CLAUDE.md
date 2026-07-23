# CLAUDE.md

Quarto book: *Traitement d'images satellites avec Python* (French). Chapters are `NN-*.qmd`; site output → `docs/`.

## Build toolchain

- **Quarto runs in docker, not on host.** Image: `mlsysbook-linux:v2` (built from `docker/linux/Dockerfile`). Host quarto (`/opt/quarto`) is a different env — use the container for reproducible builds.
- Run pattern (from repo root): `docker run --rm -v "$PWD":/workspace mlsysbook-linux:v2 quarto <args>` (repo mounts at `/workspace`). Add `--network=host -p 3508:3508` for `quarto preview`.
- Container runs as **root** → generated files (`docs/`, `pdf/`) are root-owned on host; host-side ops on them (e.g. copying PDF into `docs/`) hit EACCES — run such steps inside the container (`q cp …`, as process.sh does).
- `process.sh` — full build+export script (HTML + PDF, chapter→ipynb/marimo export). Set `-euo pipefail`; all quarto/marimo calls wrapped in a `q()` docker helper.

## Rendering

- **HTML:** `quarto render --to html --output-dir ./docs`
- **PDF:** needs the production profile — `quarto render --profile production --to pdf --output-dir ./pdf`. The `pdf` format is defined only in `_quarto-production.yml` (a Quarto profile), not in `_quarto.yml`.
- PDF filename is **book-title based** (`Traitement-d-images-satellites-avec-Python.pdf`), NOT the `output:` field in `_quarto-production.yml` (that field is dead for book projects).
- Execution is cached (`.jupyter_cache/`, `execute: cache: true`) — re-renders reuse cached notebook output.
- Quarto bundles Typst, but **book projects cannot render it** (`WARN: typst format not supported by book projects`). PDF stays LaTeX unless the project leaves `type: book`.
- `clean_notebooks.py` (stdlib, tested via `python3 -m unittest tests.test_clean_notebooks -v`) cleans quarto-exported notebooks: renders `bloc_*` callouts as inline HTML (body reused from `docs/<stem>.html`), strips the YAML header, HTML comments, and `#|` directives. Runs in process.sh via `q python3 clean_notebooks.py "$ch.ipynb"` after `quarto convert`.
- Build emits pre-existing non-fatal warnings — a SCSS parse error dumping `_quarto_internal_scss_error.scss`, and dangling `@sec-*` crossrefs. Don't chase unless fixing them directly.

## Deps

- Python: `docker/dependencies/requirements.txt`. R: `install_packages.R`. TeX: `tl_packages`. Changing these needs an image rebuild: `docker build -t mlsysbook-linux:v2 -f docker/linux/Dockerfile .`
- Fast dep-add without full ~20min rebuild: layer-patch — `docker build -t mlsysbook-linux:v2 - <<EOF` / `FROM mlsysbook-linux:v2` / `RUN pip install <pkg>` / `EOF`. Caveat: image then diverges from Dockerfile until a clean rebuild.
- `torch` must be CPU wheel: `pip install torch==2.4.0+cpu --index-url https://download.pytorch.org/whl/cpu` (avoids ~2GB CUDA wheel).
- `marimo` is in the `v2` image; chapter→marimo `.py` export active in process.sh.

## Note

Docker infra copied from Harvard `cs249r_book` (MLSysBook); `docker/**/README.md` still references upstream repo/registry — not yet adapted.

Image `v2` reconciled with Dockerfile via clean rebuild (opencv/seaborn/gdown/spyndex/torch-cpu all in `requirements.txt`); verified importable in a fresh build.

`bloc_*` callouts (objectif/package/exercice/aller_loin/attention/astuce/notes) are custom divs styled in `css/r4ds.scss` (per-type color + `images/Bloc*.png` icon).

DOCX render is commented out in process.sh. Quarto prunes non-target format subdirs from `<chapter>_files/` on each render, so `figure-docx/` PNGs get deleted — they're gitignored (`**/figure-docx/`); don't re-commit them.

`docs/…​.pdf` is ~55MB (>GitHub's 50MB soft limit) and re-commits in full each build — consider Git LFS if the repo gets heavy.
