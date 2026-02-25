from pathlib import Path

import pytest


def test_tcss_file_exists() -> None:
    tcss = Path(__file__).resolve().parents[2] / "static" / "KS-Downloader.tcss"
    assert tcss.exists()
    assert tcss.read_text(encoding="utf-8").strip()


def test_tcss_is_parseable() -> None:
    pytest.importorskip("textual")
    stylesheet_module = pytest.importorskip("textual.css.stylesheet")

    tcss = Path(__file__).resolve().parents[2] / "static" / "KS-Downloader.tcss"
    Stylesheet = stylesheet_module.Stylesheet
    stylesheet = Stylesheet()

    if hasattr(stylesheet, "read"):
        stylesheet.read(tcss)
    elif hasattr(stylesheet, "read_all"):
        stylesheet.read_all([tcss])

    if hasattr(stylesheet, "parse"):
        stylesheet.parse()
    elif hasattr(stylesheet, "reparse"):
        stylesheet.reparse()
