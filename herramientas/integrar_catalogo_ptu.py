#!/usr/bin/env python3
"""Añade claves nuevas de un catálogo PTU sin romper la compatibilidad con LIVE.

Prioridad para el valor incorporado:
1. Traducción oficial española cuando difiere del inglés.
2. Traducción comunitaria inequívoca de un texto inglés idéntico ya existente.
3. Texto inglés como respaldo pendiente de revisión.

No elimina claves antiguas ni modifica traducciones existentes.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path


SOURCE_REPLACEMENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "CB_URWG_G_Cornerstone_PowerOn-Relay_5Location_VH_Desc_001": (
        ("<EM>five</EM4>", "<EM4>five</EM4>"),
    ),
    "Local_CourierSingle_Desc_011,P": (
        ("<EM4>~mission(Owner)<EM4>", "<EM4>~mission(Owner)</EM4>"),
    ),
    "Local_DeliverySingle_Desc_004": (
        ("~mission(Destination|Target|Address)</EM4", "~mission(Destination|Target|Address)</EM4>"),
    ),
    "Local_KillSingle_Desc_003": (
        ("~mission(Location|Target|Address)<EM4>", "~mission(Location|Target|Address)</EM4>"),
    ),
    "Local_KillSingle_Desc_004": (
        ("~mission(Location|Address)<EM4>", "~mission(Location|Address)</EM4>"),
    ),
    "Local_KillSingle_Desc_005": (
        ("~mission(Location|Address)<EM4>", "~mission(Location|Address)</EM4>"),
    ),
    "Local_KillSingle_Desc_009": (
        ("~mission(Location|Name)<EM4>", "~mission(Location|Name)</EM4>"),
    ),
    "Local_RecoverSingle_Desc_006": (
        ("~mission(Location|Address)<EM4>", "~mission(Location|Address)</EM4>"),
    ),
    "Local_ResourceGathering_GroundVehicleMining_LowQuantity_Desc_001": (
        ("~mission(Destination|Address)<EM4>", "~mission(Destination|Address)</EM4>"),
    ),
    "Local_ResourceGathering_GroundVehicleMining_LowQuantity_Desc_002": (
        ("<~EM4>", "</EM4>"),
    ),
}


def read_entries(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        if not raw_line or raw_line.startswith((";", "[")) or "=" not in raw_line:
            continue
        key, value = raw_line.split("=", 1)
        entries[key] = value
    return entries


def normalized_key(key: str) -> str:
    return key.removesuffix(",P")


def repair_source_value(key: str, value: str) -> str:
    for old, new in SOURCE_REPLACEMENTS.get(key, ()):
        value = value.replace(old, new)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("old_english", type=Path)
    parser.add_argument("new_english", type=Path)
    parser.add_argument("official_spanish", type=Path)
    parser.add_argument("community_spanish", type=Path)
    args = parser.parse_args()

    old_english = read_entries(args.old_english)
    new_english = read_entries(args.new_english)
    official_spanish = read_entries(args.official_spanish)
    community_spanish = read_entries(args.community_spanish)
    community_normalized_keys = {normalized_key(key) for key in community_spanish}

    memory: dict[str, set[str]] = defaultdict(set)
    for key, english_value in old_english.items():
        if key in community_spanish:
            memory[english_value].add(community_spanish[key])

    additions: list[tuple[str, str]] = []
    official_count = 0
    memory_count = 0
    fallback_count = 0

    for key, english_value in new_english.items():
        if normalized_key(key) in community_normalized_keys:
            continue

        english_value = repair_source_value(key, english_value)

        official_value = official_spanish.get(key)
        remembered_values = memory.get(english_value, set())
        if official_value is not None and official_value != english_value:
            value = official_value
            official_count += 1
        elif len(remembered_values) == 1:
            value = next(iter(remembered_values))
            memory_count += 1
        else:
            value = english_value
            fallback_count += 1
        additions.append((key, value.rstrip(" \t")))

    original_bytes = args.community_spanish.read_bytes()
    has_bom = original_bytes.startswith(b"\xef\xbb\xbf")
    text = original_bytes[3:].decode("utf-8") if has_bom else original_bytes.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    if text and not text.endswith(("\n", "\r")):
        text += newline
    text += "".join(f"{key}={value}{newline}" for key, value in additions)
    encoded = text.encode("utf-8")
    args.community_spanish.write_bytes((b"\xef\xbb\xbf" if has_bom else b"") + encoded)

    print(f"Añadidas: {len(additions)}")
    print(f"Traducción oficial: {official_count}")
    print(f"Memoria exacta: {memory_count}")
    print(f"Respaldo inglés pendiente: {fallback_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
