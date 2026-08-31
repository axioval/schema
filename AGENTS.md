# Axioval schema

This repository owns the vendor-neutral authoring schema and normalized interchange contract used by Axioval-compatible validation applications.

## Boundaries

- `schema/` contains Pkl types, constraints, abstract package modules, and the static registry manifest schema.
- `examples/` is the only place in this repository where concrete rule instances may appear.
- `tests/` verifies successful evaluation, rejection of invalid input, and deterministic JSON output.
- Do not add production rulesets here. Official and community rulesets live in separate repositories and have the same trust level.
- Do not add IFC import or geometry implementations. Those belong to `openbimrs/ifc` and `axiolid/axiolid-kernel`; this repository describes validation data only.

## Contract

Pkl is the authoring frontend. Evaluation produces candidate JSON; `scripts/validate.py` resolves definition packages and performs fail-closed parameter/selector binding before the result is considered portable normalized data. Authoring functions and templates must lower to declarative data; applications must never depend on executing package-specific logic during model checking.

## Validation

Run `./scripts/check.sh`. The repository pins Pkl in `.pkl-version` and CI uses the same version.
