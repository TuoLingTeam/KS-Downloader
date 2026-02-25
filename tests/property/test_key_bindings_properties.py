from __future__ import annotations

import random

import pytest

pytest.importorskip("textual")

from source.TUI.about import AboutScreen
from source.TUI.index import IndexScreen
from source.TUI.setting import SettingScreen


def test_index_shortcuts_are_bound_to_expected_actions() -> None:
    mapping = {binding.key: binding.action for binding in IndexScreen.BINDINGS}
    assert mapping == {
        "q": "quit",
        "u": "update",
        "s": "settings",
        "a": "about",
    }


@pytest.mark.parametrize(
    ("screen", "required"),
    [
        (IndexScreen, {"q", "u", "s", "a"}),
        (SettingScreen, {"q", "b"}),
        (AboutScreen, {"q", "b"}),
    ],
)
def test_defined_shortcuts_have_matching_action_methods(screen, required) -> None:
    mapping = {binding.key: binding.action for binding in screen.BINDINGS}
    assert required.issubset(mapping.keys())

    # Property-style sampling: every sampled key should resolve to an existing action method.
    keys = list(mapping.keys())
    for _ in range(100):
        key = random.choice(keys)
        action = mapping[key]
        method = f"action_{action}"
        assert hasattr(screen, method) or action == "quit"
