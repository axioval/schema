# When property location matters

The same fact can appear in different places in a building model. Sometimes a
requirement only cares about the fact. Sometimes it also requires one exact
place. Axioval supports both choices.

Think of it like asking for a book:

- **Any shelf is fine:** find this book wherever the library stores it.
- **One shelf is required:** find this book in the reference section.

In technical terms, Axioval separates **property identity** from **container
qualification**. Property sets are real relationship objects in IFC, but their
names do not need to become the universal identity of a property.

## Canonical property identity

A vocabulary defines the property once:

??? example "Show the property definition"
    ```pkl
    ["axioval:example.ifc.load-bearing"] = new Definitions.PropertyDefinition {
      id = "axioval:example.ifc.load-bearing"
      name = new Types.LocalizedText { default = "Load bearing" }
      valueKind = "boolean"
      externalNames {
        new Definitions.ExternalName {
          typeSystem = "https://github.com/axioval/mcs/tree/main/examples"
          name = "axioval:example.ifc.load-bearing"
        }
      }
    }
    ```

The definition is not nested in a property set. Its stable ID can be reused by
selectors, templates, and instances. Its `ExternalName` belongs to the example
vocabulary, so the definition remains project-local: `openbim.ifc` `0.2.0`
intentionally bundles no verified PSD/QTO occurrences, and MCS does not attach
an IFC external name from a free-form string.

## Loose reference: property matters, container does not

??? example "Show the loose reference"
    ```pkl
    new Values.PropertyReferenceValue {
      property = "axioval:example.ifc.is-external"
    }
    ```

A model-specific consumer resolves the project-local concept and traverses the
model's native relationships. The property may be found in any supported
container.

Implementations must define deterministic conflict behavior. If the same
canonical property resolves more than once with incompatible values, they should
return a conflict. They must not choose one silently.

## Strict reference: membership is part of the requirement

??? example "Show the strict reference"
    ```pkl
    new Values.PropertyReferenceValue {
      property = "axioval:example.ifc.load-bearing"
      propertySet = "axioval:example.ifc.pset-wall-common"
    }
    ```

Now both local vocabulary facts are normative:

1. the property concept is `axioval:example.ifc.load-bearing`; and
2. it is related through the local container concept
   `axioval:example.ifc.pset-wall-common`.

A matching property in another set is not sufficient.

=== "Use a loose reference when"

    - the requirement is about semantic information, not authoring layout;
    - exporters legitimately place equivalent properties in different sets; or
    - a project mapping layer already canonicalizes sources.

=== "Use a strict reference when"

    - project vocabulary mandates one exact property container;
    - interoperability depends on exact container placement; or
    - the check is specifically auditing schema conformance.

## Container-agnostic resolution is still fail-closed

When `propertySet` is omitted, an adapter must:

1. resolve the project-local property concept for the active model adapter;
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
properties. That supports the example's source citation, but it is not a typed
package occurrence and does not authorize MCS to manufacture an IFC external
identity. The package-owned template catalog must supply that binding in a
future release.
