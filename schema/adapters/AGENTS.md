# Pkl adapters

Authoring-only lowering from specialized package contracts into MCS's stable,
declarative normalized representation.

- `Ifc.pkl` accepts `openbim.ifc` version-bound references and emits MCS
  `ExternalName` values. It does not define IFC names or releases.
- `Geometry.pkl` accepts only the closed `openbim.geometry` capability union and
  preserves the package-owned qualified ID.

Adapters must not copy domain catalogs, add runtime checking behavior, or hide
version/exactness information required by the source package.
