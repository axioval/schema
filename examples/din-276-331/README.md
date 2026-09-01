# DIN 276 KG 331 example

This **non-normative instructional fixture** demonstrates the complete Axioval
journey: canonical property vocabulary, a typed reusable rule definition, and
concrete rule instances.

The project profile selects objects classified as DIN 276:2018-12 cost group
331 and then applies these project-defined IFC checks:

- map the selected objects to `IfcWall` (subtypes accepted);
- expect `LoadBearing = true`, strictly in `Pset_WallCommon`; and
- expect `IsExternal = true`, regardless of the property's container.

DIN supplies the cited cost-group identifier. The IFC mappings and expected
property values are instructional project choices, not assertions that DIN 276
mandates those IFC representations.

See the [worked tutorial](../../docs/tutorials/din-276-331.md) for the rationale,
source links, and normalized output.
