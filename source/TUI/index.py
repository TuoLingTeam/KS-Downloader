from typing import TYPE_CHECKING, Any

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, RichLog

from source.translation import _

from .loading import LoadingScreen

try:
    import pyperclip
except Exception:  # pragma: no cover - fallback when dependency is missing
    class _ClipboardFallback:
        @staticmethod
        def paste() -> str:
            return ""

    pyperclip = _ClipboardFallback()

if TYPE_CHECKING:
    from source.app import KS


class IndexScreen(Screen):
    BINDINGS = [
        Binding("q", "quit", _("退出")),
        Binding("u", "update", _("更新")),
        Binding("s", "settings", _("设置")),
        Binding("a", "about", _("关于")),
    ]

    def __init__(self, ks: "KS"):
        super().__init__()
        self.ks = ks

    def compose(self) -> ComposeResult:
        yield Header()
        with ScrollableContainer(classes="vertical-layout"):
            yield Label(_("微信公众号：驼铃电商技术团"), classes="center-text")
            yield Label(_("请输入快手作品链接"), classes="center-text")
            yield Input(placeholder=_("多个链接之间使用空格分隔"), id="url")
            with Horizontal(classes="horizontal-layout"):
                yield Button(_("下载作品文件"), id="deal", variant="primary")
                yield Button(_("读取剪贴板"), id="paste", variant="default")
                yield Button(_("清空输入框"), id="reset", variant="error")
        yield RichLog(id="tip", wrap=True, markup=False)
        yield Footer()

    def on_mount(self) -> None:
        self.app.title = "KS-Downloader"
        self.app.sub_title = _("主页")
        self.ks.print = self.write_log
        self.write_log(_("欢迎使用 KS-Downloader"))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "deal":
            await self.deal_button()
        elif event.button.id == "paste":
            self.paste_button()
        elif event.button.id == "reset":
            self.reset_button()

    async def deal_button(self) -> None:
        value = self.query_one("#url", Input).value.strip()
        if not value:
            message = _("请输入快手作品链接")
            self.write_log(message, style="yellow")
            self.app.notify(message, severity="warning")
            return
        self.run_worker(self.deal(value), exclusive=True, thread=False)

    def reset_button(self) -> None:
        self.query_one("#url", Input).value = ""
        self.app.notify(_("输入框已清空"), severity="information")

    def paste_button(self) -> None:
        text = pyperclip.paste().strip()
        if not text:
            self.app.notify(_("剪贴板为空"), severity="warning")
            return
        self.query_one("#url", Input).value = text
        self.app.notify(_("已读取剪贴板内容"), severity="information")

    async def deal(self, value: str) -> None:
        await self.app.push_screen(LoadingScreen())
        try:
            await self.ks.detail(value)
            self.app.notify(_("处理完成"), severity="information")
        except Exception as exc:  # pragma: no cover - defensive guard
            self.write_log(str(exc), style="red")
            self.app.notify(str(exc), severity="error")
        finally:
            self.app.pop_screen()

    def write_log(
        self,
        *objects: Any,
        style: str | None = None,
        **_: Any,
    ) -> None:
        text = " ".join(str(item) for item in objects) if objects else ""
        if style:
            self.query_one("#tip", RichLog).write(Text(text, style=style))
        else:
            self.query_one("#tip", RichLog).write(text)

    def action_quit(self) -> None:
        self.app.exit()

    async def action_update(self) -> None:
        await self.app.action_update()

    async def action_settings(self) -> None:
        await self.app.action_settings()

    async def action_about(self) -> None:
        await self.app.action_about()
