from __future__ import annotations

import ast
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[2] / "source" / "app" / "app.py"


def _load_tree() -> ast.Module:
    return ast.parse(SOURCE.read_text(encoding="utf-8"))


def _get_ks_class(tree: ast.Module) -> ast.ClassDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "KS":
            return node
    raise AssertionError("KS class not found")


def _get_method(class_def: ast.ClassDef, method: str) -> ast.AsyncFunctionDef | ast.FunctionDef:
    for node in class_def.body:
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)) and node.name == method:
            return node
    raise AssertionError(f"method not found: {method}")


def _decorator_info(decorator: ast.expr) -> tuple[str, str, str | None] | None:
    if not isinstance(decorator, ast.Call):
        return None
    if not isinstance(decorator.func, ast.Attribute):
        return None
    if not isinstance(decorator.func.value, ast.Name):
        return None
    if decorator.func.value.id != "server":
        return None
    if not decorator.args:
        return None
    first_arg = decorator.args[0]
    if not isinstance(first_arg, ast.Constant) or not isinstance(first_arg.value, str):
        return None

    response_model = None
    for keyword in decorator.keywords:
        if keyword.arg == "response_model":
            if isinstance(keyword.value, ast.Name):
                response_model = keyword.value.id
            else:
                response_model = ast.unparse(keyword.value)
    return decorator.func.attr, first_arg.value, response_model


def test_api_routes_keep_paths_and_models() -> None:
    tree = _load_tree()
    ks = _get_ks_class(tree)
    setup_routes = _get_method(ks, "setup_routes")

    decorators: set[tuple[str, str, str | None]] = set()
    for node in setup_routes.body:
        if isinstance(node, ast.AsyncFunctionDef):
            for deco in node.decorator_list:
                info = _decorator_info(deco)
                if info:
                    decorators.add(info)

    assert ("get", "/", None) in decorators
    assert ("post", "/share", "UrlResponse") in decorators
    assert ("post", "/detail/", "ResponseModel") in decorators


def test_run_api_server_signature_is_compatible() -> None:
    tree = _load_tree()
    ks = _get_ks_class(tree)
    run_api_server = _get_method(ks, "run_api_server")
    assert isinstance(run_api_server, ast.AsyncFunctionDef)

    arg_names = [arg.arg for arg in run_api_server.args.args]
    assert arg_names == ["self", "host", "port", "log_level"]
