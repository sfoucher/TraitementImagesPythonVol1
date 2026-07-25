import unittest

from make_exercices import chapter_title, extract_exercices, CHAPTERS, build

CHAPTER = """---
jupyter: python3
---

# Mon chapitre {#sec-chap09}

Du texte.

## Points clés

:::::: bloc_notes
::: bloc_notes-body
- un point
:::
::::::

## Exercices

:::::: bloc_exercice
:::: bloc_exercice-header
::: bloc_exercice-icon
:::

**À vous de jouer**
::::

::: bloc_exercice-body
1.  Premier exercice.
2.  Second exercice.
:::
::::::

<details>
<summary>Solutions</summary>

``` python
print("réponse")
```

</details>

:::::: bloc_package
::: bloc_package-body
- numpy
:::
::::::

## Quiz
"""


class TestChapterTitle(unittest.TestCase):
    def test_strips_sec_anchor(self):
        self.assertEqual(chapter_title(CHAPTER), "Mon chapitre")

    def test_fallback_without_anchor(self):
        self.assertEqual(chapter_title("# Titre nu\n\ntexte"), "Titre nu")


class TestExtractExercices(unittest.TestCase):
    def setUp(self):
        self.block = extract_exercices(CHAPTER)

    def test_captures_exercice_block(self):
        self.assertTrue(self.block.startswith(":::::: bloc_exercice"))
        self.assertIn("Premier exercice.", self.block)
        self.assertIn("Second exercice.", self.block)

    def test_includes_solutions_details(self):
        self.assertIn("<details>", self.block)
        self.assertTrue(self.block.rstrip().endswith("</details>"))

    def test_excludes_package_and_quiz(self):
        # must stop at </details>, never reaching the package block or Quiz
        self.assertNotIn("bloc_package", self.block)
        self.assertNotIn("## Quiz", self.block)

    def test_none_when_no_exercices(self):
        self.assertIsNone(extract_exercices("# X {#sec-x}\n\nNo exercises here."))


class TestBuildOnRepo(unittest.TestCase):
    def test_every_chapter_contributes_a_section(self):
        out = build(".")
        self.assertIn("# Exercices {#sec-exercices}", out)
        # one "## " section per chapter, each carrying an exercise div
        self.assertEqual(out.count("\n:::::: bloc_exercice"), len(CHAPTERS))


if __name__ == "__main__":
    unittest.main()
