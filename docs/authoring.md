# Author a package

A ruleset package lives in its own repository. The schema repository contains
concrete instances only as examples.

## 1. Create the package boundary

```text
my-rules/
├── axioval.json
├── PklProject
├── definitions.pkl
├── ruleset.pkl
└── expected/
    ├── definitions.json
    └── ruleset.json
```

Pin the supported Pkl version and keep every manifest-selected module inside the
repository root.

## 2. Choose stable IDs

Use qualified IDs for package, vocabulary, template, and capability identity.
Do not encode mutable labels or folder paths into IDs.

```text
https://example.org/axioval/property/fire-rating
https://example.org/axioval/rule/property-exists
```

Local folder and rule IDs use the smaller repository-local identifier syntax.

## 3. Define vocabulary before policy

Declare reusable object types, properties, and property-set qualifiers in a
module that amends `schema/Definitions.pkl`. Properties and sets are independent
catalogs; do not recreate a mandatory hierarchy.

## 4. Reuse or define a capability template

A `RuleDefinition` is valid only when checking applications know its capability.
Adding a new capability ID to a package does not make applications execute it.
Coordinate portable capability semantics separately and fail closed when an
application does not support them.

## 5. Create instances

A ruleset module amends `schema/RuleSets.pkl`, declares every definition package,
and creates typed instances. Applicability selects the objects that must be
checked; do not put the expected result into applicability when that would hide
violations.

!!! example "Scope versus assertion"
    To require every `DIN 276 / 331` object to be an `IfcWall`, select by the
    classification and assert the object type in the rule. Selecting only walls
    would silently exclude incorrectly typed objects.

## 6. Declare the static manifest

```json
{
  "$schema": "schema/registry-manifest.schema.json",
  "manifestVersion": "0.1.0",
  "kind": "ruleset",
  "id": "https://example.org/axioval/my-rules",
  "version": "0.1.0",
  "schemaVersion": "0.1.0",
  "entrypoint": "ruleset.pkl",
  "definitionEntrypoints": ["definitions.pkl"]
}
```

Registry implementations inspect this file completely before invoking Pkl.
Absolute paths, traversal, non-Pkl entrypoints, unknown fields, and missing
definition modules are rejected.

## 7. Validate and version

Run the same gate locally and in CI:

```bash
PATH="$HOME/.local/bin:$PATH" ./scripts/check.sh
```

Commit Pkl source, manifest, and deterministic normalized snapshots together.
Use semantic package versions and explain compatibility changes in a changelog.

## Publication checklist

- [ ] no secrets or host-specific absolute paths;
- [ ] explicit package license and provenance;
- [ ] all capabilities documented and supported by target applications;
- [ ] strict property-set qualifiers used only when semantically intended;
- [ ] negative tests prove malformed references and wrong value kinds fail;
- [ ] normalized snapshots were generated from the committed source;
- [ ] registry submission points to an immutable revision or release.
