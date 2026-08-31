from __future__ import annotations

import json
import math
import re
from typing import Any

QUALIFIED_ID = re.compile(r"^[a-z][a-z0-9+.-]*:.+$")
IDENTIFIER = re.compile(r"^[a-z][A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*$")
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
VALUE_KINDS = {
    "string",
    "boolean",
    "integer",
    "number",
    "quantity",
    "enum",
    "reference",
    "stringList",
    "referenceList",
}
VALUE_KEYS = {kind: {"type", "value"} for kind in VALUE_KINDS}
VALUE_KEYS["quantity"] = {"type", "value", "unit"}
SELECTOR_OPERATORS = {
    "equals",
    "notEquals",
    "lessThan",
    "lessThanOrEquals",
    "greaterThan",
    "greaterThanOrEquals",
    "matches",
    "exists",
}


def fail(context: str, message: str) -> None:
    raise SystemExit(f"validation failed: {context}: {message}")


def object_value(value: Any, context: str) -> dict[str, Any]:
    if type(value) is not dict:
        fail(context, "expected object")
    return value


def list_value(value: Any, context: str) -> list[Any]:
    if type(value) is not list:
        fail(context, "expected list")
    return value


def exact_keys(
    value: dict[str, Any], required: set[str], optional: set[str], context: str
) -> None:
    missing = required - value.keys()
    unknown = value.keys() - required - optional
    if missing or unknown:
        fail(context, f"missing={sorted(missing)}, unknown={sorted(unknown)}")


def localized_text(value: Any, context: str) -> None:
    value = object_value(value, context)
    exact_keys(value, {"default", "translations"}, set(), context)
    if type(value["default"]) is not str or not value["default"]:
        fail(context, "default text must be non-empty")
    translations = object_value(value["translations"], f"{context}.translations")
    if any(
        type(key) is not str or type(text) is not str
        for key, text in translations.items()
    ):
        fail(context, "translations must map locale tags to strings")


def string_list(value: Any, context: str) -> list[str]:
    values = list_value(value, context)
    if any(type(item) is not str for item in values):
        fail(context, "expected strings")
    return values


def package_metadata(value: Any, context: str) -> str:
    value = object_value(value, context)
    exact_keys(
        value,
        {"id", "name", "version", "authors"},
        {"description", "repository", "license"},
        context,
    )
    if type(value["id"]) is not str or not QUALIFIED_ID.fullmatch(value["id"]):
        fail(context, "invalid package id")
    if type(value["name"]) is not str or not value["name"]:
        fail(context, "package name must be non-empty")
    if type(value["version"]) is not str or not SEMVER.fullmatch(value["version"]):
        fail(context, "invalid package version")
    authors = string_list(value["authors"], f"{context}.authors")
    if any(not author for author in authors):
        fail(context, "authors must be non-empty strings")
    for field in ("description", "repository", "license"):
        if field in value and (type(value[field]) is not str or not value[field]):
            fail(context, f"{field} must be a non-empty string")
    return value["id"]


def parameter_value(
    value: Any, expected_kind: str | None, context: str
) -> dict[str, Any]:
    value = object_value(value, context)
    kind = value.get("type")
    if (
        type(kind) is not str
        or kind not in VALUE_KINDS
        or (expected_kind is not None and kind != expected_kind)
    ):
        fail(
            context, f"expected {expected_kind or 'known'} value variant, got {kind!r}"
        )
    exact_keys(value, VALUE_KEYS[kind], set(), context)
    item = value["value"]
    if kind in {"string", "enum", "reference"}:
        if type(item) is not str:
            fail(context, "value must be a string")
        if kind == "enum" and not IDENTIFIER.fullmatch(item):
            fail(context, "invalid enum identifier")
        if kind == "reference" and not QUALIFIED_ID.fullmatch(item):
            fail(context, "invalid qualified reference")
    elif kind == "boolean":
        if type(item) is not bool:
            fail(context, "value must be a boolean")
    elif kind == "integer":
        if type(item) is not int:
            fail(context, "value must be an integer")
    elif kind in {"number", "quantity"}:
        if type(item) not in {int, float} or not math.isfinite(item):
            fail(context, "value must be a finite number")
        if kind == "quantity" and (type(value["unit"]) is not str or not value["unit"]):
            fail(context, "quantity unit must be non-empty")
    else:
        items = list_value(item, f"{context}.value")
        for index, entry in enumerate(items):
            if type(entry) is not str:
                fail(f"{context}.value[{index}]", "expected string")
            if kind == "referenceList" and not QUALIFIED_ID.fullmatch(entry):
                fail(f"{context}.value[{index}]", "invalid qualified reference")
    return value


