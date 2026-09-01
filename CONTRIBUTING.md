# Contributing to Axioval MCS

Thank you for improving the vendor-neutral authoring and interchange contract.
Contract changes affect package authors, registries, and checking applications,
so contributions need executable evidence, not only prose.

## Before opening a change

1. Search existing issues and the [roadmap](https://github.com/axioval/mcs/blob/main/ROADMAP.md).
2. Explain which layer changes: vocabulary, template, instance, manifest,
   normalization, or application capability.
3. State compatibility and security implications.
4. For domain claims, link an authoritative public source where possible and
   distinguish normative requirements from examples.

## Repository boundaries

- `schema/` owns reusable Pkl contracts.
- `scripts/` owns static inspection and fail-closed semantic binding.
- `examples/` is the **only** location for concrete rule instances.
- Production rulesets live in separate repositories.
- IFC parsing, geometry, and checking algorithms do not belong here.
- Axioval-owned packages receive no registry or trust privilege.

## Development setup

Requirements:

- Pkl `0.32.1` (pinned in `.pkl-version`);
- Python 3.11 or newer; and
- [`uv`](https://docs.astral.sh/uv/) for ephemeral tooling.

Run the schema gate:

??? example "Show source or commands"
    ```bash
    PATH="$HOME/.local/bin:$PATH" ./scripts/check.sh
    ```

Build and lint the documentation exactly as CI does:

??? example "Show source or commands"
    ```bash
    npx --yes markdownlint-cli2@0.18.1
    python -m pip install --disable-pip-version-check -r requirements-docs.txt
    mkdocs build --strict
    ```

Lint and format Python changes:

??? example "Show source or commands"
    ```bash
    uvx ruff format scripts tests
    uvx ruff check scripts tests
    ```

## Contract-change checklist

Every meaningful schema change should include:

- a valid Pkl example or fixture;
- regenerated deterministic JSON snapshots;
- at least one negative test proving the old invalid state fails closed;
- synchronized Pkl and Python binder acceptance;
- documentation of author and consumer behavior;
- an `Unreleased` changelog entry; and
- a clean strict docs build and `git diff --check`.

!!! note
    If a structural Pkl field is optional, the normalized binder must accept the
    same optionality. If the binder requires a semantic relation Pkl cannot prove
    locally, add deterministic cross-document binding and a rejection test.

## Property and object modeling

Prefer stable canonical concepts plus explicit external bindings.

- Do not make a property set own a property.
- Use an optional property-set qualifier only when exact placement is normative.
- Keep presentation folders cosmetic.
- Put expected facts in a rule assertion, not in applicability when doing so
  would hide violating objects.

## Documentation style

The Pages site is built from `docs/` with MkDocs Material. Use:

- short task-oriented pages;
- plain language on the homepage and first-time reader journey;
- local accessible SVG diagrams with readable mobile variants;
- collapsed source panels in step-by-step tutorials;
- no en or em dashes in repository Markdown;
- callouts for trust boundaries and normative caveats;
- complete checked examples rather than pseudo-APIs;
- links to authoritative specifications for domain claims; and
- diagrams only when they clarify data flow or ownership.

Root `CONTRIBUTING.md`, `CHANGELOG.md`, `ROADMAP.md`, and `LICENSE` are included
into the site so GitHub and Pages share one source of truth.

## Pull requests

Keep changes reviewable and atomic. Describe:

- the behavior before and after;
- the failure mode being prevented;
- commands run and their real results; and
- migration or rollback considerations.

By contributing, you agree that your contribution is licensed under
[AGPL-3.0-or-later](https://github.com/axioval/mcs/blob/main/LICENSE).
