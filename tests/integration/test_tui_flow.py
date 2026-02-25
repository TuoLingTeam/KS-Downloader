from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Checkbox, Input, Label, Select

from source.TUI.index import IndexScreen
from source.TUI.setting import SettingScreen


class _MemoryConfig:
    def __init__(self):
        self.data = {"cookie": ""}

    def read(self):
        return dict(self.data)

    def write(self, data):
        self.data = dict(data)


class _MemoryDatabase:
    def __init__(self):
        self.config_updates = []
        self.option_updates = []
        self.record = 1

    async def update_config_data(self, name: str, value: int):
        self.config_updates.append((name, value))

    async def update_option_data(self, name: str, value: str):
        self.option_updates.append((name, value))


class _FakeKS:
    def __init__(self):
        self.print = None
        self.detail_calls = []
        self.config_obj = _MemoryConfig()
        self.database = _MemoryDatabase()
        self.config = {"Record": 1}
        self.option = {"Language": "zh_CN"}

    async def detail(self, text: str):
        self.detail_calls.append(text)

    def set_language(self, language: str):
        self.option["Language"] = language


class _AboutStub(Screen):
    def compose(self) -> ComposeResult:
        yield Label("about")


class _TUIFlowApp(App[None]):
    def __init__(self, ks: _FakeKS):
        super().__init__()
        self.ks = ks

    async def on_mount(self) -> None:
        self.push_screen(IndexScreen(self.ks))

    async def action_settings(self) -> None:
        self.push_screen(SettingScreen(self.ks))

    async def action_update(self) -> None:
        return None

    async def action_about(self) -> None:
        self.push_screen(_AboutStub())

    async def refresh_screen(self) -> None:
        if isinstance(self.screen, SettingScreen):
            self.pop_screen()


def test_tui_user_flow_start_input_download_settings_quit() -> None:
    async def scenario():
        ks = _FakeKS()
        app = _TUIFlowApp(ks)

        async with app.run_test() as pilot:
            await pilot.pause()
            # startup -> input -> download
            app.screen.query_one("#url", Input).value = "https://v.kuaishou.com/demo"
            await pilot.click("#deal")
            await pilot.pause()
            assert ks.detail_calls == ["https://v.kuaishou.com/demo"]

            # open settings via shortcut, save config, and return
            await pilot.press("s")
            await pilot.pause()
            app.screen.query_one("#cookie", Input).value = "foo=bar"
            app.screen.query_one("#record", Checkbox).value = False
            app.screen.query_one("#language", Select).value = "en_US"
            await pilot.click("#save")
            await pilot.pause()

            assert ks.config_obj.read()["cookie"] == "foo=bar"
            assert ks.config["Record"] == 0
            assert ks.option["Language"] == "en_US"
            assert isinstance(app.screen, IndexScreen)

            # quit
            await pilot.press("q")

    asyncio.run(scenario())
