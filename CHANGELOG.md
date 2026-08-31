# Changelog

All notable changes to Axioval Schema are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
package/schema compatibility follows [Semantic Versioning](https://semver.org/)
once a release is tagged. The current `0.1.0` contract is pre-stable.

## [Unreleased]

### Added

- MkDocs Material documentation site and GitHub Pages deployment.
- Reusable `ObjectTypeDefinition`, `PropertyDefinition`, and independent
  `PropertySetDefinition` vocabulary components.
- Canonical `ObjectTypeReferenceValue` and `PropertyReferenceValue` variants.
- Optional exact property-set qualification without property ownership.
- `referencedValueKind` constraints for typed property-reference parameters.
- Full DIN 276 KG 331 instructional fixture covering object type, strict
  `LoadBearing`, and container-agnostic `IsExternal` requirements.
- Negative tests for unknown concepts and property-kind mismatches.
- Contributor guide, roadmap, AGPL license, and GitHub Sponsors configuration.

### Changed

- Entity-type selectors now reference reusable object-type concepts instead of
  repeating raw external type-system/name pairs.
- The minimal property example uses one canonical property reference rather than
  treating `propertySet` and `property` as peer string parameters.
- Definition-package normalized output now includes object, property, and
  property-set catalogs.

### Fixed

- Apple Pkl code fences now use a dedicated server-side lexer and fail the docs
  build if they regress to unhighlighted plain text.
- Definition-default validation no longer shadows the active ruleset document
  while binding.

### Security

- Normalization rejects unknown object/property/property-set IDs, mismatched
  referenced property kinds, and unresolved strict container qualifiers.

## [0.1.0] - 2026-08-31

### Added

- Initial Pkl authoring modules for types, values, selectors, definitions, and
  rule sets.
- Static `axioval.json` registry manifest contract.
- Repository-confined Pkl evaluation and deterministic normalized snapshots.
- Fail-closed cross-document package, definition, selector, and parameter binder.
- Minimal non-production package and CI validation workflow.

[Unreleased]: https://github.com/axioval/schema/compare/49a2d765fe9a6a5b2f9cbf650500c30b9d6068d3...HEAD
[0.1.0]: https://github.com/axioval/schema/commit/49a2d765fe9a6a5b2f9cbf650500c30b9d6068d3
