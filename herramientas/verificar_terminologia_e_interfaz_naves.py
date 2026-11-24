#!/usr/bin/env python3
"""Verifica la terminología de chatarrería y la interfaz compacta de naves."""

from __future__ import annotations

from pathlib import Path
import sys

from aplicar_terminologia_e_interfaz_naves import is_ship_ui, load


EXPECTED_BODY_LABELS = {
    "items_commodities_ConstructionMaterialsChunks": "Construction Salvage",
    "itemPort_Armor_Arms": "Brazos",
    "itemPort_Armor_Helmet": "Casco",
    "itemPort_Armor_Legs": "Piernas",
    "itemPort_Armor_Torso": "Pecho",
    "itemPort_Armor_Undersuit": "Traje interior",
    "item_TypeChar_Armor_Arms": "Brazos",
    "item_TypeChar_Armor_Helmet": "Cascos",
    "item_TypeChar_Armor_Legs": "Piernas",
    "item_TypeChar_Armor_Torso": "Pecho",
    "item_TypeChar_Armor_Undersuit": "Trajes interiores",
    "item_displayType_ArmorArms": "Brazos",
    "item_displayType_ArmorCore": "Pecho",
    "item_displayType_ArmorHands": "Manos",
    "item_displayType_ArmorLegs": "Piernas",
    "item_displayType_Headwear": "Sombreros",
    "ui_inventory_filter_category_name_armor_arms": "Brazos",
    "ui_inventory_filter_category_name_armor_core": "Pecho",
    "ui_inventory_filter_category_name_armor_helmets": "Cascos",
    "ui_inventory_filter_category_name_armor_legs": "Piernas",
    "ui_inventory_filter_category_name_clothing_legs": "Pantalones",
}


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Uso: python herramientas/verificar_terminologia_e_interfaz_naves.py GLOBAL_ES GLOBAL_EN"
        )

    spanish = load(Path(sys.argv[1]))
    english = load(Path(sys.argv[2]))
    errors: list[str] = []

    for key, expected in EXPECTED_BODY_LABELS.items():
        if spanish.get(key) != expected:
            errors.append(f"{key}: se esperaba {expected!r}, no {spanish.get(key)!r}")

    for key, value in spanish.items():
        if "salvamento" in value.casefold():
            errors.append(f"{key}: conserva la palabra 'salvamento'")
        if "sototraje" in value.casefold():
            errors.append(f"{key}: conserva la palabra 'sototraje'")
        if "brazales" in value.casefold():
            errors.append(f"{key}: conserva la palabra ambigua 'brazales'")
        if key.casefold().startswith("item_") and "name" in key.casefold():
            if value.startswith(("Armadura de brazos ", "Coraza ", "Perneras ")):
                errors.append(f"{key}: conserva un nombre de parte largo o antiguo")
        if is_ship_ui(key) and key in english and value.rstrip() != english[key].rstrip():
            errors.append(f"{key}: el rótulo compacto no coincide con el inglés")

    if errors:
        print(f"ERROR: {len(errors)} problemas de terminología o interfaz:")
        for error in errors[:100]:
            print(f"- {error}")
        return 1

    protected = sum(1 for key in spanish if is_ship_ui(key) and key in english)
    print(
        f"OK: no quedan 'salvamento', 'sototraje' ni 'brazales'; {protected} "
        "rótulos compactos de nave se conservan en inglés."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
