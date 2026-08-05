# CLAUDE.md

Quarto book: *Traitement d'images satellites avec Python* (French). Chapters are `NN-*.qmd`; site output → `docs/`.

## Build toolchain

- **Quarto runs in docker, not on host.** Image: `mlsysbook-linux:quarto-1.9.38` (the tag encodes the Quarto version; built from `docker/linux/Dockerfile` with `--build-arg QUARTO_VERSION`). Host quarto (`/opt/quarto`) is a different env — use the container for reproducible builds.
- Run pattern (from repo root): `docker run --rm -v "$PWD":/workspace mlsysbook-linux:quarto-1.9.38 quarto <args>` (repo mounts at `/workspace`). Add `--network=host -p 3508:3508` for `quarto preview`. Full form: `q quarto preview --port N --host 0.0.0.0 --no-browser`. Stopping it leaves a `.quarto/preview` lock + a lingering container → next preview fails "Terminating existing preview server" (exit 1); clear with `rm -rf .quarto/preview` and `docker stop` the orphan (`docker ps --filter ancestor=mlsysbook-linux:quarto-1.9.38`).
- Container runs as **root** → generated files (`docs/`, `pdf/`) are root-owned on host; host-side ops on them (e.g. copying PDF into `docs/`) hit EACCES — run such steps inside the container (`q cp …`, as process.sh does).
- `process.sh` — full build+export script (HTML + PDF, chapter→ipynb/marimo export). Set `-euo pipefail`; all quarto/marimo calls wrapped in a `q()` docker helper.
- Piping a script into the container needs `-i`: `docker run --rm -i … python3 - <<'PY'`. Without `-i`, stdin isn't forwarded → `python3 -` runs an empty script and exits 0 silently.

## Rendering

- **HTML:** `quarto render --to html --output-dir ./docs`
- **PDF:** needs the production profile — `quarto render --profile production --to pdf --output-dir ./pdf`. The `pdf` format is defined only in `_quarto-production.yml` (a Quarto profile), not in `_quarto.yml`.
- PDF filename is **book-title based** (`Traitement-d-images-satellites-avec-Python.pdf`), NOT the `output:` field in `_quarto-production.yml` (that field is dead for book projects).
- Execution is cached (`.jupyter_cache/`, `execute: cache: true`) — re-renders reuse cached notebook output.
- **Typst books work on Quarto ≥1.9** (image is 1.9.38). Render: `quarto render --profile typst --to orange-book-typst --output-dir ./typst-out` (profile `_quarto-typst.yml` sets `format: orange-book-typst` — the bundled textbook layout: colored title band, part banners, boxed chapter headers; palette follows the Quarto brand, blue here). Output is `typst-out/` (gitignored). `keep-typ: true` also emits the book source `index.typ` at repo root (gitignored) — compile it standalone from repo root with `quarto typst compile index.typ out.pdf` (set `TYPST_PACKAGE_CACHE_PATH=.quarto/typst/packages` for offline; needs the `images/` + `*_files/` assets present). `make-typst-zip.sh` bundles `index.typ` + its referenced assets into `typst-out/book-typst-src.zip` for upload to typst.app (`SKIP_RENDER=1` reuses an existing `index.typ`). Caveats: typst's native `.bib` parser is stricter than biblatex — **no duplicate keys**, and `url` must be a real URL (not a bare DOI like `10.xxx`); the LaTeX-only `tex-hacks/` + `callout_custom_pdf.lua` don't apply, so `bloc_*` callouts render as plain blocks. **LaTeX PDF (`--profile production`) stays canonical** — typst is experimental/optional.
- `clean_notebooks.py` (stdlib, tested via `python3 -m unittest tests.test_clean_notebooks -v`) cleans quarto-exported notebooks: strips the YAML header, HTML comments, `#|` directives, `bloc_*` callout regions (removed outright, not converted — except `bloc_exercice`, whose inner markdown is kept, fences stripped), standalone image lines (`![…](…){…}`), and trailing heading-anchor attributes (`## Titre {#sec-…}` → `## Titre`). Stdlib-only, no `docs/` dependency. Runs in process.sh via `q python3 clean_notebooks.py "$ch.ipynb"` after `quarto convert`.
- `08-Exercices.qmd` is **generated** by `make_exercices.py` (stdlib, tested via `python3 -m unittest tests.test_make_exercices -v`) — it extracts each chapter's `:::::: bloc_exercice` div (+ any following `<details>` solutions) into one consolidated chapter. **Don't hand-edit `08-Exercices.qmd`** (has a "NE PAS ÉDITER" banner); edit the exercises in the chapters. process.sh runs it (host `python3`) before rendering; it's listed in `_quarto.yml` under "Partie 5". Not exported to a notebook (no code cells).
- Build emits pre-existing non-fatal warnings — a SCSS parse error dumping `_quarto_internal_scss_error.scss`, and dangling `@sec-*` crossrefs. Don't chase unless fixing them directly.
- Editing any cell in a chapter `.qmd` invalidates its whole jupyter cache → the chapter fully re-executes on next build, which needs its data files present in repo root (`RGBNIR_of_S2A.tif`, `sentinel2.tif` (177MB), `SAR.tif`, `carte.tif`, `modis-aqua.PNG`, `berkeley.jpg`, `ASCIIdata_splib07b_rsSentinel2/`; all `*.tif`-gitignored/local). Verify present before rebuilding.
- xarray `.plot()` (pcolormesh) on a full-res raster makes a huge **vector** `figure-pdf/*.pdf` (a 1188×1599 SAR image = 40MB, and it bloats the book PDF too). Use `.plot.imshow()` (raster, ~100KB) or `artist.set_rasterized(True)`. `#| fig-format: png` is **ignored per-cell** by the jupyter engine.
- process.sh renders PDF with `--no-clean`, so renamed/removed figures linger as orphans in `*_files/figure-pdf/`. When a cell's figure outputs change, clear the chapter's `*_files/` and `docs/*_files/` before rebuilding.
- Quarto converts apostrophes in prose/headings to curly `'` in HTML — `grep` with a straight `'` misses them; verify with apostrophe-free fragments.
- Quarto copies assets referenced in HTML (`<script src=…>`) but does **not** follow JS `import` chains — imported JS (e.g. `assets/ia-companion/lib.js`, imported by `widget.js`) must be declared under `project: resources:` in `_quarto.yml` or it 404s on the published site (`docs/` gets the script but not its import).
- **pdflatex chokes on some Unicode in prose** (e.g. `≤` U+2264, `≥`) → `LaTeX Error: Unicode character …`, the LaTeX PDF fails, and `docs/*.pdf` gets dropped (a following `git add -A` then commits its deletion). Use words ("au plus"/"au moins") or add a mapping to `tex-hacks/fix-unicode-chars.tex`. `×` (U+00D7) and accented Latin are fine; typst/HTML handle all of these. After a build, verify `docs/…​.pdf` still exists before committing.

