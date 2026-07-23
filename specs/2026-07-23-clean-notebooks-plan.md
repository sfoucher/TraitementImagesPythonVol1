# clean_notebooks.py Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A stdlib Python script that cleans Quarto-exported notebooks — strips the YAML header, HTML comments and `#|` directives, and renders `bloc_*` callouts as inline-styled HTML reusing the body markup already in `docs/`.

**Architecture:** Single module `clean_notebooks.py` at repo root, composed of small pure functions (one transform each) plus an orchestrator and a CLI. Body HTML for callouts is extracted from `docs/<stem>.html` with `html.parser`. Wired into `process.sh` after `quarto convert`.

**Tech Stack:** Python 3.10+ standard library only (`json`, `re`, `base64`, `html.parser`, `pathlib`, `sys`, `argparse`, `collections.namedtuple`). Tests via stdlib `unittest`.

## Global Constraints

- **Stdlib only** — no third-party imports (no bs4, no markdown lib). Copied verbatim from spec: "bibliothèque standard uniquement".
- **In-place edits** must preserve `nbformat`, cell metadata, and cell order.
- **Unicode preserved** — write JSON with `ensure_ascii=False`, `indent=1`, trailing newline (French accented text must not be escaped/mangled).
- **Idempotent** — after cleaning, no `---` header, no `:::`, no `<!--`, no `#|` remain; a second run is a no-op.
- **7 bloc types**: `bloc_objectif`, `bloc_package`, `bloc_exercice`, `bloc_aller_loin`, `bloc_attention`, `bloc_astuce`, `bloc_notes`.
- Tests run from repo root: `python3 -m unittest tests.test_clean_notebooks -v`.
- Commit message trailer on every commit: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

## File Structure

- Create `clean_notebooks.py` — the cleaner (module + CLI).
- Create `tests/__init__.py` — empty, makes `tests` a package.
- Create `tests/test_clean_notebooks.py` — unittest suite.
- Modify `process.sh` — call the cleaner in steps 4 and 5.

---

### Task 1: `strip_html_comments` + scaffolding

**Files:**
- Create: `clean_notebooks.py`
- Create: `tests/__init__.py`
- Create: `tests/test_clean_notebooks.py`

**Interfaces:**
- Produces: `strip_html_comments(text: str) -> str` — removes `<!--- … --->` and `<!-- … -->` (multiline, non-greedy).

- [ ] **Step 1: Write the failing test**

Create `tests/__init__.py` (empty file) and `tests/test_clean_notebooks.py`:

```python
import unittest
from clean_notebooks import strip_html_comments


class TestStripHtmlComments(unittest.TestCase):
    def test_removes_simple_comment(self):
        self.assertEqual(strip_html_comments("a <!-- x --> b"), "a  b")

    def test_removes_triple_dash_comment(self):
        self.assertEqual(strip_html_comments("a <!--- x ---> b"), "a  b")

    def test_removes_multiline_comment(self):
        text = "keep\n<!--\n## draft\nmore\n-->\nend"
        self.assertEqual(strip_html_comments(text), "keep\n\nend")

    def test_no_comment_unchanged(self):
        self.assertEqual(strip_html_comments("nothing here"), "nothing here")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: FAIL — `ImportError: cannot import name 'strip_html_comments'`.

- [ ] **Step 3: Write minimal implementation**

Create `clean_notebooks.py`:

```python
#!/usr/bin/env python3
"""Clean Quarto-exported notebooks (see specs/2026-07-23-clean-notebooks-design.md)."""
import re

_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_html_comments(text: str) -> str:
    """Remove <!-- ... --> and <!--- ... ---> blocks (multiline)."""
    return _HTML_COMMENT.sub("", text)
```

Note: `<!--- x --->` is matched by the same pattern (the extra dashes are inside).

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/__init__.py tests/test_clean_notebooks.py
git commit -m "feat: strip_html_comments + test scaffolding

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: `strip_cell_directives`

**Files:**
- Modify: `clean_notebooks.py`
- Test: `tests/test_clean_notebooks.py`

**Interfaces:**
- Produces: `strip_cell_directives(lines: list[str]) -> list[str]` — drops lines matching `^\s*#\|`.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_clean_notebooks.py`:

