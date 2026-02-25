from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Select

from ..app import KS
from ..translation import _

__all__ = ["Setting"]


class Setting(Screen):
    BINDINGS = [
        Binding(key="Q", action="quit", description=_("退出程序")),
        Binding(key="B", action="back", description=_("返回首页")),
    ]

    def __init__(
        self,
        app: KS,
    ):
        super().__init__()
        self.ks = app
        self.record = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Container(
                Label(_("程序语言"), classes="params"),
                Select.from_values(
                    ["zh_CN", "en_US"],
                    allow_blank=False,
                    id="language",
                ),
                Button(_("保存语言设置"), id="save_language", variant="primary"),
                classes="settings-section",
            ),
            Container(
                Label(_("下载记录"), classes="params"),
                Label(
                    "",
                    id="record_status",
                    classes="status",
                ),
                Button(_("切换下载记录开关"), id="toggle_record"),
                classes="settings-section",
            ),
            Container(
                Label(_("Cookie 设置"), classes="params"),
                Button(_("从浏览器读取 Cookie"), id="read_cookie"),
                classes="settings-section",
            ),
            Button(_("返回首页"), id="back", variant="default"),
        )
        yield Footer()

    async def on_mount(self) -> None:
        self.title = _("程序设置")
        options = await self.ks.runtime_options()
        language = options["language"]
        self.record = options["record"]
        self.query_one("#language", Select).value = language
        self._refresh_record_status()

    def _refresh_record_status(self) -> None:
        tip = _("启用") if self.record else _("禁用")
        self.query_one("#record_status", Label).update(
            _("下载记录功能当前状态：{status}").format(status=tip)
        )

    @on(Button.Pressed, "#save_language")
    async def save_language(self):
        language = self.query_one("#language", Select).value
        if isinstance(language, str):
            await self.ks.set_language_option(language)
            self.app.notify(_("修改设置成功！"), severity="information")

    @on(Button.Pressed, "#toggle_record")
    async def toggle_record(self):
        self.record = await self.ks.toggle_record_switch()
        self._refresh_record_status()
        self.app.notify(_("修改设置成功！"), severity="information")

    @on(Button.Pressed, "#read_cookie")
    async def read_cookie(self):
        if await self.ks.read_browser_cookie():
            self.app.notify(_("读取并写入 Cookie 成功！"), severity="information")
        else:
            self.app.notify(_("读取 Cookie 失败"), severity="warning")

    @on(Button.Pressed, "#back")
    async def back_button(self):
        await self.action_back()

    async def action_back(self) -> None:
        await self.app.action_back()

    async def action_quit(self) -> None:
        await self.app.action_quit()
