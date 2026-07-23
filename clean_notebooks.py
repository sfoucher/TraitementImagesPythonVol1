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
