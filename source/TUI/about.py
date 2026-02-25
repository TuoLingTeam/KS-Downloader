from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label

from source.static import VERSION_BETA, VERSION_MAJOR, VERSION_MINOR
from source.translation import _


class AboutScreen(Screen):
    BINDINGS = [
        Binding("q", "quit", _("退出")),
        Binding("b", "index", _("返回")),
    ]

    def compose(self) -> ComposeResult:
        version = f"{VERSION_MAJOR}.{VERSION_MINOR}.{'beta' if VERSION_BETA else 'stable'}"
        yield Header()
        with ScrollableContainer(classes="vertical-layout"):
            with Container(classes="about-card"):
                yield Label("KS-Downloader", classes="center-title")
                yield Label(
                    _("版本号：{version}").format(version=version),
                    classes="center-text",
                )
                yield Label(_("微信公众号：驼铃电商技术团"), classes="center-text")
                yield Button(_("关闭"), id="close_about", variant="success")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close_about":
            self.close_about()

    def close_about(self) -> None:
        self.app.pop_screen()

    def action_index(self) -> None:
        self.app.pop_screen()
