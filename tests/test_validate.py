from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate


class LocalModuleTests(unittest.TestCase):
    def test_accepts_existing_local_pkl_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            module = base / "rules.pkl"
            module.write_text("value = 1\n")
            self.assertEqual(validate.local_module(base, "rules.pkl"), module.resolve())

    def test_rejects_traversal_absolute_missing_and_wrong_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for value in ("../rules.pkl", "/rules.pkl", "missing.pkl", "rules.json"):
                with self.subTest(value=value), self.assertRaises(SystemExit):
                    validate.local_module(base, value)

    def test_rejects_symlink_escaping_package_root(self) -> None:
        with (
            tempfile.TemporaryDirectory() as package,
            tempfile.TemporaryDirectory() as outside,
        ):
            base = Path(package)
            target = Path(outside) / "rules.pkl"
            target.write_text("value = 1\n")
            (base / "rules.pkl").symlink_to(target)
            with self.assertRaises(SystemExit):
                validate.local_module(base, "rules.pkl")


class IdentityTests(unittest.TestCase):
    def test_qualified_ids_and_semver_are_fail_closed(self) -> None:
        self.assertIsNotNone(validate.QUALIFIED_ID.fullmatch("axioval:example.rules"))
        self.assertIsNone(validate.QUALIFIED_ID.fullmatch("example.rules"))
        self.assertIsNotNone(validate.SEMVER.fullmatch("1.2.3-beta.1+build.5"))
        self.assertIsNone(validate.SEMVER.fullmatch("01.2.3"))


class BindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        expected = validate.ROOT / "examples/minimal/expected"
        cls.definitions = json.loads((expected / "definitions.json").read_text())
        cls.ruleset = json.loads((expected / "ruleset.json").read_text())

    def copies(self) -> tuple[dict, dict]:
        return copy.deepcopy(self.ruleset), copy.deepcopy(self.definitions)

    def test_accepts_fully_bound_ruleset(self) -> None:
        ruleset, definitions = self.copies()
        validate.bind_ruleset(ruleset, [definitions], "test")

    def test_rejects_unknown_definition(self) -> None:
        ruleset, definitions = self.copies()
        ruleset["root"]["rules"][0]["definitionId"] = "axioval:missing"
        with self.assertRaises(SystemExit):
            validate.bind_ruleset(ruleset, [definitions], "test")

    def test_rejects_undeclared_definition_package(self) -> None:
        ruleset, definitions = self.copies()
        ruleset["definitionPackages"] = ["axioval:other"]
        with self.assertRaises(SystemExit):
            validate.bind_ruleset(ruleset, [definitions], "test")

    def test_rejects_unknown_and_missing_parameters(self) -> None:
        ruleset, definitions = self.copies()
        params = ruleset["root"]["rules"][0]["parameters"]
        params["surprise"] = {"type": "string", "value": "x"}
        with self.assertRaises(SystemExit):
            validate.bind_ruleset(ruleset, [definitions], "test")
        ruleset, definitions = self.copies()
        definitions["definitions"]["axioval:example.property-exists"]["parameters"][
            "property"
        ]["defaultValue"] = {"type": "string", "value": "Reference"}
        del ruleset["root"]["rules"][0]["parameters"]["property"]
        with self.assertRaises(SystemExit):
            validate.bind_ruleset(ruleset, [definitions], "test")

    def test_rejects_wrong_value_variant(self) -> None:
        ruleset, definitions = self.copies()
        ruleset["root"]["rules"][0]["parameters"]["property"] = {
            "type": "boolean",
            "value": True,
        }
        with self.assertRaises(SystemExit):
            validate.bind_ruleset(ruleset, [definitions], "test")

    def test_accepts_schema_optional_descriptions_and_messages(self) -> None:
        ruleset, definitions = self.copies()
        text = {"default": "Optional", "translations": {}}
        definition = definitions["definitions"]["axioval:example.property-exists"]
        definition.pop("description")
        definition["parameters"]["property"]["description"] = text
        ruleset["root"]["description"] = text
        rule = ruleset["root"]["rules"][0]
        rule["description"] = text
        rule["message"] = text
        validate.bind_ruleset(ruleset, [definitions], "test")

    def test_accepts_compatible_default_and_allowed_value(self) -> None:
        _, definitions = self.copies()
        parameter = definitions["definitions"]["axioval:example.property-exists"][
            "parameters"
        ]["property"]
        parameter["defaultValue"] = {"type": "string", "value": "Reference"}
        parameter["allowedValues"] = [{"type": "string", "value": "Reference"}]
        validate.validate_definition_document(definitions, "test")

    def test_rejects_incompatible_definition_default(self) -> None:
        for invalid_default in (None, {"type": "boolean", "value": True}):
            _, definitions = self.copies()
            definitions["definitions"]["axioval:example.property-exists"]["parameters"][
                "property"
            ]["defaultValue"] = invalid_default
            with (
                self.subTest(invalid_default=invalid_default),
                self.assertRaises(SystemExit),
            ):
                validate.validate_definition_document(definitions, "test")

    def test_rejects_value_outside_allowed_set(self) -> None:
        ruleset, definitions = self.copies()
        definitions["definitions"]["axioval:example.property-exists"]["parameters"][
            "property"
        ]["allowedValues"] = [{"type": "string", "value": "Other"}]
        with self.assertRaises(SystemExit):
            validate.bind_ruleset(ruleset, [definitions], "test")


