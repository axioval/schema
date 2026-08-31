"""MkDocs hooks for first-class Apple Pkl syntax highlighting."""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import ClassVar

from pygments.lexer import RegexLexer, words
from pygments.lexers import _lexer_cache
from pygments.lexers._mapping import LEXERS
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Whitespace,
)


class PklLexer(RegexLexer):
    """Pygments lexer for Apple's Pkl configuration language."""

    name = "Pkl"
    aliases: ClassVar[list[str]] = ["pkl"]
    filenames: ClassVar[list[str]] = ["*.pkl"]
    mimetypes: ClassVar[list[str]] = ["text/x-pkl"]
    url = "https://pkl-lang.org"
    version_added = "local"

    _keywords = (
        "abstract",
        "amends",
        "as",
        "case",
        "class",
        "const",
        "delete",
        "else",
        "extends",
        "external",
        "fixed",
        "for",
        "function",
        "hidden",
        "if",
        "import",
        "in",
        "is",
        "let",
        "local",
        "module",
        "new",
        "open",
        "out",
        "outer",
        "override",
        "protected",
        "read",
        "record",
        "super",
        "switch",
        "this",
        "throw",
        "trace",
        "typealias",
        "unknown",
        "vararg",
        "when",
    )
    _builtins = (
        "Any",
        "Boolean",
        "DataSize",
        "Duration",
        "Dynamic",
        "Float",
        "Int",
        "List",
        "Listing",
        "Map",
        "Mapping",
        "Nothing",
        "Number",
        "Pair",
        "Set",
        "String",
        "UInt",
        "UInt8",
        "UInt16",
        "UInt32",
        "Unknown",
    )

    tokens: ClassVar = {
        "root": [
            (r"\s+", Whitespace),
            (r"///.*$", Comment.Special),
            (r"//.*$", Comment.Single),
            (r"/\*", Comment.Multiline, "comment"),
            (
                r'(?P<raw_multiline>#+)"""[\s\S]*?"""(?P=raw_multiline)',
                String.Multiline,
            ),
            (
                r'(?P<raw_string>#+)"(?:[^"\n]|"(?!(?P=raw_string)))*"(?P=raw_string)',
                String,
            ),
            (r'"""', String.Multiline, "multiline"),
            (r'"', String, "string"),
            (r"@[A-Za-z_][A-Za-z0-9_]*", Name.Decorator),
            (r"\b(?:import\*|read\*|read\?)", Keyword),
            (words(_keywords, prefix=r"\b", suffix=r"\b"), Keyword),
            (r"\b(?:true|false|null|nothing)\b", Keyword.Constant),
            (words(_builtins, prefix=r"\b", suffix=r"\b"), Name.Builtin),
            (
                r"\b0x[0-9A-Fa-f_]+(?:\.[0-9A-Fa-f_]+)?(?:[pP][+-]?[0-9_]+)?\b",
                Number.Hex,
            ),
            (r"\b0o[0-7_]+\b", Number.Oct),
            (r"\b0b[01_]+\b", Number.Bin),
            (r"\b[0-9][0-9_]*(?:\.[0-9_]+)?(?:[eE][+-]?[0-9_]+)?\b", Number),
            (r"`[^`]+`(?=\s*[=:{])", Name.Attribute),
            (r"[A-Za-z_][A-Za-z0-9_]*(?=\s*[=:{])", Name.Attribute),
            (r"(?<=\.)`[^`]+`", Name.Attribute),
            (r"(?<=\.)[A-Za-z_][A-Za-z0-9_]*", Name.Attribute),
            (r"\b[A-Z][A-Za-z0-9_]*\b", Name.Class),
            (r"`[^`]+`", Name),
            (r"[A-Za-z_][A-Za-z0-9_]*", Name),
            (r"(?:==|!=|<=|>=|&&|\|\||\?\?|\?\.|\*\*|->|[+\-*/%<>=!?|&~.^])", Operator),
            (r"[][(){},;:]", Punctuation),
            (r".", Punctuation),
        ],
        "comment": [
            (r"/\*", Comment.Multiline, "#push"),
            (r"\*/", Comment.Multiline, "#pop"),
            (r"[^*/]+", Comment.Multiline),
            (r"[*/]", Comment.Multiline),
        ],
        "string": [
            (r"\\(?:[0tnr\"']|u\{[0-9A-Fa-f]{1,8}\})", String.Escape),
            (r'"', String, "#pop"),
            (r'[^\\"\n]+|\\.|\n', String),
        ],
        "multiline": [
            (r'"""', String.Multiline, "#pop"),
            (r"\\(?:[0tnr\"']|u\{[0-9A-Fa-f]{1,8}\})", String.Escape),
            (r".|\n", String.Multiline),
        ],
    }


class _PklBlockAudit(HTMLParser):
    """Track whether each rendered Pkl block contains highlighted tokens."""

    _PYGMENTS_TOKENS: ClassVar[frozenset[str]] = frozenset(
        {
            "c",
            "c1",
            "cm",
            "cs",
            "k",
            "kc",
            "m",
            "mb",
            "mh",
            "mi",
            "mo",
            "n",
            "na",
            "nb",
            "nc",
            "nd",
            "nf",
            "nn",
            "no",
            "nt",
            "nv",
            "o",
            "p",
            "s",
            "s1",
            "s2",
            "sa",
            "sb",
            "sc",
            "sd",
            "se",
            "sh",
            "si",
            "sr",
            "ss",
            "sx",
        }
    )

    def __init__(self) -> None:
        super().__init__()
        self._div_depth = 0
        self._has_token = False
        self.blocks: list[bool] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if self._div_depth:
            if tag == "div":
                self._div_depth += 1
            elif tag == "span" and classes & self._PYGMENTS_TOKENS:
                self._has_token = True
        elif tag == "div" and "language-pkl" in classes:
            self._div_depth = 1
            self._has_token = False

    def handle_endtag(self, tag: str) -> None:
        if self._div_depth and tag == "div":
            self._div_depth -= 1
            if not self._div_depth:
                self.blocks.append(self._has_token)


