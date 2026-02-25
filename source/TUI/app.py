from contextlib import suppress
from pathlib import Path

from textual.app import App

from source.app import KS

from .about import AboutScreen
from .index import IndexScreen
from .setting import SettingScreen
from .update import UpdateScreen


class KSDownloaderApp(App[None]):
    CSS_PATH = Path(__file__).resolve().parent.parent.parent.joinpath(
        "static/KS-Downloader.tcss"
    )

    def __init__(self):
        super().__init__()
        self.ks: KS | None = None

    async def __aenter__(self):
        self.ks = KS()
        await self.ks.__aenter__()
        self.ks.config = await self.ks.database.read_config()
        self.ks.option = await self.ks.database.read_option()
        self.ks.set_language(self.ks.option["Language"])
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.ks:
            await self.ks.__aexit__(exc_type, exc_val, exc_tb)
            self.ks = None

    async def on_mount(self) -> None:
        if self.ks is None:
            self.ks = KS()
            await self.ks.__aenter__()
            self.ks.config = await self.ks.database.read_config()
            self.ks.option = await self.ks.database.read_option()
            self.ks.set_language(self.ks.option["Language"])
        self.theme = "nord"
        await self.refresh_screen()

    async def action_settings(self) -> None:
        self.push_screen("setting")

    async def action_update(self) -> None:
        self.push_screen(UpdateScreen(self.ks), self.update_result)

    async def action_about(self) -> None:
        self.push_screen("about")

    async def refresh_screen(self) -> None:
        if self.ks is None:
            return
        with suppress(KeyError):
            self.uninstall_screen("index")
        with suppress(KeyError):
            self.uninstall_screen("setting")
        with suppress(KeyError):
            self.uninstall_screen("about")
        self.install_screen(IndexScreen(self.ks), name="index")
        self.install_screen(SettingScreen(self.ks), name="setting")
        self.install_screen(AboutScreen(), name="about")
        self.switch_screen("index")

    def update_result(self, args: tuple[str, str] | None) -> None:
        if not args:
            return
        severity, message = args
        self.notify(message, severity=severity, timeout=5)

    async def on_unmount(self) -> None:
        # `on_unmount` is triggered when app exits without using context manager.
        if self.ks:
            await self.ks.close()
            self.ks = None
