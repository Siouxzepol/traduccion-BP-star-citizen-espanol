#!/usr/bin/env python3
"""Aplica la revisión humana final específica de LIVE 4.10.200."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
GLOBAL_INI = ROOT / "global-live.ini"

OVERRIDES = {
    # Objetivos que difieren de PTU: se mantienen las macros exactas de LIVE.
    "delivery_dropoff_short": "Entregar ~mission(item) en ~mission(Destination|Target|Address)",
    "delivery_pickup_short": "Recoger ~mission(item) en ~mission(Location)",
    "hauling_deliver_resource_objective": "Entregar ~mission(amount)/~mission(total) SCU de ~mission(item) en ~mission(Destination|Address|ListAll).",
    # Perfiles de reputación revisados; nombres propios sin traducir.
    "Cornerstone_RepUI_Description": '"Construyendo sobre los cimientos de nuestro pasado."\\n\\nCornerstone Developments, una de las constructoras más antiguas del \'verso, se enorgullece de haber sido pionera en la construcción prefabricada de colonias. A la vanguardia de la nueva frontera, levantó algunas de las primeras estructuras de asentamiento en sistemas como Rhetor, Croshaw y Vega. Hoy, sus equipos trabajan por todo el imperio construyendo a demanda edificios prefabricados y estaciones espaciales, además de realizar mantenimiento y reparaciones.',
    "Highpoint_RepUI_Description": "Tras ver cómo los animales invasores deterioraban valiosos ecosistemas de Noble, su planeta natal, Larkin Boden se inspiró en la Ley de Oportunidad Justa y el movimiento ecologista de finales del siglo XXVIII. En 2795 fundó Highpoint Wilderness Specialists para preservar la belleza natural de la UEE mediante el control de fauna. Al principio, la empresa se especializó en eliminar especies invasoras y controlar poblaciones. Desde entonces, ha ampliado su actividad al manejo de animales y a expediciones para observar fauna en su hábitat natural.",
    # Nyx I todavía no es accesible en este LIVE; se traduce solo su descripción.
    "Nyx1_Desc": "[NO ACCESIBLE ACTUALMENTE] Nyx I es un planeta sin núcleo que orbita más cerca del sol del sistema Nyx. Antes se consideraba imposible terraformarlo, pero Nyx I ha sufrido una transformación radical gracias a la nueva tecnología experimental de Genesis Terraforming.",
    # Descripciones completas adelantadas por el catálogo PTU, traducidas para
    # evitar que LIVE muestre bloques en inglés aunque su fuente aún diga PH.
    "item_Desc_hdtc_jacket_01_06_01": "Reducción de daño: 20%\\nCapacidad: 0,4K µSCU\\n\\nElegante, funcional y letal: la línea Bellator encaja tanto en una cena como en un tiroteo. Esta chaqueta ofrece cierta protección gracias al complejo tejido de grafeno en capas de sus hilos. Incluye un alfiler decorativo y un forro interior amplio capaz de ocultar discretamente armas pequeñas y dispositivos.\\n\\nLa edición Tuxedo presenta un negro clásico, solapas de satén negro y pañuelo blanco.",
    "item_Desc_hdtc_pants_01_07_01": "Reducción de daño: 20%\\nCapacidad: 0,4K µSCU\\n\\nElegante, funcional y letal: la línea Bellator encaja tanto en una cena como en un tiroteo. Estos pantalones entallados ofrecen cierta protección gracias al complejo tejido de grafeno en capas de sus hilos.\\n\\nLa edición Tuxedo es negra y lleva la tradicional franja lateral de satén negro.",
    "item_Desc_hdtc_shirt_03_01_01": "Reducción de daño: 20%\\n\\nElegante, funcional y letal: la línea Bellator encaja tanto en una cena como en un tiroteo. Acompañada de una lujosa corbata de seda, esta camisa ofrece cierta protección gracias al grafeno tejido en sus hilos.\\n\\nLa edición Tuxedo combina camisa blanca y pajarita negra.",
    "item_Desc_hdtc_shirt_04_01_01": "Reducción de daño: 20%\\n\\nElegante, funcional y letal: la línea Bellator encaja tanto en una cena como en un tiroteo. Con corbata de seda y chaleco entallado, esta camisa ofrece cierta protección gracias al grafeno tejido en sus hilos.\\n\\nLa edición Tuxedo combina chaleco negro, camisa blanca y pajarita negra.",
    "item_Desc_hdtc_shoes_01_07_01": "Fabricados a mano con cuero de Quasi Grazer de primera calidad, los zapatos Spettro son una incorporación elegante y refinada a cualquier vestuario. Inspirados en el calzado formal humano tradicional, combinan con cualquier conjunto de gala.\\n\\nLa edición Tuxedo luce un negro clásico pulido.",
    "DefenseCon_2956_MTC_Filament_Desc": "Fabricante: Greycat Industrial\\nFunción: Pathfinder\\n\\nGreycat sabe que la seguridad es vital para cualquier operación industrial. El MTC Mobile Tactical Center permite llevar personal y equipo de seguridad allí donde más se necesitan. Es lo bastante ágil para terrenos difíciles y dispone de taquillas para trajes, soportes de armas y almacenamiento para afrontar numerosas incidencias.\\n\\nEl aspecto Filament viste el MTC de gris con detalles negros y amarillos. También es compatible con otros vehículos Greycat de la serie M.",
    # Correcciones de redacción y erratas en aspectos.
    "item_DescSpartan_Paint_IAE2951_Grey_White_Camo": "Personaliza tu Spartan con este aspecto de camuflaje blanco y gris diseñado especialmente para la IAE 2951.",
    "item_DescSpartan_Paint_Sidewinder_Brown": "El aspecto Sidewinder permite que tu Spartan se mimetice con paisajes rocosos y desérticos.",
    # Descripciones nuevas de LIVE 4.10.3 que todavía estaban en inglés.
    "item_Desc_cbd_hat_03_iae2026_01": "Celebra la principal exposición de naves de la UEE con la gorra oficial de la Intergalactic Aerospace Expo 2956. Esta gorra negra luce el logotipo y el año del evento en la parte frontal.",
    "item_Desc_eld_shirt_10_iae2026_01": "Camiseta oficial de la Intergalactic Aerospace Expo 2956. Esta suave y cómoda camiseta de algodón gris oscuro lleva el logotipo de la IAE sobre un fondo azul intenso en la parte frontal, y el nombre y el año del evento en la espalda.",
    "item_Desc_kap_combat_light_arms_02_03_01": "Tipo de objeto: Armadura ligera\nReducción de daño: 20%\nClasificación térmica: -35 / 65 °C\nProtección radiactiva: 26000 REM\nEliminación de radiación: 145,8 REM/s\n\nLa armadura furtiva Geist combina resistencia y tecnología. Está fabricada con seda de carbono de grado militar procedente de los mismos proveedores que protegen a las fuerzas especiales de la UEE. Sus filamentos, finos como cabellos, ocultan las emisiones del usuario y dificultan su detección.\n\nLa edición Epoque combina azul marino y negro con detalles barrocos dorados.",
    "item_Desc_kap_combat_light_core_02_03_01": "Tipo de objeto: Armadura ligera\nReducción de daño: 20%\nCapacidad: 8k µSCU\nClasificación térmica: -35 / 65 °C\nProtección radiactiva: 26000 REM\nEliminación de radiación: 145,8 REM/s\nMochilas: Ligeras\n\nLa armadura furtiva Geist combina resistencia y tecnología. Está fabricada con seda de carbono de grado militar procedente de los mismos proveedores que protegen a las fuerzas especiales de la UEE. Sus filamentos, finos como cabellos, ocultan las emisiones del usuario y dificultan su detección.\n\nLa edición Epoque combina azul marino y negro con detalles barrocos dorados.",
    "item_Desc_kap_combat_light_helmet_02_03_01": "Tipo de objeto: Armadura ligera\nReducción de daño: 20%\nClasificación térmica: -35 / 65 °C\nProtección radiactiva: 26000 REM\nEliminación de radiación: 145,8 REM/s\n\nEl casco Geist está fabricado con seda de carbono de grado militar procedente de los mismos proveedores que protegen a las fuerzas especiales de la UEE. Sus filamentos, finos como cabellos, ocultan las emisiones del usuario y dificultan su detección. El visor admite retículas de realidad aumentada.\n\nLa edición Epoque combina azul marino y negro con detalles barrocos dorados.",
    "item_Desc_vgl_utility_light_backpack_01_06_01": "Tipo de objeto: Mochila ligera\nCapacidad: 75K µSCU\nCompatibilidad de torso: Todos\n\nDiseñada para equipos de primera intervención, la mochila Chiron permite transportar suministros críticos y acceder rápidamente al material médico guardado en su interior.\n\nLa edición Epoque combina azul marino y negro con detalles barrocos dorados.",
    "item_DescAuroraMK2_Paint_Green_Green_Red": "Celebra Luminalia con el aspecto Deck the Hull, que combina los tradicionales colores verde y rojo del popular festival Banu.",
    "item_DescAuroraMK2_Paint_White_Blue_White": "Viste tu nave con un diseño más frío que una ventisca. El aspecto IceBreak combina blanco puro y azul escarchado para ofrecer un estilo llamativo en cualquier estación.",
    "item_Descbanu_melee_05": "Fabricante: Banu\nTipo de objeto: Cuchillo\nClase: Cuerpo a cuerpo\n\nTamaño: N/D\n\nEl cuchillo Kamba presenta una hoja de punta recortada modificada, un hueco dentado para el dedo y una empuñadura enjoyada con ranuras. Su color oscuro y sus incrustaciones doradas proceden del singular proceso de forja de los artesanos Banu.",
    "item_DescCarryable_1H_SQ_Flair_Coin_IAE_BIS_Drake_Corsair_2026": "En honor al Drake Corsair, finalista del Best In Show 2956, esta moneda conmemorativa muestra la nave grabada en el centro y rodeada por un aro azul claro con su nombre y fabricante.",
    "item_DescCarryable_1H_SQ_Flair_Coin_IAE_BIS_Ironclad_Assault_2026": "Una moneda para quienes consideran que el Ironclad Assault, finalista del Best In Show 2956, no tiene rival. Un grabado muy detallado muestra la potencia de la nave, rematada en azul intenso alrededor del borde.",
    "item_DescCarryable_1H_SQ_Flair_Coin_IAE_BIS_Origin_M80_2026": "Esta moneda de colección celebra al M80 como finalista del Best In Show 2956. Su complejo grabado dorado sobre detalles azules representa la nave surcando el espacio.",
    "item_DescCarryable_1H_SQ_Flair_Coin_IAE_BIS_RSI_Perseus_2026": "Esta moneda de colección muestra al Perseus, ganador oficial del Best In Show 2956, grabado a mano con todo detalle. El diseño dorado contrasta con el cosmos azul y negro del fondo.",
    "item_DescCarryable_1H_SQ_Flair_Luminalia_Gift_Card_1_a": "Felicita las fiestas a alguien especial con esta tarjeta. Al abrirla aparece Pico the Penguin sosteniendo una vela y rodeado de regalos para desear una feliz Luminalia.",
    "item_DescCarryable_2H_CY_toy_plushie_penguin_1_c": "Conoce al último miembro de Squadron 42: Starman Pico the Penguin. Puede que Pico tenga más experiencia deslizándose por la nieve que pilotando naves, pero su traje de vuelo azul claro, su casco gris y su mochila le dan aspecto de as.",
    "item_DescCorsair_Paint_Black_White_Gold": "Celebra tu Corsair con el aspecto exclusivo Best In Show 2956, que combina blanco y gris con llamativos detalles dorados.",
    "item_DescDefender_Paint_Green_Green_Red": "Celebra Luminalia con el aspecto Deck the Hull, que combina los tradicionales colores verde y rojo del popular festival Banu.",
    "item_DescDefender_Paint_White_Blue_White": "Viste tu nave con un diseño más frío que una ventisca. El aspecto IceBreak combina blanco puro y azul escarchado para ofrecer un estilo llamativo en cualquier estación.",
    "item_DescFlair_Dashboard_Cockpit_Bot_luminalia_1_a": "Diseñado para colocarse en el salpicadero, este Dashbot reacciona al viaje con numerosas expresiones cómicas. Tanto si se alegra de verte como si juzga tu forma de pilotar, Emoto Dashbot hará el vuelo más divertido.\n\nLa edición Luminalia añade un acabado dorado y motivos de copos de nieve.",
    "item_DescGMNI_smg_ballistic_01_store01": "Fabricante: Gemini\nTipo de objeto: Subfusil\nClase: Balística\n\nCargador: 50\nCadencia: 1100 disparos/min\nAlcance efectivo: 35 m\n\nAccesorios: Cañón (T1), mira (T1), bajo el cañón (T1)\n\nEl C54 de Gemini es un subfusil elegante, ligero y bien equilibrado. Su armazón de polímero y diseño ergonómico son ideales para combates a corta distancia. Dispara munición de 10 mm en modo automático para saturar el objetivo y acabar rápido con cualquier enfrentamiento.\n\nLa edición Epoque combina azul marino y negro con detalles barrocos dorados.",
    "item_Descgrin_salvage_01_lumi01": "Fabricante: Greycat Industrial\nTipo de objeto: Herramienta\nClase: Dispositivo\n\nDepósito: Grande\nCadencia: N/D (haz)\nAlcance efectivo: 5 m\n\nDesguaza y repara con Cambio, una herramienta SRT de doble uso que recoge aleaciones y polímeros de los restos y los convierte en material compuesto reciclado. Puede venderse o usarse para reparaciones rápidas. Cambio SRT ofrece gran velocidad de extracción y una batería de larga duración.\n\nIlumina Luminalia con esta edición Piconalia verde.",
    "item_DescHurricane_Paint_Green_Green_Red": "Celebra Luminalia con el aspecto Deck the Hull, que combina los tradicionales colores verde y rojo del popular festival Banu.",
    "item_DescHurricane_Paint_White_Blue_White": "Viste tu nave con un diseño más frío que una ventisca. El aspecto IceBreak combina blanco puro y azul escarchado para ofrecer un estilo llamativo en cualquier estación.",
    "item_DescIronclad_Paint_Black_White_Gold": "Celebra tu Ironclad Assault con el aspecto exclusivo Best In Show 2956, que combina blanco y gris con llamativos detalles dorados.",
    "item_Descklwe_smg_energy_01_lumi01": "Fabricante: Klaus & Werner\nTipo de objeto: Subfusil\nClase: Láser\n\nBatería: 45\nCadencia: 562,5 disparos/min\nAlcance efectivo: 25 m\n\nAccesorios: Mira (T1), cañón (T1), bajo el cañón (T1)\n\nLa maestría de Klaus & Werner vuelve a destacar en el fiable y letal fusil de energía compacto Lumin V. Su nuevo modo de «ráfaga automática» dispara cinco proyectiles al mantener pulsado el gatillo, combinando la saturación del fuego automático con pausas que permiten reajustar la puntería. Su diseño ofrece poco retroceso y una dispersión reducida.\n\nIlumina Luminalia con Pico the Penguin en el lateral de esta edición Piconalia azul.",
    "item_Descksar_lmg_energy_01_store01": "Decorada en verde intenso con un patrón de damasco en forma de gotas, la edición Derivation garantiza que dejarás huella en el campo de batalla.",
    "item_Descksar_pistol_ballistic_01_lumi01": "Fabricante: Kastak Arms\nTipo de objeto: Pistola\nClase: Balística\n\nCargador: 6\nCadencia: 180 disparos/min\nAlcance efectivo: 100 m\n\nAccesorios: Mira (T1), cañón (T1), bajo el cañón (T1)\n\nLa Coda, conocida como el «cañón de mano» de Kastak Arms, puede terminar un enfrentamiento con un solo proyectil de calibre .50. Su potencia genera un fuerte retroceso y su pequeño cargador favorece los disparos únicos y precisos.\n\nIlumina Luminalia con Pico the Penguin en el lateral de esta edición Piconalia azul.",
    "item_DescM80_Paint_Black_White_Gold": "Celebra tu M80 con el aspecto exclusivo Best In Show 2956, que combina blanco y gris con llamativos detalles dorados.",
    "item_DescMeteor_Paint_Blue_Blue_Gold": "El aspecto Epoque realza el Meteor con su color azul marino y sus atrevidos detalles dorados.",
    "item_DescMoth_Paint_Green_Grey_Blue": "Distingue tu MOTH con el colorido aspecto Braken, que combina verde espuma de mar con detalles grises y azules.",
    "item_DescMoth_Paint_Metal_Grey_Grey": "El acabado metálico y los detalles grises del aspecto Stargazer reflejan la luz de las estrellas sobre el MOTH.",
    "item_DescMoth_Paint_Navy_Grey_Orange": "El aspecto Downrush combina principalmente azul y gris con llamativos detalles naranjas en la mitad trasera del MOTH.",
    "item_DescMoth_Paint_Yellow_Grey_Blue": "El aspecto Skylight, principalmente amarillo con detalles grises y azules, hace que el MOTH resulte más visible.",
    "item_DescPerseus_Paint_beige_beige_beige": "El aspecto Arenosa para el Perseus es principalmente marrón con detalles negros.",
    "item_DescPerseus_Paint_beige_blue_brown": "Tierra y mar se unen en el aspecto Shoreline Camo para el Perseus, con un patrón de camuflaje marrón y azul.",
    "item_DescPerseus_Paint_beige_green_red": "El aspecto Aftermath da al Perseus una base verde realzada con secciones beige y rojas.",
    "item_DescPerseus_Paint_Black_White_Gold": "El aspecto Best In Show 2956 combina una elegante pintura blanca y gris con llamativos remates dorados para celebrar la victoria del Perseus.",
    "item_DescPerseus_Paint_blue_blue_black": "El aspecto Mariner Camo rompe la silueta del Perseus con un patrón de camuflaje en varios tonos de azul y negro.",
    "item_DescPerseus_Paint_grey_grey_orange": "Los detalles naranjas contrastan con los distintos tonos de gris del aspecto Adamantine para el Perseus.",
    "item_DescPlayerDeco_Flair_Aegis_Idris_1_a": "Taketsu Starship Models recrea fielmente el emblemático Aegis Idris para exponerlo en el hangar. Esta maqueta a gran escala destaca el imponente casco, las numerosas torretas y los potentes motores de la Idris-M, una de las fragatas preferidas de la Armada de la UEE.",
    "item_DescRaft_Paint_Green_Green_Red": "Celebra Luminalia con el aspecto Deck the Hull, que combina los tradicionales colores verde y rojo del popular festival Banu.",
    "item_DescRaft_Paint_White_Blue_White": "Viste tu nave con un diseño más frío que una ventisca. El aspecto IceBreak combina blanco puro y azul escarchado para ofrecer un estilo llamativo en cualquier estación.",
    "item_Descsasu_pistol_toy_01_sf01": "Fabricante: Sakura Sun\nTipo de objeto: Pistola de juguete\nClase: Dardos de espuma\n\nCargador: 10\nCadencia: 450 disparos/min\nAlcance efectivo: 35 m\n\nDiviértete con la Sakura Sun WowBlast Desperado. Dispara dardos de espuma a tus amigos o a enemigos imaginarios con estas coloridas pistolas de plástico. WowBlast ofrece diversión para toda la familia en una zona de aterrizaje o durante una larga travesía.\n\nLa edición F7C luce los colores emblemáticos del clásico caza Hornet de Anvil.",
    "item_DescSHLD_RSI_S04_Polaris": "Tipo de objeto: Generador de escudo\nFabricante: Roberts Space Industries\nTamaño: 4\n\nEste generador de escudo de clase capital se diseñó específicamente para el Polaris.",
    # Rótulos breves de interfaz.
    "ItemExpiry_Expiring": "Caduca en",
    "pause_OptionsCrosshairMode_InCombat": "En combate",
    "ShipSelector_BricksIn": "Bloques en:",
    "Debug_Text_Collect": "*WIP* Recoger",
    "Debug_Text_PlantExplosives_Obj_01_Marker": "*WIP* Recoger explosivo",
}

SUBTITLE_OVERRIDES = {
    "< death from explosion >": "< muerte por explosión >",
    "< choked to death >": "< muerte por asfixia >",
    "< scream in fright >": "< grito de miedo >",
    "<Boo (your team screws up)>": "<abucheo (tu equipo falla)>",
    "<humming along to yourself>": "<tararea para sí>",
    "<reaction to gun shot, slight scream, panic breathing>": "<reacciona al disparo, grita levemente y respira con pánico>",
}


def traducir_marcador_modelo(valor: str) -> str:
    patrones = (
        (r"^\(PH\) Model: (.+?) Description$", r"(PH) Descripción de la maqueta: \1"),
        (r"^\(PH\) Box: Model (.+?)(?: Description)?$", r"(PH) Descripción de la caja de la maqueta: \1"),
        (r"^\(PH\) Holographic representation of the (.+)\.$", r"(PH) Representación holográfica de \1."),
    )
    for patron, reemplazo in patrones:
        nuevo = re.sub(patron, reemplazo, valor)
        if nuevo != valor:
            return nuevo
    return valor


def main() -> int:
    raw = GLOBAL_INI.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    output: list[str] = []
    found: set[str] = set()
    placeholders = 0

    for line in text.splitlines():
        if "=" in line and not line.startswith((";", "[")):
            raw_key, value = line.split("=", 1)
            key = raw_key.removesuffix(",P")
            if key in OVERRIDES:
                # global.ini representa los saltos de línea como los dos
                # caracteres "\\n", nunca como líneas físicas nuevas.
                value = OVERRIDES[key].replace("\n", "\\n")
                found.add(key)
            elif key.startswith("item_DescFlair_Model_"):
                nuevo = traducir_marcador_modelo(value)
                placeholders += nuevo != value
                value = nuevo
            value = SUBTITLE_OVERRIDES.get(value, value)
            line = f"{raw_key}={value}"
        output.append(line)

    missing = set(OVERRIDES) - found
    if missing:
        raise SystemExit(f"Claves no encontradas: {sorted(missing)}")

    encoded = (newline.join(output) + newline).encode("utf-8")
    GLOBAL_INI.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    print(f"Revisiones manuales: {len(found)}")
    print(f"Marcadores de modelos traducidos: {placeholders}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