def _verify_lexer_contract() -> None:
    """Exercise delimiter lengths that cannot be represented by fixed lexer states."""

    cases = (
        '####"plain"####',
        '########"embedded "#### delimiter"########',
        '######"""\nmultiline\nwith """##### inside\n"""######',
    )
    lexer = PklLexer()
    for source in cases:
        tokens = list(lexer.get_tokens_unprocessed(source))
        if len(tokens) != 1 or tokens[0][1] not in String or tokens[0][2] != source:
            raise RuntimeError(f"Pkl raw-string lexer contract failed for {source!r}")


def _verify_audit_contract() -> None:
    """Prove layout/UI spans cannot masquerade as syntax highlighting."""

    cases = (
        (
            '<div class="language-pkl"><code><span class="non-token">new</span></code></div>',
            False,
        ),
        (
            '<div class="language-pkl"><code><span class="k">new</span></code></div>',
            True,
        ),
    )
    for fragment, expected in cases:
        parser = _PklBlockAudit()
        parser.feed(fragment)
        if parser.blocks != [expected]:
            raise RuntimeError(f"Pkl highlight audit contract failed for {fragment!r}")


def _verify_svg_contract() -> None:
    """Require local diagrams to carry accessible, self-contained metadata."""

    root = Path(__file__).resolve().parent.parent
    svg_files = sorted((root / "docs" / "assets" / "images").glob("*.svg"))
    if not svg_files:
        raise RuntimeError("documentation contains no local SVG diagrams")

    violations: list[str] = []
    for path in svg_files:
        try:
            document = ET.parse(path)
        except ET.ParseError as error:
            violations.append(f"{path.name}: invalid XML ({error})")
            continue

        svg = document.getroot()
        labels = set(svg.attrib.get("aria-labelledby", "").split())
        if svg.attrib.get("role") != "img":
            violations.append(f"{path.name}: missing role=img")

        for tag_name in ("title", "desc"):
            element = svg.find(f"{{*}}{tag_name}")
            if element is None or not "".join(element.itertext()).strip():
                violations.append(f"{path.name}: missing {tag_name}")
            elif element.attrib.get("id") not in labels:
                violations.append(f"{path.name}: {tag_name} is not aria-labelledby")

        for element in svg.iter():
            if element.tag.rsplit("}", maxsplit=1)[-1] == "script":
                violations.append(f"{path.name}: scripts are not allowed")
            for attribute, value in element.attrib.items():
                attribute_name = attribute.rsplit("}", maxsplit=1)[-1]
                if attribute_name == "href" and not value.startswith("#"):
                    violations.append(
                        f"{path.name}: external references are not allowed"
                    )

    if violations:
        raise RuntimeError("invalid documentation SVG: " + "; ".join(violations))


def _verify_prose_contract() -> None:
    """Keep public and repository documentation free of en and em dashes."""

    root = Path(__file__).resolve().parent.parent
    markdown_files = sorted(
        {
            *root.glob("*.md"),
            *(root / "docs").rglob("*.md"),
            *(root / "examples").rglob("*.md"),
        }
    )
    violations: list[str] = []
    for path in markdown_files:
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if "\N{EN DASH}" in line or "\N{EM DASH}" in line:
                violations.append(f"{path.relative_to(root)}:{line_number}")

    if violations:
        raise RuntimeError(
            "documentation contains en or em dashes: " + ", ".join(violations)
        )


def on_config(config, **_kwargs):
    """Register and verify the lexer before Markdown renders code fences."""

    _verify_lexer_contract()
    _verify_audit_contract()
    _verify_svg_contract()
    _verify_prose_contract()
    LEXERS["PklLexer"] = (
        "scripts.mkdocs_hooks",
        PklLexer.name,
        tuple(PklLexer.aliases),
        tuple(PklLexer.filenames),
        tuple(PklLexer.mimetypes),
    )
    _lexer_cache[PklLexer.name] = PklLexer
    return config


def on_post_build(config, **_kwargs) -> None:
    """Fail the docs build if any Pkl fence silently falls back to plain text."""

    blocks: list[tuple[Path, bool]] = []
    for page in Path(config.site_dir).rglob("*.html"):
        parser = _PklBlockAudit()
        parser.feed(page.read_text(encoding="utf-8"))
        blocks.extend((page, highlighted) for highlighted in parser.blocks)

    if not blocks:
        raise RuntimeError("documentation build contains no language-pkl blocks")

    unhighlighted = sorted(
        {str(page) for page, highlighted in blocks if not highlighted}
    )
    if unhighlighted:
        raise RuntimeError(
            "Pkl blocks rendered without syntax tokens: " + ", ".join(unhighlighted)
        )

    logging.getLogger("mkdocs").info(
        "Verified syntax highlighting for %d Pkl blocks", len(blocks)
    )
