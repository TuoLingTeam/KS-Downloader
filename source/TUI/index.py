from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, HorizontalScroll, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, RichLog

from ..app import KS
from ..static import PROJECT_NAME
from ..tools import MASTER, PROMPT, WARNING
from ..translation import _
from .loading import Loading

__all__ = ["Index"]


class Index(Screen):
    BINDINGS = [
        Binding(key="Q", action="quit", description=_("退出程序")),
        Binding(key="U", action="update", description=_("检查更新")),
        Binding(key="S", action="settings", description=_("程序设置")),
        Binding(key="A", action="about", description=_("关于项目")),
    ]

    def __init__(
        self,
        app: KS,
    ):
        super().__init__()
        self.ks = app
        self.url_input = None
        self.logs = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            ScrollableContainer(
                Label(
                    Text(_("微信公众号：驼铃电商技术团"), style=MASTER),
                ),
                Label(
                    Text(_("请输入快手作品链接，然后点击"下载作品文件"按钮"), style=PROMPT),
                    classes="prompt",
                ),
                Input(
                    placeholder=_("多个链接之间使用空格分隔"),
                    id="url",
                ),
                HorizontalScroll(
                    Button(_("下载作品文件"), id="deal", variant="primary"),
                    Button(_("清空输入框"), id="clear"),
                    Button(_("程序设置"), id="settings"),
                    Button(_("检查更新"), id="update"),
                    Button(_("关于项目"), id="about"),
                    classes="horizontal-layout",
                ),
                id="input-section",
            ),
            RichLog(
                markup=True,
                wrap=True,
                auto_scroll=True,
                id="log",
            ),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = PROJECT_NAME
        self.url_input = self.query_one("#url", Input)
        self.logs = self.query_one("#log", RichLog)
        self.ks.bind_output(self.logs, mirror_stdout=False)
        self.logs.write(
            Text(_("欢迎使用 KS-Downloader"), style=MASTER),
            scroll_end=True,
        )

    def on_unmount(self) -> None:
        self.ks.unbind_output()

    @on(Button.Pressed, "#deal")
    async def deal_button(self):
        text = self.url_input.value.strip()
        if not text:
            self.logs.write(
                Text(_("未输入任何快手作品链接"), style=WARNING),
                scroll_end=True,
            )
            return
        self.deal()

    @on(Button.Pressed, "#clear")
    def clear_button(self):
        self.url_input.value = ""

    @on(Button.Pressed, "#settings")
    async def settings_button(self):
        await self.action_settings()

    @on(Button.Pressed, "#update")
    async def update_button(self):
        await self.action_update()

    @on(Button.Pressed, "#about")
    async def about_button(self):
        await self.action_about()

    @work(exclusive=True)
    async def deal(self):
        await self.app.push_screen(Loading())
        try:
            result = await self.ks.process_links(
                self.url_input.value,
                True,
            )
        except Exception as error:
            self.app.notify(
                str(error),
                severity="error",
            )
            return
        finally:
            await self.app.action_back()
        self.app.notify(
            result["message"],
            severity=result["severity"],
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
