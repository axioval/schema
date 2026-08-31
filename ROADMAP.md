# Roadmap

Axioval aims to make validation requirements portable without making packages
executable or privileging one vendor, model format, or repository owner.

This roadmap describes intent, not a compatibility guarantee. Milestone contents
may move as conformance tests expose missing foundations.

## Now: trustworthy authoring substrate (`0.1.x`)

- [x] Typed Pkl authoring modules and deterministic normalized JSON.
- [x] Static-first manifest inspection and repository-confined evaluation.
- [x] Fail-closed package, definition, parameter, selector, and snapshot binding.
- [x] Reusable object/property vocabulary with external-schema names.
- [x] Optional exact property-container qualification.
- [x] Rich public documentation and a complete vocabulary-to-instance tutorial.
- [ ] Publish immutable `v0.1.0` after external consumer review.

## Next: portable capability governance (`0.2.x`)

- Define a capability registry with stable semantic contracts and conformance
  vectors, not engine implementations.
- Specify deterministic diagnostic/result interchange.
- Add unit/quantity system identifiers and conversion contracts.
- Define conflict, missing, unsupported, and invalid fact states explicitly.
- Add package dependency identities, checksums, and lock data.
- Publish migration tooling for normalized schema changes.

## Then: ecosystem and registry (`0.3.x`)

- Launch `axioval/registry` submission and discovery workflows.
- Validate immutable repository revisions in isolated workers.
- Publish signed validation attestations and normalized artifact hashes.
- Index applications' declared capability support.
- Add package compatibility matrices without ownership-based trust.
- Support external vocabulary packages shared by many rulesets.

## Stable contract (`1.0.0`)

A `1.0.0` release requires:

- documented schema-version negotiation and migration rules;
- multiple independent package authors and checking-engine consumers;
- a public conformance suite with fail-closed negative vectors;
- stable capability and diagnostic semantics;
- reproducible package validation; and
- an explicit deprecation and security-response policy.

## Open design questions

- How should canonical concepts reference bSDD, IDS, and non-IFC vocabularies
  without making one service mandatory?
- Which duplicate-property cases are conflicts versus precedence policies?
- How should type-level versus occurrence-level property sources be represented?
- Which template-composition features lower cleanly to declarative normalized
  data without becoming a hidden programming language?
- How should localized diagnostics and remediation guidance be standardized?

## Non-goals

- Shipping package-provided executable checking logic.
- Owning IFC parsing, geometry kernels, or application runtime IRs.
- Treating folders or property sets as universal semantic hierarchies.
- Giving Axioval-owned repositories special registry trust.
- Claiming a documentation example is a normative DIN or IFC compliance rule.
