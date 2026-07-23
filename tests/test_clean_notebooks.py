import unittest
from clean_notebooks import strip_html_comments, strip_cell_directives


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
