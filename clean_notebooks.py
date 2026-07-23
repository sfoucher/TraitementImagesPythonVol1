#!/usr/bin/env python3
"""Clean Quarto-exported notebooks (see specs/2026-07-23-clean-notebooks-design.md)."""
import re
from collections import namedtuple
from html.parser import HTMLParser

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


def parse_docs_blocs(html):
    """Extract callouts (type, header inner HTML, body inner HTML) in order."""
    p = _BlocParser()
    p.feed(html)
    return p.blocs
