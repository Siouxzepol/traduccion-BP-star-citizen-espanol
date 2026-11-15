#!/usr/bin/env python3
"""Genera una localización LIVE desde la traducción PTU sin mezclar textos cambiados.

Uso:
  python herramientas/generar_global_live.py \
    GLOBAL_PTU GLOBAL_INGLES_LIVE GLOBAL_INGLES_PTU BASELINE_ES_LIVE SALIDA

Las claves cuyo texto inglés difiere entre LIVE y PTU recuperan el valor de la
traducción LIVE de referencia. El resto conserva todas las correcciones comunes.
"""

from __future__ import annotations

from pathlib import Path
import sys


def normalize(key: str) -> str:
    return key[:-2] if key.endswith(",P") else key


def load(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.startswith((";", "[")):
            key, value = line.split("=", 1)
            values[normalize(key)] = value
    return values


def main() -> int:
    if len(sys.argv) != 6:
        raise SystemExit(__doc__)

    source_path, live_en_path, ptu_en_path, baseline_path, output_path = map(
        Path, sys.argv[1:]
    )
    live_en = load(live_en_path)
    ptu_en = load(ptu_en_path)
    baseline = load(baseline_path)
    changed = {
        key
        for key in live_en.keys() & ptu_en.keys()
        if live_en[key] != ptu_en[key]
    }
    missing = sorted(key for key in changed if key not in baseline)
    if missing:
        raise SystemExit(f"Faltan {len(missing)} claves LIVE de referencia: {missing}")

    raw = source_path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    output: list[str] = []
    restored: set[str] = set()
    for line in text.splitlines():
        if "=" in line and not line.startswith((";", "[")):
            raw_key = line.split("=", 1)[0]
            key = normalize(raw_key)
            if key in changed:
                value = baseline[key]
                # Los nombres de objetos se conservan en inglés. Si LIVE aún
                # publica un marcador PH y PTU ya tiene el nombre definitivo,
                # se usa este último sin traducirlo.
                if key.startswith("item_Name"):
                    value = live_en[key]
                    if value.startswith("PH -") and not ptu_en[key].startswith("PH -"):
                        value = ptu_en[key]
                # Son nombres propios de ubicación, no texto descriptivo.
                if key in {
                    "mission_location_nyx_socialstation_002a_0",
                    "Name_PotentialMarokLocation",
                }:
                    value = live_en[key]
                line = f"{raw_key}={value}"
                restored.add(key)
        output.append(line)

    not_written = changed - restored
    if not_written:
        raise SystemExit(f"No se escribieron {len(not_written)} claves: {sorted(not_written)}")

    encoded = (newline.join(output) + newline).encode("utf-8")
    output_path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    print(f"Restauradas para LIVE: {len(restored)}")
    print(f"Salida: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
