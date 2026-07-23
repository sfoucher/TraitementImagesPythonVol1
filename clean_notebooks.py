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
