# Axioval schema

This repository owns the vendor-neutral authoring schema and normalized interchange contract used by Axioval-compatible validation applications.

## Boundaries

- `schema/` contains reusable object/property vocabularies, typed Pkl contracts, selectors, definitions, rulesets, and the static registry manifest schema.
- `docs/` is the MkDocs Material source; root community files are included into the site rather than duplicated.
- `examples/` is the only place in this repository where concrete rule instances may appear.
- `tests/` verifies successful evaluation, rejection of invalid input, and deterministic JSON output.
- Do not add production rulesets here. Official and community rulesets live in separate repositories and have the same trust level.
- Do not add IFC import or geometry implementations. Those belong to `openbimrs/ifc` and `axiolid/axiolid-kernel`; this repository describes validation data only.

## Contract

Pkl is the authoring frontend. Evaluation produces candidate JSON; `scripts/validate.py` resolves definition packages and performs fail-closed parameter/selector binding before the result is considered portable normalized data. Authoring functions and templates must lower to declarative data; applications must never depend on executing package-specific logic during model checking.

## Validation

Run `./scripts/check.sh` for schema, binder, and snapshot validation. The repository pins Pkl in `.pkl-version` and CI uses the same version.

Run `npx --yes markdownlint-cli2@0.18.1` and `uvx --from 'mkdocs==1.6.1' --with 'mkdocs-material==9.6.20' --with 'Pygments==2.19.2' mkdocs build --strict` for documentation. GitHub Pages deploys only the linted, strict build from `main`; the build hook verifies that every Pkl fence contains syntax tokens.
