from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.app import App
from textual.widgets import Input

from source.TUI.index import IndexScreen


class _FakeKS:
    def __init__(self):
        self.print = None
        self.detail_calls: list[str] = []

    async def detail(self, text: str) -> None:
        self.detail_calls.append(text)


class _IndexApp(App[None]):
    def __init__(self, ks: _FakeKS):
        super().__init__()
        self.ks = ks

    async def on_mount(self) -> None:
        self.push_screen(IndexScreen(self.ks))

    async def action_settings(self) -> None:
        return None

    async def action_update(self) -> None:
        return None

    async def action_about(self) -> None:
        return None


def test_index_bindings() -> None:
    keys = {binding.key for binding in IndexScreen.BINDINGS}
    assert {"q", "u", "s", "a"}.issubset(keys)


def test_empty_input_shows_warning_and_does_not_start_download() -> None:
    async def scenario():
        ks = _FakeKS()
        app = _IndexApp(ks)
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.click("#deal")
            await pilot.pause()
            assert ks.detail_calls == []

    asyncio.run(scenario())


def test_paste_button_reads_clipboard(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario():
        ks = _FakeKS()
        app = _IndexApp(ks)
        monkeypatch.setattr(
            "source.TUI.index.pyperclip.paste", lambda: "https://v.kuaishou.com/test"
        )

        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.click("#paste")
            await pilot.pause()
            assert (
                app.screen.query_one("#url", Input).value
                == "https://v.kuaishou.com/test"
            )

    asyncio.run(scenario())


def test_reset_button_clears_input() -> None:
    async def scenario():
        ks = _FakeKS()
        app = _IndexApp(ks)
        async with app.run_test() as pilot:
            await pilot.pause()
            app.screen.query_one("#url", Input).value = "abc"
            await pilot.click("#reset")
            await pilot.pause()
            assert app.screen.query_one("#url", Input).value == ""

    asyncio.run(scenario())
