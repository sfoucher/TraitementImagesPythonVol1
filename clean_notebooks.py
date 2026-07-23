#!/usr/bin/env python3
"""Clean Quarto-exported notebooks (see specs/2026-07-23-clean-notebooks-design.md)."""
import re

_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_html_comments(text: str) -> str:
    """Remove <!-- ... --> and <!--- ... ---> blocks (multiline)."""
    return _HTML_COMMENT.sub("", text)
