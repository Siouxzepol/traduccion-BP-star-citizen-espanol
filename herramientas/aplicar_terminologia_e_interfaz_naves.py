#!/usr/bin/env python3
"""Normaliza la terminología y limita el inglés a la interfaz de pilotaje.

Uso:
    python herramientas/aplicar_terminologia_e_interfaz_naves.py GLOBAL_ES GLOBAL_EN
"""

from __future__ import annotations

from pathlib import Path
import sys


SHIP_UI_PREFIXES = (
    "ui_interactor_",
    "vehicle_interactor_",
    "vehicle_room_",
    "vehicle_deck_",
    "vehicle_level_",
    "vehicle_compartment_",
)

SHIP_UI_KEYS = {
    "interaction_open_storage",
    "innerthought_lift_ORIG_890Jump_Hangar",
    "innerthought_ORIG_890Jump_Hangar_Close",
    "innerthought_ORIG_890Jump_Hangar_Open",
    "innerthought_idris_bridge_lift_bridge",
    "innerthought_idris_bridge_lift_main_deck",
}

# Solo estas familias pertenecen a la interfaz compacta que se muestra al
# pilotar: HUD de vuelo/artillería/quantum, MFD y mandos de la cabina. No se
# incluyen ``ui_interactor_`` ni los rótulos de habitaciones, puertas o
# ascensores, que deben permanecer en español.
PILOT_UI_PREFIXES = (
    "flightHUD_",
    "vehicle_gunnery_hud_",
    "quantum_hud_",
    "vehicle_interactor_",
    "mfd_",
    "ui_mfd_",
)


