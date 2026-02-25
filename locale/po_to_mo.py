from __future__ import annotations

import ast
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def scan_directory():
    return [
        item.joinpath("LC_MESSAGES/ks.po") for item in ROOT.iterdir() if item.is_dir()
    ]


def generate_map(files: list[Path]):
    return [(i, i.with_suffix(".mo")) for i in files]


def _decode_po_string(value: str) -> str:
    return ast.literal_eval(value)


def _parse_po_file(po_file: Path) -> dict[str, str]:
    messages: dict[str, str] = {}
    section = None
    msgid = ""
    msgstr = ""
    fuzzy = False

    def commit():
        nonlocal msgid, msgstr, fuzzy
        if not fuzzy:
            messages[msgid] = msgstr
        msgid = ""
        msgstr = ""
        fuzzy = False

    for raw in po_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("#,") and "fuzzy" in line:
            fuzzy = True
            continue
        if line.startswith("#"):
            continue
        if line.startswith("msgid "):
            if section == "msgstr":
                commit()
            section = "msgid"
            msgid = _decode_po_string(line[6:])
            continue
        if line.startswith("msgstr "):
            section = "msgstr"
            msgstr = _decode_po_string(line[7:])
            continue
        if line.startswith('"'):
            if section == "msgid":
                msgid += _decode_po_string(line)
            elif section == "msgstr":
                msgstr += _decode_po_string(line)
            continue
        if line == "":
            if section == "msgstr":
                commit()
            section = None

    if section == "msgstr":
        commit()
    return messages


def _write_mo(messages: dict[str, str], mo_file: Path) -> None:
    keys = sorted(messages.keys())
    original = [key.encode("utf-8") + b"\0" for key in keys]
    translated = [messages[key].encode("utf-8") + b"\0" for key in keys]

    count = len(keys)
    header_size = 7 * 4
    original_table_offset = header_size
    translated_table_offset = original_table_offset + count * 8
    data_offset = translated_table_offset + count * 8

    original_table = []
    translated_table = []
    cursor = data_offset
    for item in original:
        original_table.append((len(item) - 1, cursor))
        cursor += len(item)
    for item in translated:
        translated_table.append((len(item) - 1, cursor))
        cursor += len(item)

    output = [
        struct.pack(
            "<Iiiiiii",
            0x950412DE,
            0,
            count,
            original_table_offset,
            translated_table_offset,
            0,
            0,
        )
    ]
    output.extend(struct.pack("<II", length, offset) for length, offset in original_table)
    output.extend(
        struct.pack("<II", length, offset) for length, offset in translated_table
    )
    output.extend(original)
    output.extend(translated)
    mo_file.write_bytes(b"".join(output))


def generate_mo(maps: list[tuple[Path, Path]]) -> None:
    for po_file, mo_file in maps:
        messages = _parse_po_file(po_file)
        _write_mo(messages, mo_file)
        print(f"generated: {mo_file}")


if __name__ == "__main__":
    generate_mo(generate_map(scan_directory()))
