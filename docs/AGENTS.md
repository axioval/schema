# Documentation

This directory is the source for the public MkDocs Material site configured by
`../mkdocs.yml` and deployed through `../.github/workflows/pages.yml`.

## Conventions

- Explain the dictionary, recipe, filled card, and bundle journey before technical details.
- Keep the homepage free of programmer jargon and route tool builders to a separate reference path.
- Keep all reader-facing source blocks collapsed by default with `??? example` panels.
- Add a `page.de.md` sibling for every public `page.md`; do not rely on English fallback.
- Translate navigation and reader prose, but preserve exact identifiers, source, machine formats, and URLs.
- Use repository-owned SVG diagrams with useful alt text and mobile variants when wide artwork becomes unreadable.
- Add a `.de.svg` sibling for every diagram that contains text.
- Keep SVGs script-free. `assets/javascripts/site.js` may inline only build-verified local diagrams so the site palette can style them.
- Keep navigation and section headings text-only. Reserve icons for labeled functional controls supplied by the Material theme.
- Do not use en or em dashes in repository Markdown; the strict MkDocs hook enforces this.
- Use checked repository examples; do not invent unsupported fields or capabilities.
- Treat property-set identity as an optional exact qualifier, never property ownership.
- Link public authoritative sources for IFC and standards claims; mark instructional examples as non-normative.
- Root `CONTRIBUTING.md`, `CHANGELOG.md`, `ROADMAP.md`, and `LICENSE` are included through `community/` proxies and remain the single source of truth.
- Run the strict build from the repository root after every documentation change.
