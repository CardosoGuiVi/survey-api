from typing import Any

from sqlalchemy import Enum as SAEnum


def assert_model_schema(model: Any, expected: dict[str, dict[str, Any]]) -> None:
    columns = model.__table__.columns

    for col_name, rules in expected.items():
        assert col_name in columns, f"Missing column: {col_name}"
        col = columns[col_name]

        if "type" in rules:
            assert isinstance(col.type, rules["type"]), (
                f"{col_name}: expected type {rules['type']}, got {type(col.type)}"
            )

        if "length" in rules:
            assert getattr(col.type, "length", None) == rules["length"], (
                f"{col_name}: expected length {rules['length']}"
            )

        if "nullable" in rules:
            assert col.nullable == rules["nullable"], (
                f"{col_name}: expected nullable={rules['nullable']}"
            )

        if rules.get("pk"):
            assert col.primary_key, f"{col_name} should be primary key"

        if rules.get("server_default"):
            assert col.server_default is not None, (
                f"{col_name} should have server_default"
            )

        if "unique" in rules:
            is_unique = col.unique or any(
                col_name in constraint.columns
                for constraint in model.__table__.constraints
                if constraint.__class__.__name__ == "UniqueConstraint"
            )

            assert is_unique == rules["unique"], (
                f"{col_name}: expected unique={rules['unique']}"
            )

        if "enum" in rules:
            assert isinstance(col.type, SAEnum), f"{col_name}: expected Enum type"

            expected_enum = rules["enum"]

            assert set(col.type.enums) == {e.value for e in expected_enum}, (
                f"{col_name}: enum values mismatch"
            )
