from __future__ import annotations

import hashlib
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts import mcs_archive

ROOT = Path(__file__).resolve().parents[1]


class MCSArchiveTests(unittest.TestCase):
    def pack(self, package: str = "minimal") -> tuple[Path, Path]:
        directory = Path(tempfile.mkdtemp())
        archive = directory / f"{package}.mcs"
        mcs_archive.pack(ROOT / "examples" / package, archive, ROOT)
        return directory, archive

    def rewrite(self, archive: Path, mutate) -> None:
        with zipfile.ZipFile(archive) as source:
            contents = [(i.filename, source.read(i)) for i in source.infolist()]
        contents = mutate(contents)
        with zipfile.ZipFile(archive, "w") as target:
            for name, data in contents:
                info = mcs_archive._zipinfo(
                    name,
                    zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED,
                )
                target.writestr(info, data)

    def add_declared_payload(
        self, items: list[tuple[str, bytes]], name: str, data: bytes, role: str
    ) -> list[tuple[str, bytes]]:
        metadata_index = next(
            i for i, item in enumerate(items) if item[0] == mcs_archive.METADATA
        )
        metadata = json.loads(items[metadata_index][1])
        metadata["inventory"].append(
            {
                "path": name,
                "role": role,
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
        metadata["inventory"].sort(key=lambda entry: entry["path"])
        items[metadata_index] = (
            mcs_archive.METADATA,
            mcs_archive._json_bytes(metadata),
        )
        return items + [(name, data)]

    def test_deterministic_round_trip_and_topology(self) -> None:
        directory, first = self.pack()
        second = directory / "again.mcs"
        mcs_archive.pack(ROOT / "examples/minimal", second, ROOT)
        self.assertEqual(
            hashlib.sha256(first.read_bytes()).digest(),
            hashlib.sha256(second.read_bytes()).digest(),
        )
        metadata = mcs_archive.verify(first)
        self.assertEqual(metadata["packageRoot"], "source/examples/minimal")
        names = {entry["path"] for entry in metadata["inventory"]}
        self.assertIn("source/schema/RuleSets.pkl", names)
        self.assertIn("source/examples/minimal/assets/wall-reference.svg", names)
        self.assertIn("source/LICENSE", names)
        self.assertEqual(metadata["formatVersion"], "0.1.0")
        self.assertNotIn("source/examples/din-276-331/ruleset.pkl", names)

    def test_mimetype_metadata_and_inventory(self) -> None:
        _, archive = self.pack()
        with zipfile.ZipFile(archive) as source:
            infos = source.infolist()
            self.assertEqual(infos[0].filename, "mimetype")
            self.assertEqual(infos[0].compress_type, zipfile.ZIP_STORED)
            self.assertEqual(source.read(infos[0]), mcs_archive.MIMETYPE)
            self.assertEqual(infos[1].filename, mcs_archive.METADATA)
        metadata = mcs_archive.inspect(archive)
        self.assertEqual(metadata["mediaType"], mcs_archive.MIMETYPE.decode())
        self.assertTrue(
            all(
                {"path", "role", "size", "sha256"} == set(x)
                for x in metadata["inventory"]
            )
        )

    def test_payload_and_coordinated_source_mutations_fail(self) -> None:
        _, archive = self.pack()

        def mutate(items):
            return [
                (name, data + b" " if name == "normalized/ruleset.json" else data)
                for name, data in items
            ]

        self.rewrite(archive, mutate)
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.verify(archive)
        _, archive = self.pack()

        def coordinated(items):
            changed = []
            for name, data in items:
                if (
                    name == "source/examples/minimal/ruleset.pkl"
                    or name == "normalized/ruleset.json"
                ):
                    data = data.replace(b"Example ruleset", b"Changed ruleset")
                changed.append((name, data))
            return changed

        self.rewrite(archive, coordinated)
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.verify(
                archive
            )  # inventory independently authenticates every byte

    def test_unlisted_missing_and_hash_tampering_fail(self) -> None:
        _, archive = self.pack()
        self.rewrite(archive, lambda items: items + [("extra.json", b"{}")])
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)
        _, archive = self.pack()
        self.rewrite(
            archive,
            lambda items: [x for x in items if x[0] != "normalized/ruleset.json"],
        )
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)
        _, archive = self.pack()

        def bad_hash(items):
            return [
                (
                    n,
                    d.replace(b'"sha256":"', b'"sha256":"0', 1)
                    if n == mcs_archive.METADATA
                    else d,
                )
                for n, d in items
            ]

        self.rewrite(archive, bad_hash)
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)

    def test_bad_names_collisions_modes_and_layout_fail(self) -> None:
        for bad in ("../x", "/x", "a\\b", "a\x01b", "A", "a"):
            _, archive = self.pack()
            self.rewrite(archive, lambda items, bad=bad: items + [(bad, b"x")])
            with self.assertRaises(mcs_archive.MCSError):
                mcs_archive.inspect(archive)
        _, archive = self.pack()
        self.rewrite(
            archive,
            lambda items: [
                ("not-mimetype" if n == "mimetype" else n, d) for n, d in items
            ],
        )
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)
        _, archive = self.pack()
        with zipfile.ZipFile(archive, "a") as source:
            info = mcs_archive._zipinfo("evil", zipfile.ZIP_DEFLATED)
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            source.writestr(info, b"target")
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)

    def test_metadata_duplicate_keys_and_identity_tampering_fail(self) -> None:
        _, archive = self.pack()
        self.rewrite(
            archive,
            lambda items: [
                (n, b'{"format":"x","format":"y"}' if n == mcs_archive.METADATA else d)
                for n, d in items
            ],
        )
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)
        _, archive = self.pack()

        def metadata_identity(items):
            result = []
            for name, data in items:
                if name == mcs_archive.METADATA:
                    value = json.loads(data)
                    value["package"]["id"] = "axioval:tampered"
                    data = json.dumps(
                        value, sort_keys=True, separators=(",", ":")
                    ).encode()
                result.append((name, data))
            return result

        self.rewrite(archive, metadata_identity)
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.verify(archive)

    def test_inspect_rejects_noncanonical_paths_and_roles(self) -> None:
        _, archive = self.pack()

        def noncanonical_path(items):
            result = []
            for name, data in items:
                if name == mcs_archive.METADATA:
                    value = json.loads(data)
                    for entry in value["inventory"]:
                        if entry["path"] == "source/schema/Types.pkl":
                            entry["path"] = "source//schema/Types.pkl"
                    data = json.dumps(
                        value, sort_keys=True, separators=(",", ":")
                    ).encode()
                elif name == "source/schema/Types.pkl":
                    name = "source//schema/Types.pkl"
                result.append((name, data))
            return result

        self.rewrite(archive, noncanonical_path)
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)
        _, archive = self.pack()

        def bad_role(items):
            result = []
            for name, data in items:
                if name == mcs_archive.METADATA:
                    value = json.loads(data)
                    for entry in value["inventory"]:
                        if entry["path"] == "source/schema/Types.pkl":
                            entry["role"] = "ruleset"
                    data = json.dumps(
                        value, sort_keys=True, separators=(",", ":")
                    ).encode()
                result.append((name, data))
            return result

        self.rewrite(archive, bad_role)
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)

    def test_inspect_rejects_noncanonical_zip_permissions(self) -> None:
        _, archive = self.pack()
        with zipfile.ZipFile(archive) as source:
            contents = [(i.filename, source.read(i)) for i in source.infolist()]
        with zipfile.ZipFile(archive, "w") as target:
            for name, data in contents:
                info = mcs_archive._zipinfo(
                    name,
                    zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED,
                )
                if name == "normalized/ruleset.json":
                    info.external_attr = (stat.S_IFREG | 0o755) << 16
                target.writestr(info, data)
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)

    def test_dependency_closure_rejects_unsupported_directives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = root / "entry.pkl"
            for source in (
                'import* "*.pkl"\n',
                'amends #"base.pkl"#\n',
                'value = read("secret.txt")\n',
                'local reader = read\nvalue = reader("secret.txt")\n',
            ):
                entry.write_text(source, encoding="utf-8")
                with self.assertRaises(mcs_archive.MCSError):
                    mcs_archive._pkl_closure(root, [entry])

    def test_dependency_closure_keeps_declared_package_imports_external(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = root / "entry.pkl"
            entry.write_text(
                'import "@ifc/versions/Ifc4x3.pkl" as ifc4x3\n', encoding="utf-8"
            )
            self.assertEqual(mcs_archive._pkl_closure(root, [entry]), {entry})

    def test_dependency_closure_rejects_package_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = root / "entry.pkl"
            entry.write_text('import "@ifc/../secret.pkl"\n', encoding="utf-8")
            with self.assertRaises(mcs_archive.MCSError):
                mcs_archive._pkl_closure(root, [entry])

    def test_dependency_closure_rejects_ancestor_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "real"
            real.mkdir()
            (real / "dep.pkl").write_text("value = 1\n", encoding="utf-8")
            (root / "linked").symlink_to(real, target_is_directory=True)
            entry = root / "entry.pkl"
            entry.write_text('import "linked/dep.pkl"\n', encoding="utf-8")
            with self.assertRaises(mcs_archive.MCSError):
                mcs_archive._pkl_closure(root, [entry])

    def test_verify_rejects_declared_but_unreferenced_source(self) -> None:
        _, archive = self.pack()
        self.rewrite(
            archive,
            lambda items: self.add_declared_payload(
                items, "source/examples/minimal/unused.pkl", b"value = 1\n", "source"
            ),
        )
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.verify(archive)

    def test_rejects_multidisk_central_member(self) -> None:
        _, archive = self.pack()
        raw = bytearray(archive.read_bytes())
        eocd = len(raw) - 22
        central_offset = int.from_bytes(raw[eocd + 16 : eocd + 20], "little")
        raw[central_offset + 34 : central_offset + 36] = b"\x01\x00"
        archive.write_bytes(raw)
        with self.assertRaises(mcs_archive.MCSError):
            mcs_archive.inspect(archive)

    def test_rejects_zip_preamble_and_trailing_bytes(self) -> None:
        for prefix, suffix in ((b"x", b""), (b"", b"x")):
            _, archive = self.pack()
            archive.write_bytes(prefix + archive.read_bytes() + suffix)
            with self.assertRaises(mcs_archive.MCSError):
                mcs_archive.inspect(archive)

    def test_rejects_zip_extra_fields_and_member_comments(self) -> None:
        for attribute, value in (("extra", b"\x01\x00\x00\x00"), ("comment", b"x")):
            _, archive = self.pack()
            with zipfile.ZipFile(archive) as source:
                contents = [(i.filename, source.read(i)) for i in source.infolist()]
            with zipfile.ZipFile(archive, "w") as target:
                for name, data in contents:
                    info = mcs_archive._zipinfo(
                        name,
                        zipfile.ZIP_STORED
                        if name == "mimetype"
                        else zipfile.ZIP_DEFLATED,
                    )
                    if name == "normalized/ruleset.json":
                        setattr(info, attribute, value)
                    target.writestr(info, data)
            with self.assertRaises(mcs_archive.MCSError):
                mcs_archive.inspect(archive)

    def test_wrong_extension_and_overwrite_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "wrong.zip"
            with self.assertRaises(mcs_archive.MCSError):
                mcs_archive.pack(ROOT / "examples/minimal", output, ROOT)
            output = Path(tmp) / "exists.mcs"
            output.write_bytes(b"x")
            with self.assertRaises(mcs_archive.MCSError):
                mcs_archive.pack(ROOT / "examples/minimal", output, ROOT)
            target = Path(tmp) / "target"
            target.write_bytes(b"safe")
            output = Path(tmp) / "symlink.mcs"
            output.symlink_to(target)
            with self.assertRaises(mcs_archive.MCSError):
                mcs_archive.pack(ROOT / "examples/minimal", output, ROOT, force=True)
            self.assertEqual(target.read_bytes(), b"safe")


if __name__ == "__main__":
    unittest.main()