# Correcciones de contexto que una sustitución literal no puede resolver.
# Se aplican a ambas ramas para que LIVE y PTU mantengan la misma terminología.
CONTEXT_OVERRIDES = {
    "mission_location_stanton_0304": "una chatarrería en Hurston",
    "mission_location_stanton_0307": "una chatarrería en Daymar",
    "mission_location_stanton_0310": "una chatarrería en Wala",
    "mission_location_stanton_0428": "una chatarrería en Euterpe",
    "items_commodities_ConstructionMaterialsChunks": "Construction Salvage",
    "vehicle_deck_command": "Cubierta de mando",
    "vehicle_deck_front": "Cubierta delantera",
    "vehicle_deck_lower": "Cubierta inferior",
    "vehicle_deck_lower_cargo": "Cubierta de carga inferior",
    "vehicle_deck_main": "Cubierta principal",
    "vehicle_deck_sub_deck": "Subcubierta",
    "vehicle_deck_upper": "Cubierta superior",
    "vehicle_deck_upper_cargo": "Cubierta de carga superior",
    "vehicle_room_armory": "Armería",
    "vehicle_room_battle_stations": "Puestos de combate",
    "vehicle_room_briefing": "Sala de reuniones",
    "vehicle_room_captain": "Camarote del capitán",
    "vehicle_room_component_access": "Acceso a componentes",
    "vehicle_room_crew": "Camarotes de la tripulación",
    "vehicle_room_drones": "Hangar de drones",
    "vehicle_room_elevator_rear": "Ascensor trasero",
    "vehicle_room_elevator_shaft": "Hueco del ascensor",
    "vehicle_room_escapepods": "Cápsulas de escape",
    "vehicle_room_escaperaft": "Balsa de escape",
    "vehicle_room_guard": "Puesto de guardia",
    "vehicle_room_hottub": "Bañera de hidromasaje",
    "vehicle_room_lower_cargo_bay": "Bodega de carga inferior",
    "vehicle_room_messhall": "Comedor",
    "vehicle_room_operations_deck": "Cubierta de operaciones",
    "vehicle_room_owners_room": "Camarote del propietario",
    "vehicle_room_passenger_quarters": "Camarotes de pasajeros",
    "vehicle_room_passenger_seating": "Asientos de pasajeros",
    "vehicle_room_repair_bay": "Bahía de reparaciones",
    "vehicle_room_salvage": "Estación de desguace",
    "vehicle_room_scanning": "Sala de escaneo",
    "vehicle_room_shooting_range": "Galería de tiro",
    "vehicle_room_tractor_control": "Control del rayo tractor",
    "vehicle_room_turret": "Acceso a la torreta",
    "vehicle_room_vehicle_bay": "Hangar de vehículos",
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
    "item_displayType_Helmet": "Casco",
    "item_displayType_Undersuit": "Undersuit",
    "ui_inventory_filter_category_name_armor_arms": "Brazos",
    "ui_inventory_filter_category_name_armor_core": "Pecho",
    "ui_inventory_filter_category_name_armor_helmets": "Cascos",
    "ui_inventory_filter_category_name_armor_legs": "Piernas",
    "ui_inventory_filter_category_name_clothing_feet": "Calzado",
    "ui_inventory_filter_category_name_clothing_hands": "Guantes",
    "ui_inventory_filter_category_name_clothing_hats": "Sombreros",
    "ui_inventory_filter_category_name_clothing_legs": "Pantalones",
    "ui_inventory_filter_category_name_clothing_torso0": "Camisetas",
    "ui_inventory_filter_category_name_clothing_torso1": "Chaquetas",
    "ui_inventory_filter_category_name_undersuits": "Undersuits",
    "PU_SHIPDEALER2_M_CP_Pitch_ShipNameComment_Nova_IG_001_AnotherBangerFrom": (
        "Otro bombazo de Tumbril: el Nova es una actualización moderna del "
        "tanque de batalla clásico. Puede atacar objetivos terrestres o aéreos, "
        "y el cañón principal es absolutamente ensordecedor. Es impresionante."
    ),
    "interaction_condition_equipArmorArms_wearingArms": (
        "Quítate la armadura de brazos"
    ),
    "item_Desc_hdh_jacket_11": (
        "Capacidad de carga: 1K µSCU\\n\\nLa Sharud es una prenda superior ideal "
        "para mantenerse fresco con tiempo caluroso. Las técnicas de producción "
        "avanzadas permiten a Habidash fabricar un chal ligero pero absorbente "
        "que parece y se siente como algodón natural hilado a mano, pero a una "
        "fracción del coste. Las tres piezas de antebrazo aportan acentos "
        "elegantes y vienen con microchips incrustados que monitorizan la "
        "temperatura corporal y otras constantes vitales."
    ),
    "item_Desc_outlaw_legacy_armor_light_arms_01_04_9tails": (
        "Tipo: armadura ligera\\nReducción de daño: 20 %\\n"
        "Rango térmico: -31 a 61 °C\\nProtección radiológica: 26 000 rem\\n"
        "Tasa de eliminación radiológica: 145,8 rem/s\\n\\nSe trata de una "
        "versión modificada de la armadura de brazos Lynx de Kastak Arms. La "
        "armadura de combate Lynx se diseñó para preservar la movilidad del "
        "usuario. Su tejido, compuesto por un polímero de tecnología punta, "
        "permite soportar los daños iniciales mientras se pone a cubierto con "
        "agilidad. La llamativa armadura saltó a la fama gracias al personaje "
        "Rastreador, que la portaba en la popular serie «Fuego y furia» de "
        "mediados del siglo XXIX."
    ),
    "item_salvageHead_RSI_Salvation_Desc": (
        "Fabricante: Roberts Space Industries\\n"
        "Tipo de objeto: Cabezal de desguace\\n"
        "Tamaño: 1\\n\\n"
        "Capacidad del módulo: 1 (fijo)\\n\\n"
        "Roberts Space Industries diseñó este cabezal de desguace a medida "
        "para la Salvation. Permite recuperar una gran variedad de materiales "
        "con poca dificultad para que el operador pueda centrarse en lo que "
        "más importa."
    ),
    "vehicle_DescARGO_MOTH": (
        "Fabricante: Argo Astronautics\\n"
        "Tipo: Nave chatarrera mediana\\n\\n"
        "Descubre los siglos de experiencia industrial de Argo con la MOTH. "
        "Construida sobre un chasis de eficacia probada, dispone de tres "
        "torretas de desguace y un cargador automático exterior, lo que permite "
        "a una tripulación de cuatro personas desmontar y almacenar chatarra "
        "con gran rapidez."
    ),
    "vehicle_DescRSI_Salvation": (
        "Fabricante: Roberts Space Industries\\n"
        "Tipo: Nave chatarrera\\n\\n"
        "Durante siglos, Roberts Space Industries se ha enorgullecido de fabricar "
        "vehículos que no solo satisfacen las necesidades de los pilotos, sino que "
        "superan sus expectativas. Aunque la RSI Salvation pueda parecer una "
        "sencilla nave chatarrera, cada detalle —desde el brazo de desguace y la "
        "planta de procesamiento de a bordo hasta el práctico almacenamiento "
        "exterior— se ha perfeccionado para que incluso un principiante trabaje "
        "como un experto."
    ),
    "IAE_2956_Fortune_Sunspot_Desc": (
        "Fabricante: MISC\\nEnfoque: Chatarrería\\n\\n"
        "Para quienes quieran llevar su profesión al siguiente nivel, MISC ha "
        "diseñado el Fortune como la mejor nave chatarrera pequeña de su clase. "
        "Equipado con un versátil brazo de desguace y un elevador de carga, está "
        "construido desde cero para convertir la basura en un tesoro.\\n\\n"
        "El fuerte contraste entre el naranja cálido y el negro frío de la "
        "librea Sunspot resalta el perfil distintivo del Fortune."
    ),
    "IAE_2956_MOTH_XXXX_Desc": (
        "Fabricante: Argo Astronautics\\nEnfoque: Chatarrería\\n\\n"
        "Descubre los siglos de experiencia industrial de Argo con el MOTH. "
        "Construido sobre un chasis de eficacia probada, dispone de tres torretas "
        "de desguace y un cargador automático exterior, lo que permite a una "
        "tripulación de cuatro personas desmontar y almacenar chatarra con gran "
        "rapidez.\\n\\nLa librea Stargazer combina un acabado metálico con detalles "
        "grises que reflejan la luz de las estrellas."
    ),
    "IAE_2956_Salvation_Safeguard_Desc": (
        "Fabricante: Roberts Space Industries\\nEnfoque: Chatarrería\\n\\n"
        "Durante siglos, Roberts Space Industries se ha enorgullecido de fabricar "
        "vehículos que superan las expectativas de sus pilotos. Aunque la RSI "
        "Salvation parezca una sencilla nave chatarrera, cada detalle —desde el "
        "brazo de desguace y la planta de procesamiento de a bordo hasta el "
        "almacenamiento exterior— se ha perfeccionado para que incluso un aficionado "
        "trabaje como un experto.\\n\\nLa colorida librea industrial Safeguard para "
        "la Salvation incluye llamativas franjas azules y amarillas."
    ),
    "IAE_2956_Vulture_Longhorn_Desc": (
        "Fabricante: Drake Interplanetary\\nEnfoque: Chatarrería\\n\\n"
        "No respondas ante nadie: elimina al intermediario y deja de lado la "
        "prudencia. Desguaza restos como un profesional y hazte un nombre en el "
        "vacío a los mandos de esta robusta nave chatarrera de Drake "
        "Interplanetary.\\n\\nEl casco negro y naranja quemado de la librea Longhorn, "
        "con ásperos detalles plateados, aporta al Vulture un clásico aspecto "
        "industrial."
    ),
    "roughready_Salvage_XT_VH_desc_001": (
        "Nos ha llegado un dato de primera que podría beneficiarnos a ambos. "
        "Alguien derribó un transporte de XenoThreat cerca de "
        "<EM4>~mission(Location|Address)</EM4>. Debía llevar buena chatarra, porque "
        "un equipo de recuperación de XenoThreat apareció casi de inmediato. Sería "
        "una pena que alguien eliminara a esas naves y reclamara todo para sí.\\n\\n"
        "Tengo colegas interesados, pero los miembros de Rough & Ready atrapados "
        "allí solo parecen tomar partido. Nos vendría mejor una fuerza independiente "
        "que lanzara el ataque sorpresa.\\n\\nTe venderé las coordenadas del pecio. "
        "Elimina a las fuerzas de XenoThreat y después desguázalo. Seguro que "
        "opondrán resistencia, así que ve preparado y considera los daños colaterales "
        "como más material aprovechable.\\n\\n- Humble"
    ),
}


