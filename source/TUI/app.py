from pathlib import Path

from textual.app import App

from ..app import KS
from .about import About
from .disclaimer import Disclaimer
from .index import Index
from .setting import Setting
from .update import Update

__all__ = ["KSDownloader"]


class KSDownloader(App):
    CSS_PATH = Path(__file__).with_name("KS-Downloader.tcss")

    def __init__(self):
        super().__init__()
        self.ks: KS | None = None

    async def __aenter__(self):
        self.ks = KS()
        await self.ks.__aenter__()
        await self.ks.bootstrap()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.ks:
            await self.ks.__aexit__(exc_type, exc_value, traceback)

    async def on_mount(self) -> None:
        if self.ks is None:
            raise RuntimeError("KSDownloader must be entered via async context manager")
        self.theme = "nord"
        self.install_screen(Index(self.ks), name="index")
        await self.push_screen("index")
        if await self.ks.needs_disclaimer():
            await self.push_screen(
                Disclaimer(self.ks),
                callback=self._handle_disclaimer,
            )

    def _handle_disclaimer(self, accepted: bool) -> None:
        if not accepted:
            self.exit()

    def update_result(self, args: tuple[str, str]) -> None:
        self.notify(args[0], severity=args[1])

    async def action_settings(self):
        await self.push_screen(
            Setting(self.ks),
        )

    async def action_update(self):
        await self.push_screen(
            Update(self.ks),
            callback=self.update_result,
        )

    async def action_about(self):
        await self.push_screen(
            About(),
        )
