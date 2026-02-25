from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.app import App, ComposeResult
from textual.screen import ModalScreen, Screen
from textual.widgets import Label, LoadingIndicator

from source.TUI.loading import LoadingScreen


class _IndexScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("index")


class _LoadingApp(App[None]):
    async def on_mount(self) -> None:
        self.push_screen(_IndexScreen())
        self.push_screen(LoadingScreen())


def test_loading_screen_type() -> None:
    screen = LoadingScreen()
    assert isinstance(screen, ModalScreen)


def test_loading_screen_compose_has_indicator() -> None:
    async def scenario():
        app = _LoadingApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            assert isinstance(app.screen, LoadingScreen)
            assert app.screen.query_one(LoadingIndicator)

    asyncio.run(scenario())


def test_loading_screen_can_be_dismissed() -> None:
    async def scenario():
        app = _LoadingApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            app.pop_screen()
            await pilot.pause()
            assert not isinstance(app.screen, LoadingScreen)

    asyncio.run(scenario())
