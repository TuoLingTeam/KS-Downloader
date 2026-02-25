from __future__ import annotations

import ast
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[2] / "source" / "app" / "app.py"


def _load_ks_class() -> ast.ClassDef:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "KS":
            return node
    raise AssertionError("KS class not found")


def _method_map(ks: ast.ClassDef) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    result: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
    for node in ks.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name] = node
    return result


def test_ks_contains_print_redirect_attribute() -> None:
    ks = _load_ks_class()
    init = _method_map(ks)["__init__"]
    assigned_names: set[str] = set()
    for node in ast.walk(init):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                ):
                    assigned_names.add(target.attr)
    assert "print" in assigned_names


def test_public_method_signatures_and_return_annotations_stable() -> None:
    ks = _load_ks_class()
    methods = _method_map(ks)

    expected_args = {
        "run": ["self"],
        "detail": ["self", "detail", "download"],
        "detail_one": ["self", "url", "download", "proxy", "cookie"],
        "update_author_nickname": ["self", "data"],
        "user": ["self"],
        "disclaimer": ["self"],
        "close": ["self"],
        "run_api_server": ["self", "host", "port", "log_level"],
        "setup_routes": ["self", "server"],
    }

    for name, args in expected_args.items():
        assert name in methods, f"missing method: {name}"
        method = methods[name]
        actual_args = [arg.arg for arg in method.args.args]
        assert actual_args == args

    expected_returns = {
        "detail_one": "dict | str",
        "__handle_detail_html": "dict | None",
    }
    for name, expected in expected_returns.items():
        method = methods[name]
        assert method.returns is not None
        assert ast.unparse(method.returns) == expected
