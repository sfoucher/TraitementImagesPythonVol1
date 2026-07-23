#!/usr/bin/env python3
"""Clean Quarto-exported notebooks (see specs/2026-07-23-clean-notebooks-design.md)."""
import re

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
