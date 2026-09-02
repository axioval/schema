# IFC geometry clearance example

This example demonstrates the authoring boundary:

- `openbim.ifc` owns exact IFC4X3 entity names and release identity;
- `openbim.geometry` owns the closed directional-clearance capability ID;
- MCS owns the rule definition, applicability, parameters, and normalized output.

The package does **not** claim that selecting walls and pipe segments defines a
particular geometric algorithm. Implementations must satisfy the geometry
capability contract and report their own scoped conformance.
