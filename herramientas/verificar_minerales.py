"""Evita etiquetas cruzadas en los minerales minables de Star Citizen.

Uso: python herramientas/verificar_minerales.py
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
GLOBAL_INI = ROOT / "global.ini"

# Los minerales se conservan en inglés deliberadamente: así coinciden con la
# nomenclatura que usan jugadores, guías y terminales del juego.
EXPECTED_MINEABLES = {
    "agricium": "Agricium",
    "aluminium": "Aluminium",
    "aslarite": "Aslarite",
    "beryl": "Beryl",
    "bexalite": "Bexalite",
    "borase": "Borase",
    "copper": "Copper",
    "corundum": "Corundum",
    "gold": "Gold",
    "hephaestanite": "Hephaestanite",
    "ice": "Ice",
    "iron": "Iron",
    "laranite": "Laranite",
    "lindinium": "Lindinium",
    "ouratite": "Ouratite",
    "quantainium": "Quantainium",
    "quartz": "Quartz",
    "riccite": "Riccite",
    "savrillium": "Savrillium",
    "silicon": "Silicon",
    "stileron": "Stileron",
    "taranite": "Taranite",
    "tin": "Tin",
    "titanium": "Titanium",
    "torite": "Torite",
    "tungsten": "Tungsten",
}

# Algunas pantallas, como el gestor de carga, usan estos subtipos en vez de
# la clave mineabletype_primary. Se validan de forma explícita para impedir
# que un mineral herede el texto de una pieza de arma (p. ej., "Mirilla").
EXPECTED_SUBTYPES = {"item_SubTypeIron": "Iron"}


def read_entries(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line or line.startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        entries[key.removesuffix(",P")] = value
    return entries


def main() -> int:
    entries = read_entries(GLOBAL_INI)
    errors: list[str] = []

    for mineral_id, expected_name in EXPECTED_MINEABLES.items():
        key = f"mineabletype_primary_{mineral_id}"
        value = entries.get(key)
        if value is None:
            errors.append(f"Falta {key}")
        elif not re.fullmatch(rf"{re.escape(expected_name)} \(RS \d+\)", value):
            errors.append(f"{key}: {value!r}; se esperaba {expected_name!r} con su RS")

    for key, expected_value in EXPECTED_SUBTYPES.items():
        value = entries.get(key)
        if value != expected_value:
            errors.append(f"{key}: {value!r}; se esperaba {expected_value!r}")

    if errors:
        print("ERROR: se han detectado etiquetas de minerales incorrectas:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print(f"OK: {len(EXPECTED_MINEABLES)} minerales minables y sus subtipos son correctos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
