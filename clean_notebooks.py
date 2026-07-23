#!/usr/bin/env python3
"""Clean Quarto-exported notebooks (see specs/2026-07-23-clean-notebooks-design.md)."""
import argparse
import base64
import json
import re
import sys
from collections import namedtuple
from html.parser import HTMLParser
from pathlib import Path

# type -> (left border color, header background) — from css/r4ds.scss
BLOC_COLORS = {
    "bloc_objectif": ("#00796d", "#e2efec"),
    "bloc_package": ("#352c76", "#e2e1f2"),
    "bloc_exercice": ("#e34692", "#fbe8f2"),
    "bloc_aller_loin": ("#eb5f23", "#fef4ec"),
    "bloc_attention": ("#f0ae4e", "#fef4ec"),
    "bloc_astuce": ("#31ae74", "#f0f6ec"),
    "bloc_notes": ("#357cc0", "#eef5fb"),
}
ICON_FILES = {
    "bloc_objectif": "BlocObjectif.png",
    "bloc_package": "BlocPackage.png",
    "bloc_exercice": "BlocExercice.png",
    "bloc_aller_loin": "BlocAllerPlusLoin.png",
    "bloc_attention": "BlocAttention.png",
    "bloc_astuce": "BlocAstuce.png",
    "bloc_notes": "BlocNote.png",
}
CONTAINER_BG = "#FAF9FF"


def icon_data_uri(bloc_type, images_dir):
    """Return a base64 data: URI for the bloc icon, or None if missing."""
    p = Path(images_dir) / ICON_FILES[bloc_type]
    if not p.is_file():
        return None
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return "data:image/png;base64," + b64


def render_bloc_html(bloc_type, header_html, body_html, icon_uri):
    """Self-contained inline-styled callout box (renders without theme CSS)."""
    border, header_bg = BLOC_COLORS[bloc_type]
    img = '<img src="%s" width="16" height="16" alt=""/>' % icon_uri if icon_uri else ""
    container = (
        "border:0.5px solid silver;border-left:.3rem solid %s;"
        "border-radius:.25rem;background:%s;margin:1em 0;" % (border, CONTAINER_BG)
    )
    header = (
        "display:flex;align-items:center;gap:.5rem;padding:.4em .6em;"
        "background:%s;font-weight:700;" % header_bg
    )
    body = "padding:.3em .6em;font-size:.95em;"
    return (
        '<div style="%s">\n'
        '<div style="%s">%s<span>%s</span></div>\n'
        '<div style="%s">\n%s\n</div>\n'
        '</div>'
    ) % (container, header, img, header_html, body, body_html)


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


Bloc = namedtuple("Bloc", "type header_html body_html")


def _starttag_str(tag, attrs, selfclose=False):
    parts = []
    for k, v in attrs:
        parts.append(' %s="%s"' % (k, v) if v is not None else " %s" % k)
    return "<%s%s%s>" % (tag, "".join(parts), " /" if selfclose else "")


class _BlocParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocs = []
        self._divdepth = 0
        self._cur = None          # {"type","header":[],"body":[],"depth"}
        # stack of (capture, divdepth); capture in {"header","body","_skip"}.
        # A stack (not a flat flag) is required because the -icon div nests
        # inside -header: when the icon closes we must RESTORE "header" capture,
        # not reset to None, or the title after the icon is lost.
        self._capstack = []

    @property
    def _cap(self):
        return self._capstack[-1][0] if self._capstack else None

    def _emit(self, s):
        if self._cap in ("header", "body"):
            self._cur[self._cap].append(s)

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            self._divdepth += 1
            cls = dict(attrs).get("class", "")
            if self._cur is None and cls in KNOWN_TYPES:
                self._cur = {"type": cls, "header": [], "body": [],
                             "depth": self._divdepth}
                return
            if self._cur is not None:
                t = self._cur["type"]
                if cls == t + "-header":
                    self._capstack.append(("header", self._divdepth))
                    return
                if cls == t + "-body":
                    self._capstack.append(("body", self._divdepth))
                    return
                if cls == t + "-icon":
                    self._capstack.append(("_skip", self._divdepth))
                    return
            self._emit(_starttag_str(tag, attrs))
            return
        self._emit(_starttag_str(tag, attrs))

    def handle_startendtag(self, tag, attrs):
        self._emit(_starttag_str(tag, attrs, selfclose=True))

    def handle_data(self, data):
        self._emit(data)

    def handle_endtag(self, tag):
        if tag != "div":
            self._emit("</%s>" % tag)
            return
        # closing a div: first, does it close the current capture region?
        if self._capstack and self._divdepth == self._capstack[-1][1]:
            self._capstack.pop()
            self._divdepth -= 1
            return
        if self._cur is not None and self._divdepth == self._cur["depth"]:
            self.blocs.append(Bloc(
                self._cur["type"],
                "".join(self._cur["header"]).strip(),
                "".join(self._cur["body"]).strip(),
            ))
            self._cur = None
            self._divdepth -= 1
            return
        self._divdepth -= 1
        self._emit("</div>")


