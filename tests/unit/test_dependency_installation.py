from __future__ import annotations

import importlib.util
from pathlib import Path


def test_requirements_pin_tui_dependencies() -> None:
    requirements = Path(__file__).resolve().parents[2] / "requirements.txt"
    content = requirements.read_text(encoding="utf-8")
    assert "textual==" in content
    assert "pyperclip==" in content


def test_tui_runtime_dependency_availability_or_fallback() -> None:
    assert importlib.util.find_spec("textual") is not None

    # `pyperclip` may be absent in offline CI. Index screen provides a safe fallback.
    from source.TUI import index as index_module

    assert hasattr(index_module.pyperclip, "paste")
