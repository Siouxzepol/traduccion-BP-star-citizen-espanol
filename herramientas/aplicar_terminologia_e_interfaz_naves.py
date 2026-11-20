#!/usr/bin/env python3
"""Normaliza «salvage» y protege en inglés la interfaz compacta de naves.

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


# Correcciones de contexto que una sustitución literal no puede resolver.
# Se aplican a ambas ramas para que LIVE y PTU mantengan la misma terminología.
CONTEXT_OVERRIDES = {
    "mission_location_stanton_0304": "una chatarrería en Hurston",
    "mission_location_stanton_0307": "una chatarrería en Daymar",
    "mission_location_stanton_0310": "una chatarrería en Wala",
    "mission_location_stanton_0428": "una chatarrería en Euterpe",
    "items_commodities_ConstructionMaterialsChunks": "Escombros de construcción",
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
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.startswith((";", "[")):
            key, value = line.split("=", 1)
            values[normalize(key)] = value
    return values


def is_ship_ui(key: str) -> bool:
    return key.startswith(SHIP_UI_PREFIXES) or key in SHIP_UI_KEYS


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


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)

    spanish_path = Path(sys.argv[1])
    english_path = Path(sys.argv[2])
    english = load(english_path)

    raw = spanish_path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    output: list[str] = []
    ship_ui_changes = 0
    terminology_changes = 0

    for line in text.splitlines():
        if "=" in line and not line.startswith((";", "[")):
            raw_key, value = line.split("=", 1)
            key = normalize(raw_key)
            if is_ship_ui(key) and key in english:
                # Los espacios finales del original no tienen valor visual y
                # generan diffs frágiles entre parches.
                new_value = english[key].rstrip()
                ship_ui_changes += new_value != value
            elif key in CONTEXT_OVERRIDES:
                new_value = CONTEXT_OVERRIDES[key].rstrip()
                terminology_changes += new_value != value
            else:
                new_value = normalize_salvage(value)
                terminology_changes += new_value != value
            line = f"{raw_key}={new_value}"
        output.append(line)

    encoded = (newline.join(output) + newline).encode("utf-8")
    spanish_path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    print(f"Interfaz de nave restaurada al inglés: {ship_ui_changes}")
    print(f"Entradas con terminología corregida: {terminology_changes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
