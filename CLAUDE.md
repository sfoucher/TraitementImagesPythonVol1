# CLAUDE.md

Quarto book: *Traitement d'images satellites avec Python* (French). Chapters are `NN-*.qmd`; site output → `docs/`.

## Build toolchain

- **Quarto runs in docker, not on host.** Image: `mlsysbook-linux:v2` (built from `docker/linux/Dockerfile`). Host quarto (`/opt/quarto`) is a different env — use the container for reproducible builds.
- Run pattern (from repo root): `docker run --rm -v "$PWD":/workspace mlsysbook-linux:v2 quarto <args>` (repo mounts at `/workspace`). Add `--network=host -p 3508:3508` for `quarto preview`.
- Container runs as **root** → generated files (`docs/`, `pdf/`) are root-owned on host.
- `process.sh` — full build+export script (HTML + PDF, chapter→ipynb/marimo export). Set `-euo pipefail`; all quarto/marimo calls wrapped in a `q()` docker helper.

## Rendering

- **HTML:** `quarto render --to html --output-dir ./docs`
- **PDF:** needs the production profile — `quarto render --profile production --to pdf --output-dir ./pdf`. The `pdf` format is defined only in `_quarto-production.yml` (a Quarto profile), not in `_quarto.yml`.
- PDF filename is **book-title based** (`Traitement-d-images-satellites-avec-Python.pdf`), NOT the `output:` field in `_quarto-production.yml` (that field is dead for book projects).
- Execution is cached (`.jupyter_cache/`, `execute: cache: true`) — re-renders reuse cached notebook output.

## Deps

- Python: `docker/dependencies/requirements.txt`. R: `install_packages.R`. TeX: `tl_packages`. Changing these needs an image rebuild: `docker build -t mlsysbook-linux:v2 -f docker/linux/Dockerfile .`
- `marimo` is in requirements.txt but only active after an image rebuild.

## Note

Docker infra copied from Harvard `cs249r_book` (MLSysBook); `docker/**/README.md` still references upstream repo/registry — not yet adapted.
