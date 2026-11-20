#!/usr/bin/env python3
"""Verifica la integración específica del parche PTU 5.0.202.205."""

from pathlib import Path
import re

from aplicar_terminologia_e_interfaz_naves import is_ship_ui, load


ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent / "extracciones/ptu-5.0.201.16954/Data/Localization/english/global.ini"
NEW = ROOT.parent / "extracciones/ptu-5.0.202.205/Data/Localization/english/global.ini"
SPANISH = ROOT / "global.ini"

ENGLISH_MARKERS = re.compile(
    r"(?:Manufacturer:|Item Type:|Damage Reduction:|Temp\. Rating:|"
    r"Radiation Protection:|Radiation Scrub Rate:|Carrying Capacity:|"
    r"Core Compatibility:|Rate Of Fire:|Effective Range:|Attachments:|"
    r"Originally designed|This battery for|The Verdict from)",
    re.IGNORECASE,
)


def main() -> int:
    old = load(OLD)
    new = load(NEW)
    spanish = load(SPANISH)
    changed = sorted(
        (new.keys() - old.keys())
        | {key for key in new.keys() & old.keys() if new[key] != old[key]}
    )
    errors: list[str] = []
    source_locked = (
        "item_Name",
        "item_name",
        "vehicle_Name",
        "mission_location_",
        "itemPort_",
        "port_",
    )

    for key in changed:
        value = spanish.get(key)
        if value is None:
            errors.append(f"{key}: falta en global.ini")
            continue
        if key.startswith(source_locked) and value != new[key]:
            errors.append(f"{key}: nombre propio o ubicación alterados")
        if not key.startswith(source_locked) and not is_ship_ui(key):
            if ENGLISH_MARKERS.search(value):
                errors.append(f"{key}: conserva marcadores de descripción en inglés")
            if re.match(r"^PH ?-? Description", value, re.IGNORECASE):
                errors.append(f"{key}: conserva el marcador provisional inglés")
        if "salvamento" in value.casefold():
            errors.append(f"{key}: conserva la terminología 'salvamento'")

    if len(changed) != 541:
        errors.append(f"el parche debería contener 541 cambios, no {len(changed)}")

    if errors:
        print(f"ERROR: {len(errors)} problemas en PTU 5.0.202.205:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "OK: 541 novedades del parche PTU revisadas; nombres, ubicaciones, "
        "descripciones y terminología son coherentes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
