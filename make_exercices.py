#!/usr/bin/env python3
"""Generate 08-Exercices.qmd by aggregating each chapter's « Exercices » block.

The file 08-Exercices.qmd is DERIVED — do not edit it by hand; edit the
exercises in the chapter files, then regenerate. process.sh runs this before
rendering so the consolidated chapter is always in sync. Standard library only.

Run from the repository root:  python3 make_exercices.py
Test:                          python3 -m unittest tests.test_make_exercices -v
"""
import re
import pathlib

# Chapters in reading order; each contributes one « Exercices » section.
CHAPTERS = [
    "00-PriseEnMainPython.qmd",
    "01-ImportationManipulationImages.qmd",
    "02-RehaussementVisualisationImages.qmd",
    "03-TransformationSpectrales.qmd",
    "04-TransformationSpatiales.qmd",
    "05-ClassificationsSupervisees.qmd",
]
OUT = "08-Exercices.qmd"


def chapter_title(text):
    """Chapter title from its H1 (`# Titre {#sec-chapNN}`)."""
    m = re.search(r"^#\s+(.+?)\s*\{#sec-[^}]+\}\s*$", text, re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return re.sub(r"\s*\{.*\}\s*$", "", m.group(1)).strip() if m else "Chapitre"


def extract_exercices(text):
    """Return the `:::::: bloc_exercice … ::::::` div (plus a following
    `<details>` solutions block, if any), or None if the chapter has none."""
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines)
                  if ln.strip().startswith(":::::: bloc_exercice")), None)
    if start is None:
        return None
    end = next((j for j in range(start + 1, len(lines))
                if lines[j].strip() == "::::::"), None)
    if end is None:
        return None
    block = lines[start:end + 1]

    # Optional solutions block immediately after the exercise div.
    k = end + 1
    while k < len(lines) and lines[k].strip() == "":
        k += 1
    if k < len(lines) and lines[k].lstrip().startswith("<details>"):
        for m in range(k, len(lines)):
            block.append(lines[m])
            if lines[m].strip() == "</details>":
                break
    return "\n".join(block)


def build(root="."):
    """Assemble the consolidated chapter text from the chapter files."""
    root = pathlib.Path(root)
    parts = [
        "---",
        "eval: false",
        "---",
        "",
        "<!-- GÉNÉRÉ par make_exercices.py — NE PAS ÉDITER À LA MAIN. "
        "Modifier les exercices dans les chapitres, puis régénérer. -->",
        "",
        "# Exercices {#sec-exercices}",
        "",
        "Ce chapitre regroupe l'ensemble des exercices proposés au fil des "
        "chapitres, à des fins de révision. Il est **généré automatiquement** à "
        "partir des chapitres (script `make_exercices.py`) : les solutions et le "
        "corrigé se trouvent dans chaque chapitre d'origine.",
        "",
    ]
    for ch in CHAPTERS:
        path = root / ch
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        block = extract_exercices(text)
        if block is None:
            continue
        parts += [f"## {chapter_title(text)}", "", block, ""]
    return "\n".join(parts) + "\n"


def main():
    content = build(".")
    pathlib.Path(OUT).write_text(content, encoding="utf-8")
    n = content.count("\n## ")
    print(f"Wrote {OUT} ({n} chapter sections)")


if __name__ == "__main__":
    main()
