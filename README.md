# Axioval Schema

Axioval Schema is the vendor-neutral contract for authoring and exchanging validation rule packages.

- **Pkl source** provides types, constraints, modules, defaults, and reusable authoring functions.
- **Validated normalized JSON** is the portable application boundary; raw Pkl evaluation output is only a candidate until definition binding succeeds.
- **Rule packages** remain in independently hosted repositories discovered by [axioval/registry](https://github.com/axioval/registry).
- Official Axioval packages use exactly the same contract and receive no extra runtime privileges.

This repository deliberately contains no production rulesets. Concrete rule instances appear only in [`examples/`](examples/).

## Repository layout

```text
schema/       Pkl terminology, package schemas, and registry manifest schema
examples/     non-production examples
docs/         package and compatibility contracts
scripts/      deterministic validation entry points
tests/        contract tests
```

## Authoring model

The schema separates:

- **Terminology (TBox-like):** rule definitions, parameter declarations, selectors, and value types.
- **Instantiation (ABox-like):** concrete rule instances arranged into a ruleset package.

This is a structural schema distinction, not an OWL reasoner. Runtime rule behavior must lower to a closed application IR; Pkl methods are authoring-time generators and are not executable checker extensions.

## Evaluate the example

Requires the Pkl version in [`.pkl-version`](.pkl-version).

```bash
pkl eval -f json examples/minimal/ruleset.pkl
```

Run all repository checks:

```bash
./scripts/check.sh
```

## Package repository contract

Required:

```text
axioval.json          static registry manifest
PklProject            pinned Pkl project/dependencies
<entrypoint>.pkl      manifest-selected ruleset module
<definition>.pkl      one or more manifest-selected definition modules
```

Recommended: `README.md` and a package-chosen `LICENSE`. See [`docs/package-contract.md`](docs/package-contract.md) for the complete contract.

The registry can inspect `axioval.json` without evaluating untrusted Pkl. It then evaluates every declared definition entrypoint and the ruleset entrypoint in a sandbox. The binder rejects undeclared or duplicate definition packages, unresolved definition IDs, missing or unknown parameters, incompatible value variants/defaults, and values outside declared allowed sets. Only fully bound normalized JSON crosses the portable boundary; applications still validate it against their own typed IR.

## Status

Initial schema scaffold. Schema evolution and compatibility policy are not stable until the first tagged release.
