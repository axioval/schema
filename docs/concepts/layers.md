# Mental model

Axioval separates reusable meaning from concrete validation policy. Mixing these
layers creates packages that cannot be shared safely.

## 1. Vocabulary

A definition package can declare three independent concept catalogs:

| Concept | Purpose | Example |
| --- | --- | --- |
| `ObjectTypeDefinition` | Reusable model-object type | IFC `IfcWall` |
| `PropertyDefinition` | Reusable property identity and value kind | boolean `LoadBearing` |
| `PropertySetDefinition` | Optional external container qualifier | `Pset_WallCommon` |

Each concept has a stable qualified ID and one or more `ExternalName` bindings.
The stable ID is what rules reference; adapters map it to each supported model
schema.

!!! important
    `PropertySetDefinition` does **not** list or own properties. A property may
    appear in multiple external containers. Container membership becomes
    normative only when a selector or `PropertyReferenceValue` names a set.

## 2. Template

A `RuleDefinition` declares:

- a stable definition ID;
- a stable `capability` that applications explicitly implement; and
- typed parameter definitions.

```pkl
["axioval:example.boolean-property-equals"] = new Definitions.RuleDefinition {
  id = "axioval:example.boolean-property-equals"
  capability = "axioval:capability.property-value-equals"
  name = new Types.LocalizedText { default = "Boolean property equals" }
  parameters {
    ["property"] = new Definitions.ParameterDefinition {
      id = "property"
      name = new Types.LocalizedText { default = "Property" }
      kind = "propertyReference"
      referencedValueKind = "boolean"
    }
    ["expected"] = new Definitions.ParameterDefinition {
      id = "expected"
      name = new Types.LocalizedText { default = "Expected" }
      kind = "boolean"
    }
  }
}
```

`referencedValueKind` closes a subtle type hole: this boolean template cannot be
bound to a string property.

## 3. Instance

A `RuleInstance` binds a known definition to concrete values and an applicability
selector. Instances are policy—the ABox-like layer—and belong in external
ruleset repositories. This schema repository contains them only under
`examples/`.

## 4. Package and normalization

`axioval.json` statically identifies the package and every definition entrypoint.
Only after all entrypoints are repository-confined and all candidate JSON is
semantically bound does the output become normalized interchange.

```mermaid
sequenceDiagram
  participant R as Registry
  participant M as Manifest validator
  participant P as Pkl sandbox
  participant B as Contract binder
  R->>M: inspect axioval.json
  M->>M: resolve every local entrypoint
  M->>P: evaluate constrained modules
  P-->>B: candidate JSON
  B->>B: bind packages, concepts, templates, values, selectors
  B-->>R: validated normalized JSON or refusal
```

## What Axioval deliberately does not own

- model parsing and IFC relationship traversal;
- geometric algorithms;
- executable rule logic supplied by packages;
- an application's canonical runtime IR;
- registry trust based on repository ownership.
