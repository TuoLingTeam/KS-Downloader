from pathlib import Path


def test_tui_directory_structure_exists() -> None:
    root = Path(__file__).resolve().parents[2]
    expected_files = [
        root / "source" / "TUI" / "__init__.py",
        root / "source" / "TUI" / "app.py",
        root / "source" / "TUI" / "index.py",
        root / "source" / "TUI" / "setting.py",
        root / "source" / "TUI" / "about.py",
        root / "source" / "TUI" / "loading.py",
        root / "source" / "TUI" / "update.py",
        root / "static" / "KS-Downloader.tcss",
    ]
    for file in expected_files:
        assert file.exists(), f"missing: {file}"


def test_requirements_include_tui_dependencies() -> None:
    requirements = Path(__file__).resolve().parents[2] / "requirements.txt"
    content = requirements.read_text(encoding="utf-8")
    assert "textual" in content
    assert "pyperclip" in content
