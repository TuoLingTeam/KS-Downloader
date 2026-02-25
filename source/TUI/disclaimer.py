from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

from ..app import KS
from ..static import DISCLAIMER_TEXT
from ..translation import _

__all__ = ["Disclaimer"]


class Disclaimer(ModalScreen):
    BINDINGS = [
        Binding(key="Y", action="accept", description=_("接受")),
        Binding(key="N", action="decline", description=_("退出")),
        Binding(key="Q", action="decline", description=_("退出")),
    ]

    def __init__(
        self,
        app: KS,
    ):
        super().__init__()
        self.ks = app

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(_("免责声明"), classes="disclaimer-title"),
            Label(
                _("请先阅读以下内容；接受后方可继续使用程序。"),
                classes="disclaimer-tip",
            ),
            ScrollableContainer(
                Static(
                    _(DISCLAIMER_TEXT),
                    classes="disclaimer-text",
                ),
            ),
            Grid(
                Button(_("接受并继续"), id="accept"),
                Button(_("退出程序"), id="decline"),
                classes="disclaimer-buttons",
            ),
            id="disclaimer",
        )

    @on(Button.Pressed, "#accept")
    async def accept_button(self):
        await self.action_accept()

    @on(Button.Pressed, "#decline")
    async def decline_button(self):
        await self.action_decline()

    async def action_accept(self):
        await self.ks.accept_disclaimer()
        self.dismiss(True)

    async def action_decline(self):
        self.dismiss(False)
