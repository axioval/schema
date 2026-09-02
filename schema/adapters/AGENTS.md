# Pkl adapters

Authoring-only lowering from specialized package contracts into MCS's stable,
declarative normalized representation.

- `Ifc.pkl` accepts `openbim.ifc` version-bound entity references and emits MCS
  `ExternalName` values using the release's semantic type-system identity. It
  does not define IFC names, releases, or manufacture PSD/QTO references while
  the source package marks that catalog `not-bundled`.
- `Geometry.pkl` accepts only the closed `openbim.geometry` capability union and
  preserves the package-owned qualified ID.

Adapters must not copy domain catalogs, add runtime checking behavior, or hide
version/exactness information required by the source package.