def normalize(key: str) -> str:
    return key.removesuffix(",P")


def load(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    last_key: str | None = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.startswith((";", "[")):
            key, value = line.split("=", 1)
            last_key = normalize(key)
            values[last_key] = value
        elif last_key is not None and line.startswith(r"\n"):
            # Algunos catálogos oficiales de PTU dividen un valor largo en
            # varias líneas físicas. Cada continuación ya conserva el escape
            # literal ``\n``, por lo que basta con concatenarla.
            values[last_key] += line
    return values


def is_ship_ui(key: str) -> bool:
    return key.startswith(SHIP_UI_PREFIXES) or key in SHIP_UI_KEYS


def is_pilot_ui(key: str) -> bool:
    folded = key.casefold()
    return folded.startswith(tuple(prefix.casefold() for prefix in PILOT_UI_PREFIXES))


def normalize_salvage(value: str) -> str:
    value = value.replace("Salvamento", "Chatarrería")
    value = value.replace("salvamento", "chatarrería")

    replacements = (
        ("reclamaciones de chatarrería", "concesiones de chatarrería"),
        ("reclamación de chatarrería", "concesión de chatarrería"),
        ("Naves de chatarrería", "Naves chatarreras"),
        ("naves de chatarrería", "naves chatarreras"),
        ("Nave de chatarrería", "Nave chatarrera"),
        ("nave de chatarrería", "nave chatarrera"),
        ("barcos de chatarrería", "naves chatarreras"),
        ("barco de chatarrería", "nave chatarrera"),
        ("gran nave de chatarrería", "nave chatarrera grande"),
        ("pilotos de chatarrería", "pilotos chatarreros"),
        ("torretas de chatarrería", "torretas de desguace"),
        ("brazo de chatarrería", "brazo de desguace"),
        ("mercancía de chatarrería", "chatarra"),
        ("materiales de chatarrería", "materiales recuperados"),
        ("material de chatarrería", "material recuperado"),
        ("algún chatarrería", "algo de chatarra"),
        ("un chatarrería", "chatarra"),
        ("este chatarrería", "esta chatarra"),
        ("todo ese chatarrería", "toda esa chatarra"),
        ("el chatarrería", "la chatarra"),
        ("chatarrería justo", "chatarrería legal"),
        ("chatarrería esté permitido", "desguace esté permitido"),
        ("chatarrería permitido", "chatarrería permitida"),
        ("Guía del recuperador para la recolección de materiales", "Guía del chatarrero para la recolección de materiales"),
        ("A Guía del chatarrero", "Guía del chatarrero"),
        ("depósito de chatarrería", "chatarrería"),
    )
    for old, new in replacements:
        value = value.replace(old, new)
    return value


def normalize_clothing(key: str, value: str) -> str:
    """Usa términos inequívocos para las capas y piezas de armadura personal."""
    replacements = (
        ("Trajes interiores", "Undersuits"),
        ("trajes interiores", "undersuits"),
        ("Traje interior", "Undersuit"),
        ("traje interior", "undersuit"),
        ("Sototrajes", "Undersuits"),
        ("sototrajes", "undersuits"),
        ("Sototraje", "Undersuit"),
        ("sototraje", "undersuit"),
    )
    for old, new in replacements:
        value = value.replace(old, new)

    # En monos de trabajo, «bracers» describe el ajuste de la manga, no una
    # pieza de armadura independiente.
    value = value.replace("Brazales ajustables", "Puños ajustables")
    value = value.replace("brazales ajustables", "puños ajustables")

    # Los nombres visibles de las piezas usan las mismas partes cortas que los
    # filtros: Pecho, Brazos y Piernas. Las descripciones en prosa no se tocan.
    if key.casefold().startswith("item_") and "name" in key.casefold():
        prefixes = (
            ("Armadura de brazos ", "Brazos "),
            ("Brazales ", "Brazos "),
            ("Coraza ", "Pecho "),
            ("Perneras ", "Piernas "),
            ("Guanteletes ", "Manos "),
        )
        for old, new in prefixes:
            if value.startswith(old):
                value = new + value[len(old) :]
                break

    if any(
        term in value.casefold()
        for term in ("undersuit", "brazos ", "pecho ", "piernas ")
    ):
        value = value.rstrip()

    return value


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)

    spanish_path = Path(sys.argv[1])
    english_path = Path(sys.argv[2])
    if not english_path.is_file():
        raise SystemExit(f"No existe el catálogo inglés: {english_path}")
    english = load(english_path)

    raw = spanish_path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    output: list[str] = []
    terminology_changes = 0
    pilot_ui_changes = 0

    for line in text.splitlines():
        if "=" in line and not line.startswith((";", "[")):
            raw_key, value = line.split("=", 1)
            key = normalize(raw_key)
            if is_pilot_ui(key) and key in english:
                new_value = english[key].rstrip()
                pilot_ui_changes += new_value != value
            elif key in CONTEXT_OVERRIDES:
                new_value = CONTEXT_OVERRIDES[key].rstrip()
                terminology_changes += new_value != value
            else:
                new_value = normalize_clothing(key, normalize_salvage(value))
                if new_value != value:
                    new_value = new_value.rstrip()
                terminology_changes += new_value != value
            line = f"{raw_key}={new_value}"
        output.append(line)

    encoded = (newline.join(output) + newline).encode("utf-8")
    spanish_path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    print(f"Entradas con terminología corregida: {terminology_changes}")
    print(f"Entradas de pilotaje conservadas en inglés: {pilot_ui_changes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
