#!/usr/bin/env python3
"""Restaura en inglés los nombres dinámicos de ubicaciones de Starchitect."""

from __future__ import annotations

import argparse
from pathlib import Path


PREFIXES = (
    "Starchitect_Cluster_",
    "Starchitect_Location_",
    "Starchitect_Sector_",
)


def load_entries(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            entries[key] = value
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("english_global", type=Path)
    parser.add_argument("spanish_global", type=Path)
    args = parser.parse_args()

    english = load_entries(args.english_global)
    protected = {
        key: value for key, value in english.items() if key.startswith(PREFIXES)
    }

    raw = args.spanish_global.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if has_bom else raw.decode("utf-8")
    changed = 0
    seen: set[str] = set()
    output: list[str] = []

    for raw_line in text.splitlines(keepends=True):
        content = raw_line.rstrip("\r\n")
        ending = raw_line[len(content):]
        if "=" not in content:
            output.append(raw_line)
            continue
        key, value = content.split("=", 1)
        if key in protected:
            seen.add(key)
            if value != protected[key]:
                content = f"{key}={protected[key]}"
                changed += 1
        output.append(content + ending)

    missing = sorted(protected.keys() - seen)
    if missing:
        raise SystemExit(
            f"Faltan {len(missing)} claves dinámicas en el catálogo español"
        )

    encoded = "".join(output).encode("utf-8")
    args.spanish_global.write_bytes(
        (b"\xef\xbb\xbf" if has_bom else b"") + encoded
    )
    print(f"Ubicaciones dinámicas protegidas: {len(protected)}")
    print(f"Valores restaurados al inglés: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
