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
