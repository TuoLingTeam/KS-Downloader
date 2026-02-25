from __future__ import annotations

import asyncio
import random
import string

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
        self.record = 1
        self.language = "zh_CN"

    async def update_config_data(self, name: str, value: int):
        self.record = value

    async def update_option_data(self, name: str, value: str):
        self.language = value


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


class _SettingPropertyApp(App[None]):
    def __init__(self, ks: _FakeKS):
        super().__init__()
        self.ks = ks

    async def on_mount(self) -> None:
        self.push_screen(_IndexScreen())

    async def refresh_screen(self) -> None:
        if isinstance(self.screen, SettingScreen):
            self.pop_screen()


def _random_cookie() -> str:
    chars = string.ascii_letters + string.digits + "=;_"
    return "".join(random.choice(chars) for _ in range(random.randint(1, 32)))


def test_config_save_roundtrip_property() -> None:
    async def scenario():
        ks = _FakeKS()
        app = _SettingPropertyApp(ks)

        async with app.run_test() as pilot:
            await pilot.pause()
            for _ in range(100):
                cookie = _random_cookie()
                record = random.choice([True, False])
                language = random.choice(["zh_CN", "en_US"])

                app.push_screen(SettingScreen(ks))
                await pilot.pause()

                current = app.screen
                assert isinstance(current, SettingScreen)
                current.query_one("#cookie", Input).value = cookie
                current.query_one("#record", Checkbox).value = record
                current.query_one("#language", Select).value = language

                await current.save_settings()
                await pilot.pause()

                saved = ks.config_obj.read()
                assert saved["cookie"] == cookie
                assert ks.config["Record"] == int(record)
                assert ks.option["Language"] == language

    asyncio.run(scenario())
