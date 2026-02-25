from typing import Any, Optional, Union

from rich.console import Console
from rich.style import Style
from rich.text import Text, TextType

# import logging
# from rich.logging import RichHandler


MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"
DEBUG = "b dark_orange"


class ColorConsole(Console):
    # LOG_FORMAT = "%(message)s"
    # DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    def __init__(
        self,
        debug_mode: bool = False,
    ):
        super().__init__()
        self._sink = None
        self._mirror_stdout = True
        self.debug = self.init_debug(
            debug_mode,
        )
        # logging.basicConfig(
        #     level=logging.INFO,
        #     format=self.LOG_FORMAT,
        #     datefmt=self.DATE_FORMAT,
        #     handlers=[RichHandler(
        #         show_path=False,
        #         omit_repeated_times=False,
        #     )]
        # )
        # self.log = logging.getLogger("rich")

    def print(
        self,
        *objects: Any,
        style: Optional[Union[str, Style]] = None,
        highlight: Optional[bool] = False,
        **kwargs,
    ) -> None:
        if self._mirror_stdout:
            super().print(
                *objects,
                style=style or GENERAL,
                highlight=highlight,
                **kwargs,
            )
        self._write_sink(
            *objects,
            style=style or GENERAL,
        )

    def input(
        self,
        prompt: TextType = "",
        style: Optional[Union[str, Style]] = None,
        **kwargs,
    ) -> str:
        return super().input(Text(prompt, style=style or PROMPT), **kwargs)

    def set_sink(
        self,
        sink,
        mirror_stdout: bool = False,
    ) -> None:
        self._sink = sink
        self._mirror_stdout = mirror_stdout

    def clear_sink(self) -> None:
        self._sink = None
        self._mirror_stdout = True

    def _write_sink(
        self,
        *objects: Any,
        style: Optional[Union[str, Style]] = None,
    ) -> None:
        if not self._sink:
            return
        message = " ".join(str(i) for i in objects)
        try:
            self._sink.write(
                Text(
                    message,
                    style=style or GENERAL,
                ),
                scroll_end=True,
            )
        except TypeError:
            self._sink.write(
                Text(
                    message,
                    style=style or GENERAL,
                )
            )

    def info(self, message: str):
        self.print(message, style=INFO)
        # self.log.info(message)

    def warning(self, message: str):
        self.print(message, style=WARNING)
        # self.log.warning(message)

    def error(self, message: str):
        self.print(message, style=ERROR)
        # self.log.error(message)

    def init_debug(self, debug_mode: bool):
        def debug(message: str):
            self.print(message, style=DEBUG)
            # self.log.debug(message)

        def empty(*args, **kwargs):
            pass

        return debug if debug_mode else empty
