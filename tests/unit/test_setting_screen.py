from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Checkbox, Input, Label, Select

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
        self.config_updates: list[tuple[str, int]] = []
        self.option_updates: list[tuple[str, str]] = []
        self.record = 1

    async def update_config_data(self, name: str, value: int):
        self.config_updates.append((name, value))

    async def update_option_data(self, name: str, value: str):
        self.option_updates.append((name, value))


class _FakeKS:
    def __init__(self):
        self.config_obj = _MemoryConfig()
        self.database = _MemoryDatabase()
        self.config = {"Record": 1}
        self.option = {"Language": "zh_CN"}

    def set_language(self, language: str):
        self.option["Language"] = language


class _IndexScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("index")


class _SettingApp(App[None]):
    def __init__(self, ks: _FakeKS):
        super().__init__()
        self.ks = ks
        self.refresh_count = 0

    async def on_mount(self) -> None:
        self.push_screen(_IndexScreen())
        self.push_screen(SettingScreen(self.ks))

    async def refresh_screen(self) -> None:
        self.refresh_count += 1
        if isinstance(self.screen, SettingScreen):
            self.pop_screen()


def test_setting_bindings() -> None:
    keys = {binding.key for binding in SettingScreen.BINDINGS}
    assert {"q", "b"}.issubset(keys)


def test_save_button_persists_settings() -> None:
    async def scenario():
        ks = _FakeKS()
        app = _SettingApp(ks)

        async with app.run_test() as pilot:
            await pilot.pause()

            app.screen.query_one("#cookie", Input).value = "k=v"
            app.screen.query_one("#record", Checkbox).value = False
            app.screen.query_one("#language", Select).value = "en_US"

            await pilot.click("#save")
            await pilot.pause()

            assert ks.config_obj.read()["cookie"] == "k=v"
            assert ks.database.config_updates[-1] == ("Record", 0)
            assert ks.database.option_updates[-1] == ("Language", "en_US")
            assert ks.option["Language"] == "en_US"
            assert app.refresh_count == 1

    asyncio.run(scenario())


def test_abandon_button_discards_changes() -> None:
    async def scenario():
        ks = _FakeKS()
        app = _SettingApp(ks)

        async with app.run_test() as pilot:
            await pilot.pause()

            app.screen.query_one("#cookie", Input).value = "will_not_save"
            await pilot.click("#abandon")
            await pilot.pause()

            assert ks.config_obj.read()["cookie"] == ""
            assert ks.database.config_updates == []
            assert ks.database.option_updates == []

    asyncio.run(scenario())
