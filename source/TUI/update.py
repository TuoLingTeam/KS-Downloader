from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Label

from source.translation import _

if TYPE_CHECKING:
    from source.app import KS


class UpdateScreen(ModalScreen[tuple[str, str] | None]):
    def __init__(self, ks: "KS"):
        super().__init__()
        self.ks = ks

    def compose(self) -> ComposeResult:
        with Container(id="update-dialog"):
            yield Label(_("正在检查版本更新..."), classes="center-text")

    async def on_mount(self) -> None:
        await self.check_update()

    async def check_update(self) -> None:
        target = await self.ks.version.get_target_version()
        if not target:
            self.dismiss(("error", _("检测新版本失败")))
            return
        current = f"{self.ks.VERSION_MAJOR}.{self.ks.VERSION_MINOR}"
        state = self.ks.version.compare_versions(
            current,
            target,
            self.ks.VERSION_BETA,
        )
        message = self.ks.version.STATUS_CODE.get(state, _("检测新版本失败"))
        if state == 4:
            severity = "information"
        elif state in (1, 2, 3):
            severity = "warning"
        else:
            severity = "error"
        self.dismiss((severity, message))