def validate_parameter_definition(value: Any, context: str) -> dict[str, Any]:
    value = object_value(value, context)
    exact_keys(
        value,
        {"id", "name", "kind", "required", "allowedValues"},
        {"defaultValue", "unitDimension", "description"},
        context,
    )
    if type(value["id"]) is not str or not IDENTIFIER.fullmatch(value["id"]):
        fail(context, "invalid parameter id")
    localized_text(value["name"], f"{context}.name")
    if "description" in value:
        localized_text(value["description"], f"{context}.description")
    kind = value["kind"]
    if (
        type(kind) is not str
        or kind not in VALUE_KINDS
        or type(value["required"]) is not bool
    ):
        fail(context, "invalid parameter kind or required flag")
    dimension = value.get("unitDimension")
    if kind == "quantity":
        if type(dimension) is not str or not dimension:
            fail(context, "quantity parameters require unitDimension")
    elif "unitDimension" in value:
        fail(context, "unitDimension is only valid for quantity parameters")
    if "defaultValue" in value:
        parameter_value(value["defaultValue"], kind, f"{context}.defaultValue")
    allowed = list_value(value["allowedValues"], f"{context}.allowedValues")
    seen: set[str] = set()
    for index, allowed_value in enumerate(allowed):
        validated = parameter_value(
            allowed_value, kind, f"{context}.allowedValues[{index}]"
        )
        marker = json.dumps(validated, sort_keys=True, separators=(",", ":"))
        if marker in seen:
            fail(context, "duplicate allowed value")
        seen.add(marker)
    if "defaultValue" in value and allowed and value["defaultValue"] not in allowed:
        fail(context, "defaultValue is outside allowedValues")
    return value


def validate_definition_document(
    value: Any, context: str
) -> tuple[str, dict[str, dict[str, Any]]]:
    value = object_value(value, context)
    exact_keys(value, {"schemaVersion", "package", "definitions"}, set(), context)
    package_id = package_metadata(value["package"], f"{context}.package")
    definitions = object_value(value["definitions"], f"{context}.definitions")
    if not definitions:
        fail(context, "definition package is empty")
    for definition_id, definition in definitions.items():
        definition_context = f"{context}.definitions[{definition_id!r}]"
        definition = object_value(definition, definition_context)
        exact_keys(
            definition,
            {"id", "name", "capability", "parameters", "tags"},
            {"description"},
            definition_context,
        )
        if definition_id != definition["id"] or not QUALIFIED_ID.fullmatch(
            definition_id
        ):
            fail(definition_context, "map key and definition id must match")
        localized_text(definition["name"], f"{definition_context}.name")
        if "description" in definition:
            localized_text(
                definition["description"], f"{definition_context}.description"
            )
        if type(definition["capability"]) is not str or not QUALIFIED_ID.fullmatch(
            definition["capability"]
        ):
            fail(definition_context, "invalid capability id")
        parameters = object_value(
            definition["parameters"], f"{definition_context}.parameters"
        )
        for parameter_id, parameter in parameters.items():
            validated = validate_parameter_definition(
                parameter, f"{definition_context}.parameters[{parameter_id!r}]"
            )
            if parameter_id != validated["id"]:
                fail(definition_context, "parameter map key and id must match")
        string_list(definition["tags"], f"{definition_context}.tags")
    return package_id, definitions


def validate_selector(value: Any, context: str) -> None:
    value = object_value(value, context)
    kind = value.get("kind")
    if type(kind) is not str:
        fail(context, "selector kind must be a string")
    if kind == "all":
        exact_keys(value, {"kind"}, set(), context)
    elif kind == "entityType":
        exact_keys(
            value, {"kind", "typeSystem", "typeName", "includeSubtypes"}, set(), context
        )
        if (
            type(value["typeSystem"]) is not str
            or not QUALIFIED_ID.fullmatch(value["typeSystem"])
            or type(value["typeName"]) is not str
            or not value["typeName"]
            or type(value["includeSubtypes"]) is not bool
        ):
            fail(context, "invalid entity type selector")
    elif kind == "property":
        exact_keys(
            value, {"kind", "property", "operator"}, {"propertySet", "value"}, context
        )
        operator = value["operator"]
        if (
            type(operator) is not str
            or operator not in SELECTOR_OPERATORS
            or type(value["property"]) is not str
            or not value["property"]
        ):
            fail(context, "invalid property selector")
        if "propertySet" in value and (
            type(value["propertySet"]) is not str or not value["propertySet"]
        ):
            fail(context, "propertySet must be a non-empty string")
        if operator == "exists" and "value" in value:
            fail(context, "exists selector must not have a value")
        if operator != "exists" and "value" not in value:
            fail(context, "comparison selector requires a value")
        if "value" in value:
            checked = parameter_value(value["value"], None, f"{context}.value")
            if operator == "matches" and checked["type"] != "string":
                fail(context, "matches requires a string value")
    elif kind == "classification":
        exact_keys(
            value, {"kind", "system", "code", "includeDescendants"}, set(), context
        )
        if (
            any(
                type(value[key]) is not str or not value[key]
                for key in ("system", "code")
            )
            or type(value["includeDescendants"]) is not bool
        ):
            fail(context, "invalid classification selector")
    elif kind in {"allOf", "anyOf"}:
        exact_keys(value, {"kind", "operands"}, set(), context)
        operands = list_value(value["operands"], f"{context}.operands")
        if not operands:
            fail(context, "compound selector requires operands")
        for index, operand in enumerate(operands):
            validate_selector(operand, f"{context}.operands[{index}]")
    elif kind == "not":
        exact_keys(value, {"kind", "operand"}, set(), context)
        validate_selector(value["operand"], f"{context}.operand")
    else:
        fail(context, f"unknown selector kind {kind!r}")


