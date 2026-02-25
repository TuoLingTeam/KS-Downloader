from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

from ..app import KS
from ..static import DISCLAIMER_TEXT
from ..translation import _

__all__ = ["Disclaimer"]


class Disclaimer(ModalScreen):
    def __init__(
        self,
        app: KS,
    ):
        super().__init__()
        self.ks = app

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(_("免责声明"), classes="params"),
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
    async def accept(self):
        await self.ks.accept_disclaimer()
        self.dismiss(True)

    @on(Button.Pressed, "#decline")
    async def decline(self):
        self.dismiss(False)
