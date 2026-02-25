from __future__ import annotations

import random

from source.translation import _, switch_language


def test_language_switch_integrity_property() -> None:
    expectations = {
        "zh_CN": "设置",
        "en_US": "Settings",
    }

    for idx in range(100):
        language = random.choice(["zh_CN", "en_US"])
        switch_language(language)
        translated = _("设置")
        assert translated == expectations[language]

    # restore default for other tests
    switch_language("zh_CN")