def render_bloc_markdown(region_lines):
    """Fallback: strip ::: fences, quote the remaining title + body."""
    out = []
    for ln in region_lines:
        colons, _ = _fence_info(ln)
        if colons:            # any fence line -> drop
            continue
        if ln.strip() == "":  # drop blank lines inside the box
            continue
        out.append("> " + ln if not ln.startswith(">") else ln)
    return out


def parse_docs_blocs(html):
    """Extract callouts (type, header inner HTML, body inner HTML) in order."""
    p = _BlocParser()
    p.feed(html)
    return p.blocs


def _count_blocs(cells):
    total = 0
    for c in cells:
        if c["cell_type"] == "markdown":
            total += len(iter_blocs_in_markdown(c["source"]))
    return total


def _replace_blocs_html(lines, bloc_iter, images_dir):
    regions = iter_blocs_in_markdown(lines)
    if not regions:
        return lines
    out, prev = [], 0
    for start, end, _type in regions:
        out.extend(lines[prev:start])
        b = next(bloc_iter)
        uri = icon_data_uri(b.type, images_dir)
        out.append(render_bloc_html(b.type, b.header_html, b.body_html, uri) + "\n")
        prev = end + 1
    out.extend(lines[prev:])
    return out


def _replace_blocs_markdown(lines):
    regions = iter_blocs_in_markdown(lines)
    if not regions:
        return lines
    out, prev = [], 0
    for start, end, _type in regions:
        out.extend(lines[prev:start])
        out.extend(render_bloc_markdown(lines[start:end + 1]))
        prev = end + 1
    out.extend(lines[prev:])
    return out


def clean_notebook(nb, docs_blocs, images_dir):
    """Return a cleaned copy of an nbformat notebook dict."""
    cells = nb.get("cells", [])
    use_html = _count_blocs(cells) == len(docs_blocs)
    if not use_html:
        sys.stderr.write(
            "WARN: bloc count != docs bloc count; using markdown fallback\n")
    bloc_iter = iter(docs_blocs)

    new_cells = []
    first_md_seen = False
    for cell in cells:
        if cell["cell_type"] == "markdown":
            src = cell["source"]
            if not first_md_seen:
                src = strip_yaml_header(src)
                first_md_seen = True
            src = strip_html_comments("".join(src)).splitlines(keepends=True)
            if use_html:
                src = _replace_blocs_html(src, bloc_iter, images_dir)
            else:
                src = _replace_blocs_markdown(src)
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
    ap.add_argument("--docs-dir", default="docs")
    ap.add_argument("--images-dir", default="images")
    args = ap.parse_args(argv)

    for nbp in args.notebooks:
        path = Path(nbp)
        with path.open(encoding="utf-8") as f:
            nb = json.load(f)
        html_path = Path(args.docs_dir) / (path.stem + ".html")
        docs_blocs = parse_docs_blocs(html_path.read_text(encoding="utf-8")) \
            if html_path.is_file() else []
        nb = clean_notebook(nb, docs_blocs, args.images_dir)
        with path.open("w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
