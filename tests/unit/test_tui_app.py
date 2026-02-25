from __future__ import annotations

import ast
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[2] / "source" / "TUI" / "app.py"


def _load_app_class() -> ast.ClassDef:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "KSDownloaderApp":
            return node
    raise AssertionError("KSDownloaderApp class not found")


def test_app_initialization_method_exists() -> None:
    cls = _load_app_class()
    methods = {node.name for node in cls.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert "__init__" in methods


def test_css_path_points_to_tcss_file_name() -> None:
    cls = _load_app_class()
    for node in cls.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "CSS_PATH":
                    expression = ast.unparse(node.value)
                    assert "KS-Downloader.tcss" in expression
                    return
    raise AssertionError("CSS_PATH assignment not found")


def test_action_methods_exist() -> None:
    cls = _load_app_class()
    methods = {node.name for node in cls.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert "action_settings" in methods
    assert "action_update" in methods
    assert "action_about" in methods
    assert "refresh_screen" in methods
    assert "update_result" in methods
