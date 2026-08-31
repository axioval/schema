# DIN 276 KG 331 example

This **non-normative instructional fixture** demonstrates the complete Axioval
journey: canonical property vocabulary, a typed reusable rule definition, and
concrete rule instances.

It selects objects classified as DIN 276:2018-12 cost group 331 and requires:

- object type `IfcWall` (subtypes accepted);
- `LoadBearing = true`, strictly in `Pset_WallCommon`; and
- `IsExternal = true`, regardless of the property's container.

See the [worked tutorial](../../docs/tutorials/din-276-331.md) for the rationale,
source links, and normalized output.