def bind_ruleset(
    value: Any, definition_documents: list[dict[str, Any]], context: str
) -> None:
    value = object_value(value, context)
    exact_keys(
        value,
        {"schemaVersion", "package", "definitionPackages", "root"},
        set(),
        context,
    )
    package_metadata(value["package"], f"{context}.package")
    declared_list = string_list(
        value["definitionPackages"], f"{context}.definitionPackages"
    )
    if (
        not declared_list
        or any(not QUALIFIED_ID.fullmatch(package_id) for package_id in declared_list)
        or len(set(declared_list)) != len(declared_list)
    ):
        fail(context, "definitionPackages must be non-empty, qualified, and unique")
    definitions: dict[str, dict[str, Any]] = {}
    loaded_packages: set[str] = set()
    for index, document in enumerate(definition_documents):
        package_id, package_definitions = validate_definition_document(
            document, f"{context}.definitionDocuments[{index}]"
        )
        if package_id in loaded_packages:
            fail(context, f"duplicate definition package {package_id!r}")
        loaded_packages.add(package_id)
        overlap = definitions.keys() & package_definitions.keys()
        if overlap:
            fail(context, f"duplicate definition ids {sorted(overlap)}")
        definitions.update(package_definitions)
    if set(declared_list) != loaded_packages:
        fail(
            context,
            f"declared definition packages {sorted(declared_list)} do not match loaded packages {sorted(loaded_packages)}",
        )
    seen_ids: set[str] = set()

    def walk(folder: Any, folder_context: str) -> None:
        folder = object_value(folder, folder_context)
        exact_keys(
            folder,
            {"id", "name", "rules", "folders"},
            {"description"},
            folder_context,
        )
        folder_id = folder["id"]
        if type(folder_id) is not str or not IDENTIFIER.fullmatch(folder_id):
            fail(folder_context, "invalid folder id")
        if folder_id in seen_ids:
            fail(folder_context, f"duplicate rule/folder id {folder_id!r}")
        seen_ids.add(folder_id)
        localized_text(folder["name"], f"{folder_context}.name")
        if "description" in folder:
            localized_text(folder["description"], f"{folder_context}.description")
        for index, rule in enumerate(
            list_value(folder["rules"], f"{folder_context}.rules")
        ):
            rule_context = f"{folder_context}.rules[{index}]"
            rule = object_value(rule, rule_context)
            exact_keys(
                rule,
                {
                    "id",
                    "definitionId",
                    "name",
                    "enabled",
                    "severity",
                    "parameters",
                    "applicability",
                    "tags",
                },
                {"description", "message"},
                rule_context,
            )
            rule_id = rule["id"]
            definition_id = rule["definitionId"]
            if type(rule_id) is not str or not IDENTIFIER.fullmatch(rule_id):
                fail(rule_context, "invalid rule id")
            if type(definition_id) is not str or not QUALIFIED_ID.fullmatch(
                definition_id
            ):
                fail(rule_context, "invalid definitionId")
            if (
                type(rule["enabled"]) is not bool
                or type(rule["severity"]) is not str
                or rule["severity"] not in {"info", "warning", "error"}
            ):
                fail(rule_context, "invalid enabled flag or severity")
            localized_text(rule["name"], f"{rule_context}.name")
            for field in ("description", "message"):
                if field in rule:
                    localized_text(rule[field], f"{rule_context}.{field}")
            string_list(rule["tags"], f"{rule_context}.tags")
            if rule_id in seen_ids:
                fail(rule_context, f"duplicate rule/folder id {rule_id!r}")
            seen_ids.add(rule_id)
            definition = definitions.get(definition_id)
            if definition is None:
                fail(rule_context, f"unknown definitionId {definition_id!r}")
            bindings = object_value(rule["parameters"], f"{rule_context}.parameters")
            parameters = definition["parameters"]
            unknown = bindings.keys() - parameters.keys()
            missing = {
                key for key, parameter in parameters.items() if parameter["required"]
            } - bindings.keys()
            if unknown or missing:
                fail(
                    rule_context,
                    f"unknown parameters={sorted(unknown)}, missing required parameters={sorted(missing)}",
                )
            for parameter_id, binding in bindings.items():
                parameter = parameters[parameter_id]
                checked = parameter_value(
                    binding,
                    parameter["kind"],
                    f"{rule_context}.parameters[{parameter_id!r}]",
                )
                if (
                    parameter["allowedValues"]
                    and checked not in parameter["allowedValues"]
                ):
                    fail(
                        rule_context,
                        f"parameter {parameter_id!r} is outside allowedValues",
                    )
            validate_selector(rule["applicability"], f"{rule_context}.applicability")
        for index, child in enumerate(
            list_value(folder["folders"], f"{folder_context}.folders")
        ):
            walk(child, f"{folder_context}.folders[{index}]")

    walk(value["root"], f"{context}.root")
