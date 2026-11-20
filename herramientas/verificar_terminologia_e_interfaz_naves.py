#!/usr/bin/env python3
"""Verifica la terminología de chatarrería y la interfaz compacta de naves."""

from __future__ import annotations

from pathlib import Path
import sys

from aplicar_terminologia_e_interfaz_naves import is_ship_ui, load


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Uso: python herramientas/verificar_terminologia_e_interfaz_naves.py GLOBAL_ES GLOBAL_EN"
        )

    spanish = load(Path(sys.argv[1]))
    english = load(Path(sys.argv[2]))
    errors: list[str] = []

    for key, value in spanish.items():
        if "salvamento" in value.casefold():
            errors.append(f"{key}: conserva la palabra 'salvamento'")
        if is_ship_ui(key) and key in english and value.rstrip() != english[key].rstrip():
            errors.append(f"{key}: el rótulo compacto no coincide con el inglés")

    if errors:
        print(f"ERROR: {len(errors)} problemas de terminología o interfaz:")
        for error in errors[:100]:
            print(f"- {error}")
        return 1

    protected = sum(1 for key in spanish if is_ship_ui(key) and key in english)
    print(
        f"OK: no queda 'salvamento' y {protected} rótulos compactos de nave "
        "se conservan en inglés."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
