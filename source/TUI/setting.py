from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Input, Label, Select

from source.translation import _

if TYPE_CHECKING:
    from source.app import KS


class SettingScreen(Screen):
    BINDINGS = [
        Binding("q", "quit", _("退出")),
        Binding("b", "index", _("返回")),
    ]

    def __init__(self, ks: "KS"):
        super().__init__()
        self.ks = ks

    def compose(self) -> ComposeResult:
        data = self.ks.config_obj.read()
        option = self.ks.option or {"Language": "zh_CN"}
        config = self.ks.config or {"Record": 1}
        yield Header()
        with ScrollableContainer(classes="vertical-layout"):
            yield Label(_("Cookie"), classes="center-text")
            yield Input(value=data.get("cookie", ""), id="cookie")
            yield Label(_("下载记录"), classes="center-text")
            yield Checkbox(
                _("启用下载记录"),
                value=bool(config.get("Record", 1)),
                id="record",
            )
            yield Label(_("语言"), classes="center-text")
            yield Select(
                options=[
                    ("简体中文", "zh_CN"),
                    ("English", "en_US"),
                ],
                value=option.get("Language", "zh_CN"),
                id="language",
            )
            with Container(classes="horizontal-layout"):
                yield Button(_("保存配置"), id="save", variant="success")
                yield Button(_("放弃更改"), id="abandon", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        self.app.title = "KS-Downloader"
        self.app.sub_title = _("设置")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            await self.save_settings()
        elif event.button.id == "abandon":
            self.reset()

    async def save_settings(self) -> None:
        cookie = self.query_one("#cookie", Input).value.strip()
        record = 1 if self.query_one("#record", Checkbox).value else 0
        language = self.query_one("#language", Select).value
        if language not in ("zh_CN", "en_US"):
            language = "zh_CN"

        data = self.ks.config_obj.read()
        self.ks.config_obj.write(data | {"cookie": cookie})
        await self.ks.database.update_config_data("Record", int(record))
        await self.ks.database.update_option_data("Language", str(language))
        self.ks.database.record = int(record)
        if self.ks.config is not None:
            self.ks.config["Record"] = int(record)
        if self.ks.option is not None:
            self.ks.option["Language"] = str(language)
        self.ks.set_language(str(language))
        await self.app.refresh_screen()
        self.app.notify(_("配置保存成功"), severity="information")

    def reset(self) -> None:
        self.app.pop_screen()
        self.app.notify(_("已放弃当前更改"), severity="warning")

    def action_index(self) -> None:
        self.app.pop_screen()
