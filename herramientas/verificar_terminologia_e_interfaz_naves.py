#!/usr/bin/env python3
"""Verifica la terminología y separa pilotaje de interiores de nave."""

from __future__ import annotations

from pathlib import Path
import sys

from aplicar_terminologia_e_interfaz_naves import is_pilot_ui, is_ship_ui, load


EXPECTED_BODY_LABELS = {
    "items_commodities_ConstructionMaterialsChunks": "Construction Salvage",
    "itemPort_Armor_Arms": "Brazos",
    "itemPort_Armor_Helmet": "Casco",
    "itemPort_Armor_Legs": "Piernas",
    "itemPort_Armor_Torso": "Pecho",
    "itemPort_Armor_Undersuit": "Undersuit",
    "item_TypeChar_Armor_Arms": "Brazos",
    "item_TypeChar_Armor_Helmet": "Cascos",
    "item_TypeChar_Armor_Legs": "Piernas",
    "item_TypeChar_Armor_Torso": "Pecho",
    "item_TypeChar_Armor_Undersuit": "Undersuits",
    "item_displayType_ArmorArms": "Brazos",
    "item_displayType_ArmorCore": "Pecho",
    "item_displayType_ArmorHands": "Manos",
    "item_displayType_ArmorLegs": "Piernas",
    "item_displayType_Headwear": "Sombreros",
    "item_displayType_Undersuit": "Undersuit",
    "ui_inventory_filter_category_name_armor_arms": "Brazos",
    "ui_inventory_filter_category_name_armor_core": "Pecho",
    "ui_inventory_filter_category_name_armor_helmets": "Cascos",
    "ui_inventory_filter_category_name_armor_legs": "Piernas",
    "ui_inventory_filter_category_name_clothing_legs": "Pantalones",
    "ui_inventory_filter_category_name_undersuits": "Undersuits",
}

EXPECTED_SHIP_UI_SPANISH = {
    "interaction_open_storage": "Abrir almacenamiento",
    "ui_interactor_close_door": "Cerrar puerta",
    "ui_interactor_open_door": "Abrir puerta",
    "ui_interactor_use_door": "Usar puerta",
    "vehicle_room_airlock": "Esclusa",
    "vehicle_deck_command": "Cubierta de mando",
    "vehicle_deck_main": "Cubierta principal",
    "vehicle_deck_upper": "Cubierta superior",
    "vehicle_room_bathroom": "Aseo",
    "vehicle_room_battle_stations": "Puestos de combate",
    "vehicle_room_captain": "Camarote del capitán",
    "vehicle_room_elevator_rear": "Ascensor trasero",
    "vehicle_room_elevator_shaft": "Hueco del ascensor",
    "vehicle_room_engineering": "Ingeniería",
    "vehicle_room_engineering_bottom": "Ingeniería inferior",
    "vehicle_room_engineering_top": "Ingeniería superior",
    "vehicle_room_neck": "Pasillo",
    "vehicle_room_turret": "Acceso a la torreta",
    "vehicle_deck_lower_corridor": "Corredor inferior",
    "vehicle_deck_upper_corridor": "Corredor superior",
}

for _docking_port_number in range(1, 21):
    _docking_port_suffix = f"{_docking_port_number:02d}"
    _docking_port_label = f"Puerto Dock {_docking_port_suffix}"
    EXPECTED_SHIP_UI_SPANISH[
        f"dockingport_{_docking_port_suffix}"
    ] = _docking_port_label
    EXPECTED_SHIP_UI_SPANISH[
        f"ui_interactor_dockingport_{_docking_port_suffix}"
    ] = _docking_port_label


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

    for key, expected in EXPECTED_SHIP_UI_SPANISH.items():
        if spanish.get(key) != expected:
            errors.append(f"{key}: se esperaba {expected!r}, no {spanish.get(key)!r}")

    for key, value in spanish.items():
        if "salvamento" in value.casefold():
            errors.append(f"{key}: conserva la palabra 'salvamento'")
        if "sototraje" in value.casefold():
            errors.append(f"{key}: conserva la palabra 'sototraje'")
        if "traje interior" in value.casefold() or "trajes interiores" in value.casefold():
            errors.append(f"{key}: conserva la traducción de 'undersuit'")
        if "brazales" in value.casefold():
            errors.append(f"{key}: conserva la palabra ambigua 'brazales'")
        if key.casefold().startswith("item_") and "name" in key.casefold():
            if value.startswith(("Armadura de brazos ", "Coraza ", "Perneras ")):
                errors.append(f"{key}: conserva un nombre de parte largo o antiguo")
    pilot_ui_keys = [key for key in spanish if is_pilot_ui(key) and key in english]
    pilot_not_english = [
        key
        for key in pilot_ui_keys
        if spanish[key].rstrip() != english[key].rstrip()
    ]
    for key in pilot_not_english:
        errors.append(f"{key}: la interfaz de pilotaje no conserva el inglés")

    ship_ui_keys = [
        key
        for key in spanish
        if is_ship_ui(key) and not is_pilot_ui(key) and key in english
    ]
    localized = sum(
        spanish[key].rstrip() != english[key].rstrip() for key in ship_ui_keys
    )
    if localized < 600:
        errors.append(
            f"solo {localized} rótulos internos están traducidos; se esperaban al menos 600"
        )

    if errors:
        print(f"ERROR: {len(errors)} problemas de terminología o interfaz:")
        for error in errors[:100]:
            print(f"- {error}")
        return 1

    print(
        f"OK: no quedan 'salvamento', 'sototraje', 'traje interior' ni "
        f"'brazales'; {localized} de {len(ship_ui_keys)} rótulos internos de "
        f"nave están traducidos al español y {len(pilot_ui_keys)} claves del "
        "HUD/MFD/mandos de pilotaje se conservan en inglés."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