## Deps

- Python: `docker/dependencies/requirements.txt`. R: `install_packages.R`. TeX: `tl_packages`. Changing these needs an image rebuild: `docker build --build-arg QUARTO_VERSION=1.9.38 -t mlsysbook-linux:quarto-1.9.38 -f docker/linux/Dockerfile .`
- Quarto version is a build arg (`ARG QUARTO_VERSION`, default 1.7.31). process.sh derives `IMAGE` from `QUARTO_VERSION` (default 1.9.38, env-overridable: `QUARTO_VERSION=1.10.x ./process.sh`).
- Fast dep-add without full ~20min rebuild: layer-patch — `docker build -t mlsysbook-linux:quarto-1.9.38 - <<EOF` / `FROM mlsysbook-linux:quarto-1.9.38` / `RUN pip install <pkg>` / `EOF`. Caveat: image then diverges from Dockerfile until a clean rebuild.
- `torch` must be CPU wheel: `pip install torch==2.4.0+cpu --index-url https://download.pytorch.org/whl/cpu` (avoids ~2GB CUDA wheel).
- `marimo` is in the `v2` image; chapter→marimo `.py` export active in process.sh.

## Note

Docker infra copied from Harvard `cs249r_book` (MLSysBook); `docker/**/README.md` still references upstream repo/registry — not yet adapted.

All Python deps (opencv/seaborn/gdown/spyndex/torch-cpu/…) are in `requirements.txt`, so a clean rebuild is reproducible. The older `mlsysbook-linux:v2` (Quarto 1.7.31) may still exist locally; `quarto-1.9.38` is current.

`bloc_*` callouts (objectif/package/exercice/aller_loin/attention/astuce/notes) are custom divs styled in `css/r4ds.scss` (per-type color + `images/Bloc*.png` icon).

`assets/ia-companion/` — "Assistant IA" chat widget (`widget.js` + `lib.js`), injected via `_quarto.yml` `include-after-body` (`data-worker-url=…workers.dev`). LLM logic (`max_tokens`, system prompt, beginner/expert `level`) lives in a **separate Cloudflare worker, NOT this repo** — answer-truncation / level bugs are worker-side. Widget runs in a shadow DOM: key events need `stopPropagation` at the shadow root, else Quarto's search hotkeys (`f`/`s`/`/`) hijack keystrokes (its handler reads `document.activeElement`, which is the shadow host, not the textarea).

Chapter quizzes: an HTML-only cell `render_quizz(Quiz("quiz/ChapNN.yml", "ChapNN"))` from `code_complementaire/quizz_functions.py`, guarded by `.content-visible when-format="html"` with a `when-profile="production"` PDF fallback. Quiz YAML = list of questions: `type` uc/mc/stat, `response` a **1-based** index (or list for mc), `answers` list, optional `help`. `quiz/Chap01–07.yml` shipped as unrelated spatial-stats placeholders — each chapter must point at its own `ChapNN.yml`.

DOCX render is commented out in process.sh. Quarto prunes non-target format subdirs from `<chapter>_files/` on each render, so `figure-docx/` PNGs get deleted — they're gitignored (`**/figure-docx/`); don't re-commit them.

`docs/…​.pdf` is committed in full each build (~17MB after removing vector figure bombs — see the pcolormesh note). If it exceeds GitHub's 50MB soft limit again, hunt oversized `*_files/figure-pdf/*.pdf` or use Git LFS.