```python
from clean_notebooks import strip_cell_directives


class TestStripCellDirectives(unittest.TestCase):
    def test_drops_directive_lines(self):
        lines = ["#| eval: false\n", "#| echo: false\n", "import numpy as np\n"]
        self.assertEqual(strip_cell_directives(lines), ["import numpy as np\n"])

    def test_keeps_normal_comments(self):
        lines = ["# a real comment\n", "x = 1\n"]
        self.assertEqual(strip_cell_directives(lines), ["# a real comment\n", "x = 1\n"])

    def test_drops_indented_directive(self):
        lines = ["    #| output: false\n", "    y = 2\n"]
        self.assertEqual(strip_cell_directives(lines), ["    y = 2\n"])

    def test_all_directives_becomes_empty(self):
        lines = ["#| label: tbl-x\n", "#| tbl-cap: \"T\"\n"]
        self.assertEqual(strip_cell_directives(lines), [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks.TestStripCellDirectives -v`
Expected: FAIL — `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `clean_notebooks.py`:

```python
_DIRECTIVE = re.compile(r"^\s*#\|")


def strip_cell_directives(lines):
    """Drop Quarto cell-option lines (#| ...) from a code cell source list."""
    return [ln for ln in lines if not _DIRECTIVE.match(ln)]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (8 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/test_clean_notebooks.py
git commit -m "feat: strip_cell_directives

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: `strip_yaml_header`

**Files:**
- Modify: `clean_notebooks.py`
- Test: `tests/test_clean_notebooks.py`

**Interfaces:**
- Produces: `strip_yaml_header(lines: list[str]) -> list[str]` — if `lines[0]` is a `---` fence at the very top, remove through the closing `---` (and a following blank line). Otherwise return `lines` unchanged.

- [ ] **Step 1: Write the failing test**

Append:

```python
from clean_notebooks import strip_yaml_header


class TestStripYamlHeader(unittest.TestCase):
    def test_header_only_cell(self):
        lines = ["---\n", "jupyter: python3\n", "eval: false\n", "---"]
        self.assertEqual(strip_yaml_header(lines), [])

    def test_header_then_content(self):
        lines = ["---\n", "jupyter: python3\n", "---\n", "\n", "# Titre\n", "texte\n"]
        self.assertEqual(strip_yaml_header(lines), ["# Titre\n", "texte\n"])

    def test_no_header_unchanged(self):
        lines = ["# Titre\n", "texte\n"]
        self.assertEqual(strip_yaml_header(lines), ["# Titre\n", "texte\n"])

    def test_horizontal_rule_not_header(self):
        # a --- not at position 0 is a normal <hr>, must be preserved
        lines = ["texte\n", "\n", "---\n", "suite\n"]
        self.assertEqual(strip_yaml_header(lines), ["texte\n", "\n", "---\n", "suite\n"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks.TestStripYamlHeader -v`
Expected: FAIL — `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `clean_notebooks.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (12 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/test_clean_notebooks.py
git commit -m "feat: strip_yaml_header

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: `iter_blocs_in_markdown`

**Files:**
- Modify: `clean_notebooks.py`
- Test: `tests/test_clean_notebooks.py`

**Interfaces:**
- Produces: `iter_blocs_in_markdown(lines: list[str]) -> list[tuple[int, int, str]]` — returns `(start, end, bloc_type)` for each **top-level** bloc region: `start` = index of the opening `::: bloc_TYPE` line, `end` = index of its matching closing fence line (inclusive), `bloc_type` e.g. `"bloc_objectif"`. Nested `-header/-icon/-body` fences are consumed inside the region, not reported separately.

- [ ] **Step 1: Write the failing test**

Append:

```python
from clean_notebooks import iter_blocs_in_markdown


class TestIterBlocs(unittest.TestCase):
    def test_single_bloc_bounds(self):
        lines = [
            "intro\n",                       # 0
            ":::::: bloc_objectif\n",        # 1  open (depth 6)
            ":::: bloc_objectif-header\n",   # 2
            "::: bloc_objectif-icon\n",      # 3
            ":::\n",                          # 4
            "**Titre**\n",                   # 5
            "::::\n",                         # 6
            "::: bloc_objectif-body\n",      # 7
            "corps\n",                        # 8
            ":::\n",                          # 9
            "::::::\n",                        # 10 close (depth 6)
            "apres\n",                        # 11
        ]
        self.assertEqual(iter_blocs_in_markdown(lines), [(1, 10, "bloc_objectif")])

    def test_two_blocs(self):
        lines = [
            "::: bloc_notes\n", "a\n", ":::\n",
            "mid\n",
            "::: bloc_astuce\n", "b\n", ":::\n",
        ]
        self.assertEqual(
            iter_blocs_in_markdown(lines),
            [(0, 2, "bloc_notes"), (4, 6, "bloc_astuce")],
        )

    def test_no_bloc(self):
        self.assertEqual(iter_blocs_in_markdown(["plain\n", "text\n"]), [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks.TestIterBlocs -v`
Expected: FAIL — `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `clean_notebooks.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (15 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/test_clean_notebooks.py
git commit -m "feat: iter_blocs_in_markdown (fence region detection)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: `parse_docs_blocs`

**Files:**
- Modify: `clean_notebooks.py`
- Test: `tests/test_clean_notebooks.py`

**Interfaces:**
- Produces:
  - `Bloc = namedtuple("Bloc", "type header_html body_html")`
  - `parse_docs_blocs(html: str) -> list[Bloc]` — in document order, extracts each callout's type, inner HTML of its `-header` (minus the `-icon` div) and inner HTML of its `-body`.

- [ ] **Step 1: Write the failing test**

Append:

```python
from clean_notebooks import parse_docs_blocs, Bloc

DOCS_FRAGMENT = """
<p>avant</p>
<div class="bloc_objectif">
<div class="bloc_objectif-header">
<div class="bloc_objectif-icon">

</div>
<p><strong>Objectifs</strong></p>
</div>
<div class="bloc_objectif-body">
<p>intro&nbsp;:</p>
<ul>
<li>un</li>
<li>deux</li>
</ul>
</div>
</div>
<p>apres</p>
"""


class TestParseDocsBlocs(unittest.TestCase):
    def test_extracts_one_bloc(self):
        blocs = parse_docs_blocs(DOCS_FRAGMENT)
        self.assertEqual(len(blocs), 1)
        b = blocs[0]
        self.assertEqual(b.type, "bloc_objectif")
        self.assertIn("<strong>Objectifs</strong>", b.header_html)
        self.assertIn("<li>un</li>", b.body_html)
        self.assertIn("<li>deux</li>", b.body_html)
        # the icon div must not leak into the header
        self.assertNotIn("bloc_objectif-icon", b.header_html)

    def test_no_bloc(self):
        self.assertEqual(parse_docs_blocs("<p>rien</p>"), [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks.TestParseDocsBlocs -v`
Expected: FAIL — `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `clean_notebooks.py`:

```python
from collections import namedtuple
from html.parser import HTMLParser

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


def parse_docs_blocs(html):
    """Extract callouts (type, header inner HTML, body inner HTML) in order."""
    p = _BlocParser()
    p.feed(html)
    return p.blocs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (17 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/test_clean_notebooks.py
git commit -m "feat: parse_docs_blocs (extract rendered callout HTML from docs)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 6: color map, `icon_data_uri`, `render_bloc_html`

**Files:**
- Modify: `clean_notebooks.py`
- Test: `tests/test_clean_notebooks.py`

**Interfaces:**
- Produces:
  - `BLOC_COLORS: dict[str, tuple[str, str]]` — type → (left-border hex, header-bg hex).
  - `ICON_FILES: dict[str, str]` — type → PNG filename under images dir.
  - `icon_data_uri(bloc_type: str, images_dir) -> str | None` — base64 `data:` URI, or `None` if the file is missing.
  - `render_bloc_html(bloc_type: str, header_html: str, body_html: str, icon_uri: str | None) -> str` — self-contained inline-styled `<div>` box.

- [ ] **Step 1: Write the failing test**

Append:

```python
import os
import tempfile
from clean_notebooks import (BLOC_COLORS, ICON_FILES, icon_data_uri,
                             render_bloc_html)


class TestRenderBlocHtml(unittest.TestCase):
    def test_all_types_have_colors_and_icons(self):
        from clean_notebooks import KNOWN_TYPES
        for t in KNOWN_TYPES:
            self.assertIn(t, BLOC_COLORS)
            self.assertIn(t, ICON_FILES)

    def test_render_contains_colors_and_body(self):
        html = render_bloc_html(
            "bloc_objectif", "<p><strong>T</strong></p>", "<ul><li>x</li></ul>", None)
        self.assertIn("#00796d", html)   # objectif border color
        self.assertIn("#e2efec", html)   # objectif header bg
        self.assertIn("<strong>T</strong>", html)
        self.assertIn("<li>x</li>", html)
        self.assertTrue(html.lstrip().startswith("<div"))

    def test_render_without_icon_has_no_img(self):
        html = render_bloc_html("bloc_notes", "<p>H</p>", "<p>B</p>", None)
        self.assertNotIn("<img", html)

    def test_render_with_icon_has_data_uri(self):
        html = render_bloc_html("bloc_notes", "<p>H</p>", "<p>B</p>",
                                "data:image/png;base64,AAAA")
        self.assertIn('src="data:image/png;base64,AAAA"', html)

    def test_icon_data_uri_missing_returns_none(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(icon_data_uri("bloc_notes", d))

    def test_icon_data_uri_reads_png(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, ICON_FILES["bloc_notes"]), "wb").write(b"\x89PNG\r\n")
            uri = icon_data_uri("bloc_notes", d)
            self.assertTrue(uri.startswith("data:image/png;base64,"))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks.TestRenderBlocHtml -v`
Expected: FAIL — `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `clean_notebooks.py` (near the top add `import base64` and `from pathlib import Path`):

```python
import base64
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (23 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/test_clean_notebooks.py
git commit -m "feat: render_bloc_html + icon_data_uri + color map

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 7: `render_bloc_markdown` (fallback mode B)

**Files:**
- Modify: `clean_notebooks.py`
- Test: `tests/test_clean_notebooks.py`

**Interfaces:**
- Produces: `render_bloc_markdown(region_lines: list[str]) -> list[str]` — strips all `:::` fence lines and empty `-icon` blocks, keeps title + body, prefixes remaining non-blank lines with `> ` (blockquote). Used when docs HTML is missing or bloc counts mismatch.

- [ ] **Step 1: Write the failing test**

Append:

```python
from clean_notebooks import render_bloc_markdown


class TestRenderBlocMarkdown(unittest.TestCase):
    def test_strips_fences_and_quotes(self):
        region = [
            ":::::: bloc_objectif\n",
            ":::: bloc_objectif-header\n",
            "::: bloc_objectif-icon\n",
            ":::\n",
            "**Titre**\n",
            "::::\n",
            "::: bloc_objectif-body\n",
            "corps\n",
            ":::\n",
            "::::::\n",
        ]
        out = render_bloc_markdown(region)
        self.assertEqual(out, ["> **Titre**\n", "> corps\n"])

    def test_no_fence_lines_remain(self):
        region = ["::: bloc_notes\n", "texte\n", ":::\n"]
        out = "".join(render_bloc_markdown(region))
        self.assertNotIn(":::", out)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks.TestRenderBlocMarkdown -v`
Expected: FAIL — `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `clean_notebooks.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (25 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/test_clean_notebooks.py
git commit -m "feat: render_bloc_markdown fallback

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 8: `clean_notebook` orchestration

**Files:**
- Modify: `clean_notebooks.py`
- Test: `tests/test_clean_notebooks.py`

**Interfaces:**
- Consumes: all functions from Tasks 1–7.
- Produces: `clean_notebook(nb: dict, docs_blocs: list[Bloc], images_dir) -> dict` — returns a cleaned nbformat dict. Applies: YAML strip (first md cell), HTML-comment strip, bloc→HTML replacement (consuming `docs_blocs` in order; fallback to markdown if the notebook's total bloc count ≠ `len(docs_blocs)`), `#|` strip on code cells, and drops cells whose source becomes empty.

- [ ] **Step 1: Write the failing test**

Append:

```python
from clean_notebooks import clean_notebook


def _md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def _code(src):
    return {"cell_type": "code", "metadata": {}, "source": src,
            "outputs": [], "execution_count": None}


class TestCleanNotebook(unittest.TestCase):
    def test_yaml_comment_directive_and_bloc(self):
        nb = {"cells": [
            _md(["---\n", "jupyter: python3\n", "---\n", "\n",
                 "# Titre\n", "<!-- draft -->\n",
                 "::: bloc_notes\n", "**H**\n", "corps\n", ":::\n"]),
            _code(["#| echo: false\n", "x = 1\n"]),
        ], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        blocs = [Bloc("bloc_notes", "<p><strong>H</strong></p>", "<p>corps</p>")]
        out = clean_notebook(nb, blocs, images_dir="/nonexistent")
        md_src = "".join(out["cells"][0]["source"])
        self.assertNotIn("---", md_src)
        self.assertNotIn("<!--", md_src)
        self.assertNotIn(":::", md_src)
        self.assertIn("<strong>H</strong>", md_src)   # HTML render used
        self.assertEqual(out["cells"][1]["source"], ["x = 1\n"])

    def test_count_mismatch_falls_back_to_markdown(self):
        nb = {"cells": [
            _md(["::: bloc_notes\n", "**H**\n", "corps\n", ":::\n"]),
        ], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        out = clean_notebook(nb, docs_blocs=[], images_dir="/nonexistent")
        md_src = "".join(out["cells"][0]["source"])
        self.assertNotIn(":::", md_src)
        self.assertIn("> **H**", md_src)              # blockquote fallback

    def test_empty_code_cell_dropped(self):
        nb = {"cells": [_code(["#| eval: false\n"])],
              "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        out = clean_notebook(nb, [], images_dir="/nonexistent")
        self.assertEqual(out["cells"], [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks.TestCleanNotebook -v`
Expected: FAIL — `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `clean_notebooks.py`:

```python
import sys


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (28 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/test_clean_notebooks.py
git commit -m "feat: clean_notebook orchestration (transforms + fallback + cell drop)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 9: `main` CLI + idempotency (end-to-end)

**Files:**
- Modify: `clean_notebooks.py`
- Test: `tests/test_clean_notebooks.py`

**Interfaces:**
- Consumes: `clean_notebook`, `parse_docs_blocs`.
- Produces: `main(argv: list[str]) -> int` — parses `NB.ipynb [...] [--docs-dir docs] [--images-dir images]`, loads each notebook, finds `<docs-dir>/<stem>.html` (blocs `[]` if absent), writes back with `json.dump(..., ensure_ascii=False, indent=1)` + trailing newline. Returns 0 on success.

- [ ] **Step 1: Write the failing test**

Append:

```python
import json
from clean_notebooks import main


class TestMainEndToEnd(unittest.TestCase):
    def _write_nb(self, path):
        nb = {"cells": [
            {"cell_type": "markdown", "metadata": {},
             "source": ["---\n", "jupyter: python3\n", "---\n", "\n",
                        "# Titre {#sec-x}\n", "<!-- d -->\n",
                        "::: bloc_notes\n", "**H**\n", "corps\n", ":::\n"]},
            {"cell_type": "code", "metadata": {}, "outputs": [],
             "execution_count": None, "source": ["#| echo: false\n", "x = 1\n"]},
        ], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f)

    def test_cleans_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            nbp = os.path.join(d, "03-Chap.ipynb")
            docs = os.path.join(d, "docs")
            os.makedirs(docs)
            open(os.path.join(docs, "03-Chap.html"), "w", encoding="utf-8").write(
                '<div class="bloc_notes"><div class="bloc_notes-header">'
                '<p><strong>H</strong></p></div>'
                '<div class="bloc_notes-body"><p>corps</p></div></div>')
            self._write_nb(nbp)

            rc = main([nbp, "--docs-dir", docs, "--images-dir", d])
            self.assertEqual(rc, 0)
            txt1 = open(nbp, encoding="utf-8").read()
            self.assertNotIn(":::", txt1)
            self.assertNotIn("#|", txt1)
            self.assertNotIn("jupyter: python3", txt1)
            self.assertIn("<strong>H</strong>", txt1)

            # idempotent: second run does not change the file
            main([nbp, "--docs-dir", docs, "--images-dir", d])
            txt2 = open(nbp, encoding="utf-8").read()
            self.assertEqual(txt1, txt2)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_clean_notebooks.TestMainEndToEnd -v`
Expected: FAIL — `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Add to `clean_notebooks.py`:

```python
import argparse
import json


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (29 tests).

- [ ] **Step 5: Commit**

```bash
git add clean_notebooks.py tests/test_clean_notebooks.py
git commit -m "feat: main CLI + idempotency (end-to-end)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 10: Wire into `process.sh` + verify on real notebooks

**Files:**
- Modify: `process.sh:44-54`

**Interfaces:**
- Consumes: `clean_notebooks.py main` via CLI.

- [ ] **Step 1: Add the cleaning call to both export loops**

In `process.sh`, the chapters loop (step 4) currently reads:

```bash
for ch in "${CHAPTERS[@]}"; do
  q quarto convert "$ch.qmd"
  [ "$HAVE_MARIMO" = 1 ] && q marimo convert "$ch.ipynb" -o "./marimo/$ch.py"
  mv -f "$ch.ipynb" ./notebooks/
done
```

Change to (clean before marimo/mv so the exported notebook is clean):

```bash
for ch in "${CHAPTERS[@]}"; do
  q quarto convert "$ch.qmd"
  q python3 clean_notebooks.py "$ch.ipynb"
  [ "$HAVE_MARIMO" = 1 ] && q marimo convert "$ch.ipynb" -o "./marimo/$ch.py"
  mv -f "$ch.ipynb" ./notebooks/
done
```

And the aux loop (step 5):

```bash
for ch in "${AUX[@]}"; do
  q quarto convert "$ch.qmd"
  mv -f "$ch.ipynb" ./notebooks/
done
```

Change to:

```bash
for ch in "${AUX[@]}"; do
  q quarto convert "$ch.qmd"
  q python3 clean_notebooks.py "$ch.ipynb"
  mv -f "$ch.ipynb" ./notebooks/
done
```

- [ ] **Step 2: Run the full unittest suite once more**

Run: `python3 -m unittest tests.test_clean_notebooks -v`
Expected: PASS (29 tests).

- [ ] **Step 3: Verify the cleaner on one real notebook (dry check, no build)**

Run (uses the already-built `docs/`):

```bash
cp notebooks/00-PriseEnMainPython.ipynb /tmp/nb-check.ipynb
q python3 clean_notebooks.py /tmp/nb-check.ipynb --docs-dir docs --images-dir images
python3 - <<'PY'
import json
j = json.load(open("/tmp/nb-check.ipynb"))
txt = json.dumps(j, ensure_ascii=False)
assert ":::" not in txt, "fences remain"
assert "jupyter: python3" not in txt, "yaml header remains"
assert "#|" not in txt, "directives remain"
assert 'style="border' in txt, "bloc HTML not rendered"
print("OK: real-notebook clean verified")
PY
```

Expected: `OK: real-notebook clean verified`.

- [ ] **Step 4: Run the full build to confirm end-to-end**

Run: `./process.sh`
Expected: exit 0; `notebooks/*.ipynb` regenerated and clean.

- [ ] **Step 5: Commit**

```bash
git add process.sh
git commit -m "build: run clean_notebooks.py after quarto convert in process.sh

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Notes for the implementer

- Run all commands from the repo root `/home/sfoucher/DEV/TraitementImagesPythonVol1`.
- `q` is the docker helper defined in `process.sh`: `q() { docker run --rm -v "$PWD":/workspace mlsysbook-linux:v2 "$@"; }`. To run the cleaner in the container manually: `docker run --rm -v "$PWD":/workspace mlsysbook-linux:v2 python3 clean_notebooks.py <args>`.
- The generated `notebooks/*.ipynb` are build outputs; commit them separately from the script/tests (as the project already does for regenerated content).
- Do not add third-party imports — the whole point is zero image rebuild.
