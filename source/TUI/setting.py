from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalScroll, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Select

from ..app import KS
from ..tools import INFO, WARNING
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
            Label(
                Text(_("程序设置"), style=INFO),
                classes="hero-title",
            ),
            Label(
                _("修改后立即生效，部分设置会写入本地配置文件。"),
                classes="hero-subtitle",
            ),
            classes="section-card",
        )
        yield ScrollableContainer(
            Label(_("语言设置"), classes="params"),
            Select.from_values(
                ["zh_CN", "en_US"],
                allow_blank=False,
                id="language",
            ),
            HorizontalScroll(
                Button(_("保存语言设置"), id="save_language"),
                classes="horizontal-layout",
            ),
            Label(_("下载记录"), classes="params"),
            Label(
                "",
                id="record_status",
                classes="info-line",
            ),
            HorizontalScroll(
                Button(_("切换下载记录开关"), id="toggle_record"),
                classes="horizontal-layout",
            ),
            Label(_("Cookie"), classes="params"),
            Label(
                _("可从浏览器读取并写入当前配置"),
                classes="info-line",
            ),
            HorizontalScroll(
                Button(_("从浏览器读取 Cookie"), id="read_cookie"),
                classes="horizontal-layout",
            ),
            HorizontalScroll(
                Button(_("返回首页"), id="back"),
                classes="horizontal-layout",
            ),
        )
        yield Footer()

    async def on_mount(self) -> None:
        self.title = _("程序设置")
        options = await self.ks.runtime_options()
        self.record = options["record"]
        self.query_one("#language", Select).value = options["language"]
        self._refresh_record_status()

    def _refresh_record_status(self) -> None:
        tip = _("启用") if self.record else _("禁用")
        style = INFO if self.record else WARNING
        self.query_one("#record_status", Label).update(
            Text(
                _("下载记录功能当前状态：{status}").format(status=tip),
                style=style,
            )
        )

    @on(Button.Pressed, "#save_language")
    async def save_language(self):
        language = self.query_one("#language", Select).value
        if isinstance(language, str):
            await self.ks.set_language_option(language)
            self.app.notify(
                _("语言设置已更新"),
                severity="information",
            )

    @on(Button.Pressed, "#toggle_record")
    async def toggle_record(self):
        self.record = await self.ks.toggle_record_switch()
        self._refresh_record_status()
        self.app.notify(
            _("下载记录状态已更新"),
            severity="information",
        )

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
