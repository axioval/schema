"""Source-level contracts for the bilingual documentation UX."""

from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.mkdocs_hooks import _label_task_inputs, _verify_localized_diagram_output

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


class DocumentationUxTests(unittest.TestCase):
    def public_pages(self) -> list[Path]:
        return sorted(
            path
            for path in DOCS.rglob("*.md")
            if path.name != "AGENTS.md" and not path.name.endswith(".de.md")
        )

    def test_every_public_page_has_a_german_sibling(self) -> None:
        pages = self.public_pages()
        self.assertEqual(len(pages), 13)
        missing = [
            path.relative_to(DOCS)
            for path in pages
            if not path.with_name(f"{path.stem}.de.md").is_file()
        ]
        self.assertEqual(missing, [])

    def test_scope_lists_show_included_and_excluded_responsibilities(self) -> None:
        for name in ("layers.md", "layers.de.md"):
            content = (DOCS / "concepts" / name).read_text(encoding="utf-8")
            self.assertEqual(
                content.count('class="scope-list scope-list--included"'), 1
            )
            self.assertEqual(
                content.count('class="scope-list scope-list--excluded"'), 1
            )

    def test_reader_code_is_collapsed_by_default(self) -> None:
        files = [
            *self.public_pages(),
            *DOCS.rglob("*.de.md"),
            ROOT / "CONTRIBUTING.md",
        ]
        exposed: list[str] = []
        for path in files:
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                if re.match(r"^```", line):
                    exposed.append(f"{path.relative_to(ROOT)}:{number}")
        self.assertEqual(exposed, [])

    def test_locale_and_interaction_configuration_is_pinned(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        requirements = (ROOT / "requirements-docs.txt").read_text(encoding="utf-8")
        for contract in (
            "mkdocs-static-i18n==1.3.1",
            "mkdocs-material==9.6.20",
            "Pygments==2.19.2",
        ):
            self.assertIn(contract, requirements)
        for contract in (
            "docs_structure: suffix",
            "fallback_to_default: false",
            "locale: de",
            "pymdownx.tasklist:",
            "assets/javascripts/site.js",
        ):
            self.assertIn(contract, config)

    def test_diagrams_have_complete_german_variants(self) -> None:
        images = DOCS / "assets" / "images"
        originals = sorted(
            path for path in images.glob("*.svg") if not path.name.endswith(".de.svg")
        )
        self.assertEqual(len(originals), 7)
        for original in originals:
            translated = original.with_name(f"{original.stem}.de.svg")
            self.assertTrue(translated.is_file(), translated.name)
            svg = ET.parse(translated).getroot()
            self.assertEqual(svg.attrib.get("role"), "img")
            self.assertTrue(svg.attrib.get("aria-labelledby"))
            self.assertFalse(
                any(node.tag.rsplit("}", 1)[-1] == "script" for node in svg.iter())
            )
            visible_text = " ".join(
                (node.text or "").strip()
                for node in svg.iter()
                if node.tag.rsplit("}", 1)[-1] in {"title", "desc", "text", "tspan"}
            )
            self.assertNotRegex(
                visible_text.lower(),
                r"\b(describe|check|share|bundle|tool|together|dictionary|recipe|filled|card|work|for)\b",
            )

        for page in sorted(DOCS.rglob("*.de.md")):
            source = page.read_text(encoding="utf-8")
            raw_sources = re.findall(
                r'<(?:source|img)[^>]+(?:srcset|src)="([^"]+\.svg)"', source
            )
            for reference in raw_sources:
                self.assertFalse(reference.endswith(".de.svg"), f"{page}: {reference}")
                stem = Path(reference).name.removesuffix(".svg")
                self.assertTrue((images / f"{stem}.de.svg").is_file(), reference)
            markdown = re.sub(r"<(?:source|img)[^>]+>", "", source)
            for reference in re.findall(
                r"(?:\.\./)*assets/images/[^\s\"')>]+\.svg", markdown
            ):
                self.assertTrue(reference.endswith(".de.svg"), f"{page}: {reference}")
                self.assertTrue((images / Path(reference).name).is_file(), reference)

    def test_generated_german_diagram_routes_fail_closed(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            page = site / "de" / "guide" / "topic" / "index.html"
            image = site / "de" / "assets" / "images" / "test.svg"
            sources = site / "sources"
            page.parent.mkdir(parents=True)
            image.parent.mkdir(parents=True)
            sources.mkdir()
            image.write_text("<svg/>", encoding="utf-8")
            (sources / "test.de.svg").write_text("<svg/>", encoding="utf-8")
            page.write_text(
                '<img src="../../assets/images/test.svg">', encoding="utf-8"
            )
            _verify_localized_diagram_output(site, sources)
            for broken in ("test.de.svg", "missing.svg"):
                page.write_text(
                    f'<img src="../../assets/images/{broken}">', encoding="utf-8"
                )
                with self.assertRaisesRegex(RuntimeError, "invalid German diagram"):
                    _verify_localized_diagram_output(site, sources)
            page.write_text(
                '<img src="../../assets/images/test.svg">', encoding="utf-8"
            )
            image.write_text('<svg id="wrong"/>', encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "does not match"):
                _verify_localized_diagram_output(site, sources)

    def test_site_script_keeps_svg_and_locale_boundaries(self) -> None:
        script = (DOCS / "assets" / "javascripts" / "site.js").read_text(
            encoding="utf-8"
        )
        for contract in (
            "url.origin !== location.origin",
            '!url.pathname.includes("/assets/images/")',
            'svg.querySelector("script, foreignObject")',
            "localStorage.getItem(languageKey)",
            "localStorage.getItem(navKey)",
            "a[hreflang]",
            ".md-content h1, .md-content h2",
        ):
            self.assertIn(contract, script)

    def test_material_icon_set_is_complete(self) -> None:
        icon_dir = DOCS / "assets" / "icons"
        required = {
            "account-group",
            "arrow-right",
            "check-circle",
            "close-circle",
            "compass",
            "file-document",
            "help-circle",
            "home",
            "layers",
            "license",
            "lightbulb",
            "map-marker",
            "map-marker-path",
            "package",
            "shape",
            "share",
            "shield-check",
            "source-repository",
            "tools",
            "wall",
        }
        missing = sorted(
            name for name in required if not (icon_dir / f"{name}.svg").is_file()
        )
        self.assertEqual(missing, [])

    def test_task_list_controls_receive_static_accessible_names(self) -> None:
        source = (
            '<li class="task-list-item"><label class="task-list-control">'
            '<input type="checkbox" disabled/><span></span></label> '
            "Read &amp; verify</li>"
        )
        rendered = _label_task_inputs(source)
        self.assertIn('disabled aria-label="Read &amp; verify"/>', rendered)
        self.assertNotIn("disabled/ aria-label", rendered)
        self.assertEqual(_label_task_inputs(rendered), rendered)

    def test_publication_checklist_remains_a_real_task_list(self) -> None:
        authoring = (DOCS / "authoring.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"^- \[ \] ", authoring, re.MULTILINE)), 7)


if __name__ == "__main__":
    unittest.main()
