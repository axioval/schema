# Property addressing without folder semantics

Property sets are real relationship objects in IFC, but treating their names as
the universal identity of a property causes the same problem as mandatory file
folders: one hierarchy must answer several unrelated organizational questions.
Axioval therefore separates **property identity** from **container qualification**.

## Canonical property identity

A vocabulary defines the property once:

```pkl
["axioval:example.ifc.load-bearing"] = new Definitions.PropertyDefinition {
  id = "axioval:example.ifc.load-bearing"
  name = new Types.LocalizedText { default = "Load bearing" }
  valueKind = "boolean"
  externalNames {
    new Definitions.ExternalName {
      typeSystem = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3"
      name = "LoadBearing"
    }
  }
}
```

The definition is not nested in a property set. Its stable ID can be reused by
selectors, templates, and instances.

## Loose reference: property matters, container does not

```pkl
new Values.PropertyReferenceValue {
  property = "axioval:example.ifc.is-external"
}
```

An adapter resolves the external name and traverses the model's native
relationships. The property may be found in any supported container.

Implementations must define deterministic conflict behavior. If the same
canonical property resolves more than once with incompatible values, they should
return a conflict—not choose one silently.

## Strict reference: membership is part of the requirement

```pkl
new Values.PropertyReferenceValue {
  property = "axioval:example.ifc.load-bearing"
  propertySet = "axioval:example.ifc.pset-wall-common"
}
```

Now both facts are normative:

1. the property is `LoadBearing`; and
2. it is related through the external container mapped from
   `Pset_WallCommon`.

A matching property in another set is not sufficient.

=== "Use a loose reference when"

    - the requirement is about semantic information, not authoring layout;
    - exporters legitimately place equivalent properties in different sets; or
    - a project mapping layer already canonicalizes sources.

=== "Use a strict reference when"

    - delivery requirements mandate a standard property set;
    - interoperability depends on exact container placement; or
    - the check is specifically auditing schema conformance.

## Container-agnostic resolution is still fail-closed

When `propertySet` is omitted, an adapter must:

1. map the canonical property concept into the active model schema;
2. collect occurrences across supported property containers;
3. report missing when no occurrence exists;
4. converge type-correct occurrences only when their semantic values agree; and
5. report conflicting or invalid when values disagree or cannot be typed.

It must never accept the first same-named property it happens to encounter.

## IFC relationship context

In IFC, an object is related to property definitions through
[`IfcRelDefinesByProperties`](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcRelDefinesByProperties.htm),
and a property set groups named properties. Axioval does not erase that
relationship. It lets each requirement decide whether the **container identity**
is significant.

The official IFC 4.3.2
[`Pset_WallCommon`](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/Pset_WallCommon.htm)
documentation lists both `LoadBearing` and `IsExternal` as boolean single-value
properties. That makes it a useful demonstration, not a reason to hard-code
property-set ownership into the generic schema.
