#!/usr/bin/env python3
"""Verifica la integración específica de PTU 5.0.202.10025."""

from pathlib import Path
import re

from aplicar_terminologia_e_interfaz_naves import load, normalize


ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent / "extracciones/ptu-5.0.202.205/Data/Localization/english/global.ini"
NEW = ROOT.parent / "extracciones/ptu-5.0.202.10025/Data/Localization/english/global.ini"
SPANISH = ROOT / "global.ini"


def raw_keys(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line and not line.startswith((";", "[")) and "=" in line:
            raw_key = line.split("=", 1)[0]
            result[normalize(raw_key)] = raw_key
    return result


def main() -> int:
    old = load(OLD)
    new = load(NEW)
    spanish = load(SPANISH)
    old_raw = raw_keys(OLD)
    new_raw = raw_keys(NEW)
    spanish_raw = raw_keys(SPANISH)
    changed = sorted(
        (new.keys() - old.keys())
        | {key for key in new.keys() & old.keys() if new[key] != old[key]}
    )
    schema_changed = sorted(
        key for key in new.keys() & old.keys() if new_raw[key] != old_raw[key]
    )
    errors: list[str] = []

    if len(changed) != 215:
        errors.append(f"se esperaban 215 valores modificados, no {len(changed)}")
    if new.keys() - spanish.keys():
        errors.append(f"faltan {len(new.keys() - spanish.keys())} claves del catálogo nuevo")

    for key in schema_changed:
        if spanish_raw.get(key) != new_raw[key]:
            errors.append(f"{key}: conserva la grafía antigua {spanish_raw.get(key)!r}")

    for key in changed:
        value = spanish.get(key)
        if value is None:
            errors.append(f"{key}: falta en global.ini")
            continue
        if key.startswith(("item_Name", "item_name", "vehicle_Name")) and value != new[key]:
            errors.append(f"{key}: el nombre propio no coincide con el inglés")
        if key.startswith(("item_Desc", "vehicle_Desc")):
            if re.search(
                r"(?:Item Type:|Carrying Capacity:|Core Compatibility:|"
                r"When you|The .* edition|This .* shirt|A well-fitted)",
                value,
                re.IGNORECASE,
            ):
                errors.append(f"{key}: conserva texto descriptivo en inglés")
            if re.match(r"^PH ?-?", value, re.IGNORECASE):
                errors.append(f"{key}: conserva un marcador provisional PH")

    mining = spanish.get("Journal_General_Mining_Compendium_Content", "")
    minerals = (
        "Agricium", "Aluminium", "Aslarite", "Beryl", "Bexalite", "Copper",
        "Gold", "Hephaestanite", "Laranite", "Quartz", "Sadaryx", "Savrilium",
        "Tin", "Titanium", "Torite",
    )
    for mineral in minerals:
        marker = f"<EM3>{mineral}</EM3>"
        start = mining.find(marker)
        end = mining.find("<EM3>", start + len(marker))
        block = mining[start:end if end >= 0 else None]
        if start < 0 or "- Nyx I" not in block:
            errors.append(f"guía minera: falta Nyx I para {mineral}")
    if any(f"<EM3>{mineral}</EM3>" not in mining for mineral in minerals):
        errors.append("guía minera: se ha traducido algún nombre de mineral")

    harvest = spanish.get("Journal_General_Harvestables_Content", "")
    for name in ("GATALA FUNGI", "LUMBORB POD", "POUCHWEED"):
        if name not in harvest:
            errors.append(f"guía de recolectables: falta {name}")
    if "Where to Find:" in harvest:
        errors.append("guía de recolectables: conserva 'Where to Find' en inglés")
    if harvest.count("Nyx I") < 6:
        errors.append("guía de recolectables: faltan referencias nuevas a Nyx I")

    expected = {
        "ContractScope_SolarSystem": "Intrasistema",
        "hmd_OptionsWheelAttachMode": "[Experimental] RV - Menú radial fijo",
        "hmd_OptionsWheelScale": "[Experimental] RV - Escala del menú radial",
        "Starchitect_Location_Archtype_RemoteLocation_0001": "Unoccupied Territory",
        "vehicle_room_battle_stations": "Battle Stations",
    }
    for key, value in expected.items():
        if spanish.get(key) != value:
            errors.append(f"{key}: debería ser {value!r}")

    if any("salvamento" in value.casefold() for value in spanish.values()):
        errors.append("el catálogo conserva la terminología 'salvamento'")

    if errors:
        print(f"ERROR: {len(errors)} problemas en PTU 5.0.202.10025:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "OK: PTU 5.0.202.10025 integrada; 215 cambios, claves definitivas, "
        "nombres ingleses y contenido de Nyx I verificados."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