class StaticManifestTests(unittest.TestCase):
    def test_schema_and_validator_required_fields_stay_in_sync(self) -> None:
        schema = json.loads(
            (validate.ROOT / "schema/registry-manifest.schema.json").read_text()
        )
        self.assertEqual(set(schema["required"]), validate.REQUIRED)
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["definitionEntrypoints"]["minItems"], 1)
        self.assertEqual(
            schema["properties"]["entrypoint"]["pattern"],
            validate.PKL_ENTRYPOINT.pattern,
        )
        self.assertEqual(
            schema["properties"]["definitionEntrypoints"]["items"]["pattern"],
            validate.PKL_ENTRYPOINT.pattern,
        )

    def test_rejects_missing_or_malformed_definition_entrypoints(self) -> None:
        manifest = json.loads(
            (validate.ROOT / "examples/minimal/axioval.json").read_text()
        )
        for entries in (None, [], ["definitions.pkl", "definitions.pkl"], [{}]):
            candidate = copy.deepcopy(manifest)
            if entries is None:
                del candidate["definitionEntrypoints"]
            else:
                candidate["definitionEntrypoints"] = entries
            with self.subTest(entries=entries), self.assertRaises(SystemExit):
                validate.validate_manifest(candidate, Path("axioval.json"))

    def test_rejects_unsafe_entrypoint_paths_before_resolution(self) -> None:
        manifest = json.loads(
            (validate.ROOT / "examples/minimal/axioval.json").read_text()
        )
        for field, value in (
            ("entrypoint", "/ruleset.pkl"),
            ("entrypoint", "../ruleset.pkl"),
            ("entrypoint", "ruleset.txt"),
            ("definitionEntrypoints", ["/definitions.pkl"]),
            ("definitionEntrypoints", ["../definitions.pkl"]),
            ("definitionEntrypoints", ["definitions.txt"]),
        ):
            candidate = copy.deepcopy(manifest)
            candidate[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(SystemExit):
                validate.validate_manifest(candidate, Path("axioval.json"))


class SelectorTests(unittest.TestCase):
    def test_rejects_exists_with_value_and_comparison_without_value(self) -> None:
        from scripts.contracts import validate_selector

        with self.assertRaises(SystemExit):
            validate_selector(
                {
                    "kind": "property",
                    "property": "Reference",
                    "operator": "exists",
                    "value": {"type": "string", "value": "x"},
                },
                "test",
            )
        with self.assertRaises(SystemExit):
            validate_selector(
                {"kind": "property", "property": "Reference", "operator": "equals"},
                "test",
            )


if __name__ == "__main__":
    unittest.main()
