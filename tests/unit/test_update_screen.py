from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.screen import ModalScreen

from source.TUI.update import UpdateScreen


class _FakeVersion:
    STATUS_CODE = {
        1: "latest-stable",
        2: "latest-dev",
        3: "dev-with-stable",
        4: "upgradable",
    }

    def __init__(self, target: str | None, state: int):
        self.target = target
        self.state = state
        self.compare_calls: list[tuple[str, str, bool]] = []

    async def get_target_version(self):
        return self.target

    def compare_versions(self, current: str, target: str, is_development: bool) -> int:
        self.compare_calls.append((current, target, is_development))
        return self.state


class _FakeKS:
    VERSION_MAJOR = 1
    VERSION_MINOR = 5
    VERSION_BETA = False

    def __init__(self, target: str | None, state: int):
        self.version = _FakeVersion(target, state)


def test_update_screen_type() -> None:
    screen = UpdateScreen(_FakeKS("1.6", 4))
    assert isinstance(screen, ModalScreen)


def test_check_update_returns_error_when_fetch_failed() -> None:
    async def scenario():
        screen = UpdateScreen(_FakeKS(None, 1))
        dismissed = None

        def capture(result):
            nonlocal dismissed
            dismissed = result

        screen.dismiss = capture  # type: ignore[method-assign]
        await screen.check_update()

        assert dismissed is not None
        assert dismissed[0] == "error"
        assert dismissed[1] in ("检测新版本失败", "Failed to check for new version", "")

    asyncio.run(scenario())


def test_check_update_returns_expected_severity_and_message() -> None:
    async def scenario():
        ks = _FakeKS("1.6", 4)
        screen = UpdateScreen(ks)
        dismissed = None

        def capture(result):
            nonlocal dismissed
            dismissed = result

        screen.dismiss = capture  # type: ignore[method-assign]
        await screen.check_update()

        assert dismissed == ("information", "upgradable")
        assert ks.version.compare_calls == [("1.5", "1.6", False)]

    asyncio.run(scenario())
