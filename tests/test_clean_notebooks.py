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
