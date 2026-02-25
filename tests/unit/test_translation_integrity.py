from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POT = ROOT / "locale" / "ks.pot"
PO_ZH = ROOT / "locale" / "zh_CN" / "LC_MESSAGES" / "ks.po"
PO_EN = ROOT / "locale" / "en_US" / "LC_MESSAGES" / "ks.po"
MO_ZH = ROOT / "locale" / "zh_CN" / "LC_MESSAGES" / "ks.mo"
MO_EN = ROOT / "locale" / "en_US" / "LC_MESSAGES" / "ks.mo"


REQUIRED_UI_MSGIDS = {
    "退出",
    "返回",
    "设置",
    "更新",
    "关于",
    "保存配置",
    "放弃更改",
    "下载作品文件",
    "读取剪贴板",
    "清空输入框",
}


def _parse_msg_pairs(path: Path) -> dict[str, str]:
    msgid = None
    msgstr = None
    section = None
    result: dict[str, str] = {}

    def decode(value: str) -> str:
        return ast.literal_eval(value)

    def commit():
        nonlocal msgid, msgstr
        if msgid is not None and msgstr is not None:
            result[msgid] = msgstr
        msgid = None
        msgstr = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("msgid "):
            if section == "msgstr":
                commit()
            section = "msgid"
            msgid = decode(line[6:])
            msgstr = ""
            continue
        if line.startswith("msgstr "):
            section = "msgstr"
            msgstr = decode(line[7:])
            continue
        if line.startswith('"'):
            if section == "msgid" and msgid is not None:
                msgid += decode(line)
            elif section == "msgstr" and msgstr is not None:
                msgstr += decode(line)
            continue
        if line == "" and section == "msgstr":
            commit()
            section = None

    if section == "msgstr":
        commit()
    return result


def test_all_msgids_exist_in_po_files() -> None:
    pot_ids = {key for key in _parse_msg_pairs(POT).keys() if key}
    zh_ids = set(_parse_msg_pairs(PO_ZH).keys())
    en_ids = set(_parse_msg_pairs(PO_EN).keys())

    assert pot_ids.issubset(zh_ids)
    assert pot_ids.issubset(en_ids)


def test_required_ui_msgids_have_translations() -> None:
    zh_pairs = _parse_msg_pairs(PO_ZH)
    en_pairs = _parse_msg_pairs(PO_EN)

    for msgid in REQUIRED_UI_MSGIDS:
        assert zh_pairs.get(msgid, "") != ""
        assert en_pairs.get(msgid, "") != ""


def test_mo_files_exist() -> None:
    assert MO_ZH.exists()
    assert MO_EN.exists()
