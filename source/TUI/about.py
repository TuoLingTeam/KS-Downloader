from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalScroll, ScrollableContainer
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
                classes="hero-title",
            ),
            Label(
                Text(_("专注于快手作品下载与数据提取"), style=INFO),
                classes="hero-subtitle",
            ),
            classes="section-card",
        )
        yield ScrollableContainer(
            Label(
                Text(_("程序版本：{version}").format(version=__VERSION__), style=INFO),
                classes="params",
            ),
            Label(
                Text(_("开源协议：{licence}").format(licence=LICENCE), style=INFO),
                classes="params",
            ),
            Label(
                _("项目地址"),
                classes="params",
            ),
            Link(
                REPOSITORY,
                url=REPOSITORY,
                tooltip=_("点击访问"),
            ),
            Label(
                _("感谢使用 KS-Downloader。"),
                classes="info-line",
            ),
            HorizontalScroll(
                Button(_("检查更新"), id="update_about"),
                Button(_("返回首页"), id="back"),
                classes="horizontal-layout",
            ),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = PROJECT_NAME

    @on(Button.Pressed, "#back")
    async def back_button(self):
        await self.action_back()

    @on(Button.Pressed, "#update_about")
    async def update_button(self):
        await self.action_update()

    async def action_back(self) -> None:
        await self.app.action_back()

    async def action_quit(self) -> None:
        await self.app.action_quit()

    async def action_update(self):
        await self.app.run_action("update")
