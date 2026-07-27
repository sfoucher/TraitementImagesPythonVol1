#!/usr/bin/env python3
"""Clean Quarto-exported notebooks: strip the YAML header, HTML comments,
`#|` cell directives, `bloc_*` callout regions (except bloc_exercice, whose
inner markdown is kept), standalone image lines, and heading anchor
attributes (see specs/2026-07-23-clean-notebooks-design.md)."""
import argparse
import json
import re
from pathlib import Path


_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_DIRECTIVE = re.compile(r"^\s*#\|")


def strip_html_comments(text: str) -> str:
    """Remove <!-- ... --> and <!--- ... ---> blocks (multiline)."""
    return _HTML_COMMENT.sub("", text)


def strip_cell_directives(lines):
    """Drop Quarto cell-option lines (#| ...) from a code cell source list."""
    return [ln for ln in lines if not _DIRECTIVE.match(ln)]


def strip_yaml_header(lines):
    """Remove a leading --- ... --- YAML front matter block (position 0 only)."""
    if not lines or lines[0].strip() != "---":
        return lines
    # find the closing fence
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            rest = lines[i + 1:]
            # drop a single leading blank line left behind
            if rest and rest[0].strip() == "":
                rest = rest[1:]
            return rest
    return lines  # no closing fence: leave untouched


# A trailing pandoc attribute block on an ATX heading, e.g. "## Titre {#sec-x}"
# or "# T {#id .unnumbered}". [^}]* keeps it anchored to the final {...} group.
_HEADING_ATTR = re.compile(r"^(#{1,6}\s.*?)\s*\{[^}]*\}\s*$")


def strip_heading_anchors(lines):
    """Drop a trailing {#id .class ...} attribute block from ATX headings."""
    out = []
    for ln in lines:
        nl = "\n" if ln.endswith("\n") else ""
        m = _HEADING_ATTR.match(ln.rstrip("\n"))
        out.append(m.group(1).rstrip() + nl if m else ln)
    return out


# A standalone markdown image line, e.g. "![légende](images/x.png)" with an
# optional trailing {…} attribute block (fig-align, width, …).
_IMAGE = re.compile(r"^!\[[^\]]*\]\([^)]*\)\s*(\{[^}]*\})?\s*$")


def strip_images(lines):
    """Drop standalone markdown image lines (![alt](path){…})."""
    return [ln for ln in lines if not _IMAGE.match(ln.strip())]


KNOWN_TYPES = (
    "bloc_objectif", "bloc_package", "bloc_exercice", "bloc_aller_loin",
    "bloc_attention", "bloc_astuce", "bloc_notes",
)
_FENCE = re.compile(r"^(:{3,})\s*(\S*)\s*$")


def _fence_info(line):
    """Return (colon_count, label) for a fence line, or (None, None)."""
    m = _FENCE.match(line.rstrip("\n"))
    if not m:
        return None, None
    return len(m.group(1)), m.group(2)


def iter_blocs_in_markdown(lines):
    """Find top-level bloc regions. Returns list of (start, end, type)."""
    regions = []
    i = 0
    n = len(lines)
    while i < n:
        colons, label = _fence_info(lines[i])
        if colons and label in KNOWN_TYPES:
            # find matching close: same colon count, empty label, tracking nesting
            depth = 1
            j = i + 1
            while j < n:
                c, lab = _fence_info(lines[j])
                if c:
                    if lab:            # an opening fence (has a label)
                        depth += 1
                    else:              # a closing fence (bare :::)
                        depth -= 1
                        if depth == 0:
                            break
                j += 1
            regions.append((i, j, label))
            i = j + 1
        else:
            i += 1
    return regions


# Bloc types whose inner markdown is kept (fences stripped, content preserved).
KEEP_CONTENT = ("bloc_exercice",)


def _bloc_content(region_lines):
    """Inner markdown of a bloc region: drop the ::: fence lines, keep the rest."""
    return [ln for ln in region_lines if _fence_info(ln)[0] is None]


def strip_blocs(lines):
    """Remove bloc_* callout regions; keep the inner markdown of KEEP_CONTENT types."""
    regions = iter_blocs_in_markdown(lines)
    if not regions:
        return lines
    out, prev = [], 0
    for start, end, btype in regions:
        out.extend(lines[prev:start])
        if btype in KEEP_CONTENT:
            out.extend(_bloc_content(lines[start:end + 1]))
        prev = end + 1
    out.extend(lines[prev:])
    return out


def clean_notebook(nb):
    """Return a cleaned copy of an nbformat notebook dict."""
    cells = nb.get("cells", [])
    new_cells = []
    first_md_seen = False
    for cell in cells:
        if cell["cell_type"] == "markdown":
            src = cell["source"]
            if not first_md_seen:
                src = strip_yaml_header(src)
                first_md_seen = True
            src = strip_html_comments("".join(src)).splitlines(keepends=True)
            src = strip_blocs(src)
            src = strip_images(src)
            src = strip_heading_anchors(src)
            # normalize to canonical one-newline-per-line elements so a second
            # run re-reads the same list shape (idempotency)
            src = "".join(src).splitlines(keepends=True)
            if "".join(src).strip() == "":
                continue          # drop empty markdown cell
            cell = dict(cell, source=src)
        elif cell["cell_type"] == "code":
            src = strip_cell_directives(cell["source"])
            if "".join(src).strip() == "":
                continue          # drop empty code cell
            cell = dict(cell, source=src)
        new_cells.append(cell)

    return dict(nb, cells=new_cells)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Clean Quarto-exported notebooks.")
    ap.add_argument("notebooks", nargs="+")
    args = ap.parse_args(argv)

    for nbp in args.notebooks:
        path = Path(nbp)
        with path.open(encoding="utf-8") as f:
            nb = json.load(f)
        nb = clean_notebook(nb)
        with path.open("w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
