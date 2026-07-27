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


from clean_notebooks import strip_heading_anchors


class TestStripHeadingAnchors(unittest.TestCase):
    def test_strips_id_anchor(self):
        self.assertEqual(
            strip_heading_anchors(["## Créer un exécutable {#sec-00-executable}\n"]),
            ["## Créer un exécutable\n"])

    def test_strips_id_and_classes(self):
        self.assertEqual(
            strip_heading_anchors(["# Titre {#sec-x .unnumbered}\n"]),
            ["# Titre\n"])

    def test_plain_heading_unchanged(self):
        self.assertEqual(strip_heading_anchors(["## Titre\n"]), ["## Titre\n"])

    def test_non_heading_not_touched(self):
        # a {#x} in body text is not a heading -> left alone
        self.assertEqual(strip_heading_anchors(["voir {#x}\n"]), ["voir {#x}\n"])

    def test_preserves_missing_trailing_newline(self):
        self.assertEqual(strip_heading_anchors(["## T {#s}"]), ["## T"])


from clean_notebooks import strip_images


class TestStripImages(unittest.TestCase):
    def test_removes_plain_image(self):
        self.assertEqual(
            strip_images(["![Fenêtre principale.](images/jupyter-accueil.png)\n"]),
            [])

    def test_removes_image_with_attrs(self):
        self.assertEqual(
            strip_images(["![leg](images/x.png){fig-align=\"center\"}\n"]), [])

    def test_keeps_surrounding_text(self):
        lines = ["avant\n", "![a](img/y.png)\n", "apres\n"]
        self.assertEqual(strip_images(lines), ["avant\n", "apres\n"])

    def test_inline_image_in_prose_kept(self):
        # an image mid-sentence is not a standalone line -> left alone
        lines = ["voir ![a](img/y.png) ici\n"]
        self.assertEqual(strip_images(lines), ["voir ![a](img/y.png) ici\n"])


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


from clean_notebooks import strip_blocs


class TestStripBlocs(unittest.TestCase):
    def test_removes_region_keeps_surroundings(self):
        lines = [
            "avant\n",
            "::: bloc_notes\n", "**H**\n", "corps\n", ":::\n",
            "apres\n",
        ]
        self.assertEqual(strip_blocs(lines), ["avant\n", "apres\n"])

    def test_no_bloc_unchanged(self):
        lines = ["a\n", "b\n"]
        self.assertEqual(strip_blocs(lines), ["a\n", "b\n"])

    def test_removes_two_blocs(self):
        lines = [
            "::: bloc_notes\n", "a\n", ":::\n",
            "mid\n",
            "::: bloc_astuce\n", "b\n", ":::\n",
        ]
        self.assertEqual(strip_blocs(lines), ["mid\n"])

    def test_keeps_exercice_content(self):
        lines = [
            "avant\n",
            ":::::: bloc_exercice\n",
            ":::: bloc_exercice-header\n",
            "::: bloc_exercice-icon\n", ":::\n",
            "**Exercice 1**\n",
            "::::\n",
            "::: bloc_exercice-body\n",
            "Calculez le NDVI.\n",
            ":::\n",
            "::::::\n",
            "apres\n",
        ]
        self.assertEqual(
            strip_blocs(lines),
            ["avant\n", "**Exercice 1**\n", "Calculez le NDVI.\n", "apres\n"])

    def test_removes_other_blocs_keeps_exercice(self):
        lines = [
            "::: bloc_notes\n", "note\n", ":::\n",
            "::: bloc_exercice\n", "consigne\n", ":::\n",
        ]
        self.assertEqual(strip_blocs(lines), ["consigne\n"])


import os
import tempfile
import json
from clean_notebooks import clean_notebook, main


def _md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def _code(src):
    return {"cell_type": "code", "metadata": {}, "source": src,
            "outputs": [], "execution_count": None}


class TestCleanNotebook(unittest.TestCase):
    def test_yaml_comment_directive_anchor_and_bloc(self):
        nb = {"cells": [
            _md(["---\n", "jupyter: python3\n", "---\n", "\n",
                 "# Titre {#sec-x}\n", "<!-- draft -->\n", "texte\n",
                 "![leg](images/x.png)\n",
                 "::: bloc_notes\n", "**H**\n", "corps\n", ":::\n"]),
            _code(["#| echo: false\n", "x = 1\n"]),
        ], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        out = clean_notebook(nb)
        md_src = "".join(out["cells"][0]["source"])
        self.assertNotIn("---", md_src)          # yaml gone
        self.assertNotIn("<!--", md_src)         # comment gone
        self.assertNotIn(":::", md_src)          # bloc removed
        self.assertNotIn("**H**", md_src)        # bloc body removed
        self.assertNotIn("![leg]", md_src)       # image line removed
        self.assertNotIn("{#sec-x}", md_src)     # heading anchor stripped
        self.assertIn("# Titre\n", md_src)       # heading text kept
        self.assertIn("texte", md_src)
        self.assertEqual(out["cells"][1]["source"], ["x = 1\n"])

    def test_bloc_only_markdown_cell_dropped(self):
        nb = {"cells": [
            _md(["::: bloc_notes\n", "**H**\n", "corps\n", ":::\n"]),
        ], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        out = clean_notebook(nb)
        self.assertEqual(out["cells"], [])

    def test_empty_code_cell_dropped(self):
        nb = {"cells": [_code(["#| eval: false\n"])],
              "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        out = clean_notebook(nb)
        self.assertEqual(out["cells"], [])


class TestMainEndToEnd(unittest.TestCase):
    def _write_nb(self, path):
        nb = {"cells": [
            {"cell_type": "markdown", "metadata": {},
             "source": ["---\n", "jupyter: python3\n", "---\n", "\n",
                        "# Titre {#sec-x}\n", "<!-- d -->\n", "texte\n",
                        "::: bloc_notes\n", "**H**\n", "corps\n", ":::\n"]},
            {"cell_type": "code", "metadata": {}, "outputs": [],
             "execution_count": None, "source": ["#| echo: false\n", "x = 1\n"]},
        ], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f)

    def test_cleans_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            nbp = os.path.join(d, "03-Chap.ipynb")
            self._write_nb(nbp)

            rc = main([nbp])
            self.assertEqual(rc, 0)
            txt1 = open(nbp, encoding="utf-8").read()
            self.assertNotIn(":::", txt1)
            self.assertNotIn("#|", txt1)
            self.assertNotIn("jupyter: python3", txt1)
            self.assertNotIn("{#sec-x}", txt1)
            self.assertIn("Titre", txt1)

            # idempotent: second run does not change the file
            main([nbp])
            txt2 = open(nbp, encoding="utf-8").read()
            self.assertEqual(txt1, txt2)


if __name__ == "__main__":
    unittest.main()
