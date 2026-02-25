from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Label, LoadingIndicator

from source.translation import _


class LoadingScreen(ModalScreen[None]):
    def compose(self) -> ComposeResult:
        with Container(id="loading-dialog"):
            yield LoadingIndicator()
            yield Label(_("正在处理中，请稍候..."), classes="center-text")
