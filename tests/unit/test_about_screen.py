from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.app import App
from textual.widgets import Button, Label

from source.TUI.about import AboutScreen
from source.static import VERSION_BETA, VERSION_MAJOR, VERSION_MINOR


class _AboutApp(App[None]):
    async def on_mount(self) -> None:
        self.push_screen(AboutScreen())


def test_about_contains_version_text() -> None:
    async def scenario():
        app = _AboutApp()
        version = f"{VERSION_MAJOR}.{VERSION_MINOR}.{'beta' if VERSION_BETA else 'stable'}"

        async with app.run_test() as pilot:
            await pilot.pause()
            labels = [str(widget.render()) for widget in app.screen.query(Label)]
            assert any(version in text for text in labels)

    asyncio.run(scenario())


def test_about_contains_wechat_info_and_close_button() -> None:
    async def scenario():
        app = _AboutApp()

        async with app.run_test() as pilot:
            await pilot.pause()
            labels = [str(widget.render()) for widget in app.screen.query(Label)]
            assert any(
                ("微信公众号：驼铃电商技术团" in text) or ("WeChat Official Account" in text)
                for text in labels
            )
            assert app.screen.query_one("#close_about", Button)

    asyncio.run(scenario())
