from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalScroll, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, RichLog

from ..app import KS
from ..static import PROJECT_NAME
from ..tools import ERROR, INFO, MASTER, PROMPT, WARNING
from ..translation import _
from .loading import Loading

__all__ = ["Index"]


class Index(Screen):
    BINDINGS = [
        Binding(key="Q", action="quit", description=_("退出程序")),
        Binding(key="U", action="update", description=_("检查更新")),
        Binding(key="S", action="settings", description=_("程序设置")),
        Binding(key="A", action="about", description=_("关于项目")),
        Binding(key="D", action="deal", description=_("开始下载")),
        Binding(key="L", action="clear_log", description=_("清空日志")),
    ]

    def __init__(
        self,
        app: KS,
    ):
        super().__init__()
        self.ks = app
        self.url_input = None
        self.logs = None
        self.status = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Label(
                Text(PROJECT_NAME, style=MASTER),
                classes="hero-title",
            ),
            Label(
                Text(_("请输入快手作品链接，按 Enter 或点击按钮开始下载"), style=PROMPT),
                classes="hero-subtitle",
            ),
            Label(
                Text(_("微信公众号：驼铃电商技术团"), style=MASTER),
                classes="hero-tip",
            ),
            classes="section-card",
            id="hero_card",
        )
        yield Input(
            placeholder=_("支持多个链接，使用空格分隔"),
            id="url",
        )
        yield HorizontalScroll(
            Button(_("下载作品文件"), id="deal"),
            Button(_("清空输入框"), id="clear"),
            Button(_("程序设置"), id="settings"),
            Button(_("检查更新"), id="update"),
            Button(_("关于项目"), id="about"),
            classes="horizontal-layout",
        )
        yield HorizontalScroll(
            Button(_("清空日志"), id="clear_log"),
            classes="horizontal-layout",
        )
        yield Label(
            Text(_("当前状态：就绪"), style=INFO),
            id="status",
            classes="status-line",
        )
        yield Label(
            _("运行日志"),
            classes="log-title",
        )
        yield Label(
            _("快捷键：D 下载 | L 清空日志 | S 设置 | U 更新 | A 关于 | Q 退出"),
            classes="info-line",
        )
        yield RichLog(
            markup=True,
            wrap=True,
            auto_scroll=True,
            id="log",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = PROJECT_NAME
        self.url_input = self.query_one("#url", Input)
        self.logs = self.query_one("#log", RichLog)
        self.status = self.query_one("#status", Label)
        self.ks.bind_output(self.logs, mirror_stdout=False)
        self.logs.write(
            Text(_("欢迎使用 KS-Downloader"), style=MASTER),
            scroll_end=True,
        )
        self.logs.write(
            Text("=" * 50, style=PROMPT),
            scroll_end=True,
        )

    def on_unmount(self) -> None:
        self.ks.unbind_output()

    def _set_status(
        self,
        message: str,
        style: str = INFO,
    ) -> None:
        self.status.update(
            Text(
                _("当前状态：{message}").format(message=message),
                style=style,
            )
        )

    def _set_controls_disabled(
        self,
        disabled: bool,
    ) -> None:
        for button_id in (
            "#deal",
            "#clear",
            "#settings",
            "#update",
            "#about",
            "#clear_log",
        ):
            self.query_one(button_id, Button).disabled = disabled
        self.url_input.disabled = disabled

    @on(Button.Pressed, "#deal")
    async def deal_button(self):
        text = self.url_input.value.strip()
        if not text:
            self.logs.write(
                Text(_("未输入任何快手作品链接"), style=WARNING),
                scroll_end=True,
            )
            self._set_status(_("等待输入"), WARNING)
            return
        self.deal()

    @on(Input.Submitted, "#url")
    async def submit_input(self):
        await self.deal_button()

    @on(Button.Pressed, "#clear")
    def clear_button(self):
        self.url_input.value = ""
        self._set_status(_("已清空输入框"), INFO)

    @on(Button.Pressed, "#settings")
    async def settings_button(self):
        await self.action_settings()

    @on(Button.Pressed, "#update")
    async def update_button(self):
        await self.action_update()

    @on(Button.Pressed, "#about")
    async def about_button(self):
        await self.action_about()

    @on(Button.Pressed, "#clear_log")
    def clear_log_button(self):
        self.logs.clear()
        self._set_status(_("日志已清空"), INFO)

    @work(exclusive=True)
    async def deal(self):
        self._set_controls_disabled(True)
        self._set_status(_("正在处理链接"), PROMPT)
        await self.app.push_screen(Loading())
        try:
            result = await self.ks.process_links(
                self.url_input.value,
                True,
            )
        except Exception as error:
            self.logs.write(
                Text(
                    _("处理异常：{error}").format(error=error),
                    style=ERROR,
                ),
                scroll_end=True,
            )
            self.app.notify(
                str(error),
                severity="error",
            )
            self._set_status(_("处理失败"), ERROR)
            return
        finally:
            await self.app.action_back()
            self._set_controls_disabled(False)
        self.app.notify(
            result["message"],
            severity=result["severity"],
        )
        self._set_status(
            result["message"],
            INFO if result["success"] > 0 else WARNING,
        )
        if result["success"] > 0:
            self.url_input.value = ""

    async def action_quit(self) -> None:
        await self.app.action_quit()

    async def action_update(self):
        await self.app.run_action("update")

    async def action_settings(self):
        await self.app.run_action("settings")

    async def action_about(self):
        await self.app.run_action("about")

    async def action_deal(self):
        await self.deal_button()

    async def action_clear_log(self):
        self.clear_log_button()
