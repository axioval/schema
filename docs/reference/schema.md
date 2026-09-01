# Schema surface

This is the precise reference for people connecting software to Axioval. If you
only want to understand or prepare a check, start with the
[four building blocks](../guide/building-blocks.md) instead.

The Pkl modules define what authors may write. The Python binder is the final
safety gate before checked information becomes normalized JSON. All examples are
folded by default so you can scan the concepts first.

## Modules

| Module | Owns |
| --- | --- |
| `Types.pkl` | identifiers, semantic versions, localized text, package metadata |
| `Citations.pkl` | bibliographic sources, locators, citations, parameter targets |
| `Values.pkl` | tagged scalar/list values plus object/property references |
| `Selectors.pkl` | object type, property, classification, boolean-composition selectors |
| `Definitions.pkl` | vocabularies and reusable capability templates |
| `RuleSets.pkl` | concrete rule instances and cosmetic folders |

## Package metadata and citations

`PackageMetadata.name` and `description` use `LocalizedText`; package authors no
longer combine languages in one string. Each definition or ruleset document owns
a `sources` catalog. A source records a kind, formal designation, localized
title, and optional publisher, edition, ISO publication date, and HTTPS URL.

A `Citation` points to one source and may add ordered locators such as part,
clause, paragraph, table, figure, or page. Definition components, rules, and
requirements can carry citations. `parameterCitations` applies one citation to
explicit parameters that are actually bound by that rule. Unknown source IDs,
unsafe URLs, invalid dates, duplicate citation IDs or locators, and unknown
parameter targets fail closed.

Citations are provenance metadata only. They do not change applicability,
evidence, evaluation, verdicts, legal force, or compliance claims.

## Definition package

A normalized definition document has these top-level fields:

??? example "Show the normalized document shape"
    ```json
    {
      "schemaVersion": "0.1.0",
      "package": {},
      "sources": {},
      "objectTypes": {},
      "properties": {},
      "propertySets": {},
      "definitions": {}
    }
    ```

At least one reusable component must be present. Map keys must equal component
IDs. Duplicate component IDs across loaded packages are rejected.

### `ObjectTypeDefinition`

Maps one stable Axioval object-type ID to external-schema names such as
`IfcWall`. Object-type references can specify whether subtypes are accepted.

### `PropertyDefinition`

Maps one stable property ID to external names and one `valueKind`. Quantity
properties also require a qualified `unitDimension`. The property is independent
of any container.

### `PropertySetDefinition`

Maps one stable qualifier ID to external container names. It contains no member
list and establishes no ownership relation.

### `RuleDefinition`

Declares a capability and typed parameter map. `referencedValueKind` is valid
only on a `propertyReference` parameter and constrains the referenced property's
catalogued type.

## Reference values

=== "Object type"

    ??? example "Show JSON"
        ```json
        {
          "type": "objectTypeReference",
          "objectType": "axioval:example.ifc.wall",
          "includeSubtypes": true
        }
        ```

=== "Property, loose"

    ??? example "Show JSON"
        ```json
        {
          "type": "propertyReference",
          "property": "axioval:example.ifc.is-external"
        }
        ```

=== "Property, strict"

    ??? example "Show JSON"
        ```json
        {
          "type": "propertyReference",
          "property": "axioval:example.ifc.load-bearing",
          "propertySet": "axioval:example.ifc.pset-wall-common"
        }
        ```

## Selectors

Selectors are declarative and recursively validated:

- `all`
- `entityType` using a canonical object-type ID
- `property` using a canonical property ID and optional set qualifier
- `classification`
- `allOf`, `anyOf`, and `not`

A comparison value on a property selector must match the referenced property's
catalogued `valueKind`. `exists` rejects a comparison value; every other
operator requires one.

## Rich applicability

A rule that involves several populations uses an `Applicability` object. Its
`groups` map gives every population a stable local ID, localized name, optional
description, and recursively validated selector. Requirements and trusted host
adapters can target these groups by ID.

For example, an opening-coordination rule can name separate groups for
penetrated elements, penetrating elements, and openings without pretending they
are one flat selection. Group-map keys must equal group IDs. Empty group maps,
unknown concepts, and malformed selectors are rejected.

Legacy rules may still provide one selector directly. Requirements need rich
applicability because a flat selector has no targetable group IDs.

## Requirements

A `Requirement` records a stable ID, localized statement, optional description,
and one or more `targetGroups`. Every referenced group must exist in the same
rule. Requirement IDs and group references must be unique.

Requirements explain the expected state. They do not execute package code or
replace the `RuleDefinition.capability` contract used by a trusted application.

## Explanatory images

A rule can carry `ExplanatoryImage` entries with localized alternative text and
an optional localized caption. Images are package-contained assets referenced by
a normalized relative path and declared media type. PNG, JPEG, WebP, and SVG are
supported.

Normalization rejects absolute paths, traversal, backslashes, extension and
media-type mismatches, duplicate image IDs, missing files, symlink escapes,
active SVG content, external SVG references, and raster signature mismatches.
Images are explanatory only and never change applicability or execution.

## Folders are cosmetic

`RuleFolder` exists for presentation and organization. Its position does not
change selector scope, rule identity, execution semantics, or trust. Consumers
may render alternative views without rewriting the rules.

## Compatibility status

The current schema version is `0.1.0` and pre-stable. See the
[roadmap](../community/roadmap.md) for the planned compatibility policy and the
[changelog](../community/changelog.md) for contract changes.
