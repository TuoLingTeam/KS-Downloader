from textual import work
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label, LoadingIndicator

from ..app import KS
from ..translation import _

__all__ = ["Update"]


class Update(ModalScreen):
    def __init__(
        self,
        app: KS,
    ):
        super().__init__()
        self.ks = app

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(_("正在检查新版本，请稍等...")),
            LoadingIndicator(),
            classes="loading",
        )

    @work(exclusive=True)
    async def check_update(self) -> None:
        message, __, severity = await self.ks.check_update_status()
        self.dismiss((message, severity))

    def on_mount(self) -> None:
        self.check_update()
