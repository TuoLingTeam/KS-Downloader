from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Link

from ..static import LICENCE, PROJECT_NAME, REPOSITORY, __VERSION__
from ..tools import INFO, MASTER
from ..translation import _

__all__ = ["About"]


class About(Screen):
    BINDINGS = [
        Binding(key="Q", action="quit", description=_("退出程序")),
        Binding(key="U", action="update", description=_("检查更新")),
        Binding(key="B", action="back", description=_("返回首页")),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Label(
                Text(PROJECT_NAME, style=MASTER),
                classes="prompt",
            ),
            Label(
                Text(_("程序版本：{version}").format(version=__VERSION__), style=INFO),
                classes="prompt",
            ),
            Label(
                Text(_("开源协议：{licence}").format(licence=LICENCE), style=INFO),
                classes="prompt",
            ),
            Link(
                REPOSITORY,
                url=REPOSITORY,
                tooltip=_("点击访问"),
            ),
            Button(_("返回首页"), id="back", variant="default"),
            classes="about-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = PROJECT_NAME

    @on(Button.Pressed, "#back")
    async def back_button(self):
        await self.action_back()

    async def action_back(self) -> None:
        await self.app.action_back()

    async def action_quit(self) -> None:
        await self.app.action_quit()

    async def action_update(self):
        await self.app.run_action("update")
