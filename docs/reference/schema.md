# Schema surface

The Pkl modules are the typed authoring API. The Python binder defines the
fail-closed semantic acceptance boundary for normalized JSON.

## Modules

| Module | Owns |
| --- | --- |
| `Types.pkl` | identifiers, semantic versions, localized text, package metadata |
| `Values.pkl` | tagged scalar/list values plus object/property references |
| `Selectors.pkl` | object type, property, classification, boolean-composition selectors |
| `Definitions.pkl` | vocabularies and reusable capability templates |
| `RuleSets.pkl` | concrete rule instances and cosmetic folders |

## Definition package

A normalized definition document has these top-level fields:

```json
{
  "schemaVersion": "0.1.0",
  "package": {},
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

    ```json
    {
      "type": "objectTypeReference",
      "objectType": "axioval:example.ifc.wall",
      "includeSubtypes": true
    }
    ```

=== "Property, loose"

    ```json
    {
      "type": "propertyReference",
      "property": "axioval:example.ifc.is-external"
    }
    ```

=== "Property, strict"

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

## Folders are cosmetic

`RuleFolder` exists for presentation and organization. Its position does not
change selector scope, rule identity, execution semantics, or trust. Consumers
may render alternative views without rewriting the rules.

## Compatibility status

The current schema version is `0.1.0` and pre-stable. See the
[roadmap](../community/roadmap.md) for the planned compatibility policy and the
[changelog](../community/changelog.md) for contract changes.
