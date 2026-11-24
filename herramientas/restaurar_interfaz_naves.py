#!/usr/bin/env python3
"""Restaura las traducciones de interfaz de naves desde una revisión conocida.

Uso:
    python herramientas/restaurar_interfaz_naves.py GLOBAL_ES REVISION:RUTA
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from aplicar_terminologia_e_interfaz_naves import is_pilot_ui, is_ship_ui, normalize


ROOT = Path(__file__).resolve().parents[1]


def load_reference(spec: str) -> dict[str, str]:
    raw = subprocess.check_output(["git", "show", spec], cwd=ROOT)
    text = raw.decode("utf-8-sig")
    values: dict[str, str] = {}
    for line in text.splitlines():
        if "=" in line and not line.startswith((";", "[")):
            raw_key, value = line.split("=", 1)
            values[normalize(raw_key)] = value
    return values


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)

    target = Path(sys.argv[1])
    reference = load_reference(sys.argv[2])
    raw = target.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in text else "\n"
    output: list[str] = []
    restored = 0
    missing: list[str] = []

    for line in text.splitlines():
        if "=" in line and not line.startswith((";", "[")):
            raw_key, value = line.split("=", 1)
            key = normalize(raw_key)
            if is_ship_ui(key) and not is_pilot_ui(key):
                if key not in reference:
                    missing.append(key)
                else:
                    restored += reference[key].rstrip() != value.rstrip()
                    line = f"{raw_key}={reference[key].rstrip()}"
        output.append(line)

    if missing:
        print(f"ERROR: faltan {len(missing)} claves en la referencia:")
        for key in missing[:50]:
            print(f"- {key}")
        return 1

    encoded = (newline.join(output) + newline).encode("utf-8")
    target.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    print(f"Rótulos de interfaz restaurados al español: {restored}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
