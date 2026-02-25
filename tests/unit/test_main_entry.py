from __future__ import annotations

import asyncio
import importlib.util
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "main.py"


class _FakeKS:
    def __init__(self, server_mode: bool = False):
        self.server_mode = server_mode

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None

    async def run_api_server(self, host, port, log_level):
        _state["api_calls"].append((self.server_mode, host, port, log_level))


class _FakeTUIApp:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None

    async def run_async(self):
        _state["tui_calls"] += 1


_state: dict[str, list | int] = {"api_calls": [], "tui_calls": 0}


def _load_main_with_stubs(monkeypatch: pytest.MonkeyPatch) -> types.ModuleType:
    source_module = types.ModuleType("source")
    source_module.KS = _FakeKS

    source_tui_module = types.ModuleType("source.TUI")
    source_tui_module.KSDownloaderApp = _FakeTUIApp

    monkeypatch.setitem(sys.modules, "source", source_module)
    monkeypatch.setitem(sys.modules, "source.TUI", source_tui_module)

    spec = importlib.util.spec_from_file_location("main_test_module", MAIN)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_args_starts_tui(monkeypatch: pytest.MonkeyPatch) -> None:
    global _state
    _state = {"api_calls": [], "tui_calls": 0}

    module = _load_main_with_stubs(monkeypatch)
    module.argv = ["main.py"]
    monkeypatch.setattr(sys, "argv", ["main.py"])

    asyncio.run(module.main())

    assert _state["tui_calls"] == 1
    assert _state["api_calls"] == []


def test_api_arg_starts_api_server(monkeypatch: pytest.MonkeyPatch) -> None:
    global _state
    _state = {"api_calls": [], "tui_calls": 0}

    module = _load_main_with_stubs(monkeypatch)
    module.argv = ["main.py", "api", "--host", "127.0.0.1", "--port", "6000"]
    namespace = types.SimpleNamespace(mode="api", host="127.0.0.1", port=6000)
    monkeypatch.setattr(
        module.argparse.ArgumentParser,
        "parse_known_args",
        lambda self: (namespace, []),
    )

    asyncio.run(module.main())

    assert _state["tui_calls"] == 0
    assert _state["api_calls"] == [(True, "127.0.0.1", 6000, "info")]
