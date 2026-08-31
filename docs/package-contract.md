# Ruleset repository contract

A repository submitted to the Axioval registry represents a package, not a privileged publication channel. Repositories owned by `axioval` follow this exact contract and receive no extra capabilities.

## Required files

```text
axioval.json     # static discovery manifest
PklProject       # pinned Pkl project boundary
<entry>.pkl      # ruleset module named by axioval.json
<definition>.pkl # one or more definition modules named by axioval.json
```

The manifest MUST validate against `schema/registry-manifest.schema.json`. Its entrypoints are repository-relative paths: absolute paths and `..` traversal are forbidden.

## Evaluation contract

The ruleset entrypoint amends `schema/RuleSets.pkl` and evaluates to candidate JSON. Every `definitionEntrypoints` module amends `schema/Definitions.pkl`. Authoring functions and imports are evaluated away, then the binder MUST resolve every declared definition package and definition ID and validate required/unknown parameters, value variants, defaults, allowed values, selectors, and duplicate identities. Raw evaluator output is not normalized interchange data until this binding succeeds.

Applications MUST fail closed when a declaration is missing, conflicting, malformed, or unsupported. They MUST also validate fully bound normalized data against their own typed IR.

## Source and compiled forms

Pkl source is authoritative for editing. A registry may cache evaluated JSON, but generated output is not accepted as proof that source is safe or valid. Evaluation of untrusted repositories requires network restrictions, package checksum verification, and CPU/memory/output limits.

## Licensing and provenance

Package authors choose their own license and repository host. Registry listing does not transfer ownership or imply endorsement. Axioval-owned packages are ordinary packages validated through the same pipeline.
