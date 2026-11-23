#!/usr/bin/env python3
"""Integra y traduce las novedades de PTU 5.0.202.10025.

Este parche sustituye numerosas claves provisionales con sufijo `,P` por sus
claves definitivas, publica nombres reales de objetos y amplía las guías de
recolección y minería con Nyx I. El script migra las claves sin duplicarlas.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re

from aplicar_ptu_5_0_202 import (
    BODY_BY_CLEAN,
    EDITION_BY_CLEAN,
    clean,
    translate_stats,
)
from aplicar_terminologia_e_interfaz_naves import load, normalize


ROOT = Path(__file__).resolve().parents[1]
GLOBAL = ROOT / "global.ini"
OLD_EN = ROOT.parent / "extracciones/ptu-5.0.202.205/Data/Localization/english/global.ini"
NEW_EN = ROOT.parent / "extracciones/ptu-5.0.202.10025/Data/Localization/english/global.ini"


MANUAL_BODY_TRANSLATIONS = {
    "When you can't afford to fumble. Flexible polyweave provides excellent grip plus ablative ceramic demi-gaunt reinforcement and close-fit cuffs.": (
        "Cuando no puedes permitirte un fallo, el tejido polimérico flexible aporta "
        "un agarre excelente, mientras que el refuerzo cerámico ablativo de los "
        "medios guanteletes y los puños ceñidos protegen las manos."
    ),
    "The Volatus Balaclava is a staple for security and military operatives. Designed using strong, breathable, 100% Sol-grown cotton with reinforced polymer fibers embedded into the material, this balaclava serves to both keep you comfortable, as well as obscure your identity.": (
        "El pasamontañas Volatus es una prenda esencial para personal militar y de "
        "seguridad. Está confeccionado con algodón resistente y transpirable, "
        "cultivado íntegramente en Sol y reforzado con fibras poliméricas para "
        "mantener la comodidad y ocultar la identidad."
    ),
    "A well-fitted green digital camo-print hat.": (
        "Una gorra de buen ajuste con estampado de camuflaje digital verde."
    ),
    "The Drifter edition is a dark gray that hides the dirt and wear of the day well.": (
        "La edición Drifter presenta un gris oscuro que disimula bien la suciedad y "
        "el desgaste del día a día."
    ),
    "Kastak Arms brings practicality to the forefront with their Nightlock line. The vest is fitted with tactical pockets across the chest area atop reinforced metal plating on vital areas to ensure you're ready for your next patrol.": (
        "Kastak Arms antepone la funcionalidad con su línea Nightlock. El chaleco "
        "incorpora bolsillos tácticos sobre el pecho y placas metálicas reforzadas "
        "en las zonas vitales para que estés listo para la próxima patrulla."
    ),
    "The Combat Camo edition is green with a dark green camoflage pattern.": (
        "La edición Combat Camo es verde y presenta un patrón de camuflaje verde oscuro."
    ),
    "Luna's Echopark shirt balances comfort and style, with its slim fit high neck collar, quarter zip and color-blocked torso to create a bold silhouette.": (
        "La camisa Echopark de Luna combina comodidad y estilo mediante un corte "
        "entallado, cuello alto, cremallera de un cuarto y torso con bloques de "
        "color que crean una silueta llamativa."
    ),
}

MANUAL_BODY_TRANSLATIONS.update({
    "The Combat Camo edition are dark green with lighter green accents.":
        "La edición Combat Camo combina verde oscuro con detalles verde claro.",
    "The RoughUp edition wears its scrappy character on its bright orange sleeve, while still keeping the wearer comfortable.":
        "La edición RoughUp luce un carácter desenfadado con su llamativo naranja, sin renunciar a la comodidad.",
    "Feel as intimidating as you look with the Patchwork edition, with pops of orange over grey and brown.":
        "La intimidante edición Patchwork añade toques naranjas sobre tonos grises y marrones.",
    "The Drifter edition features brown and burnt orange leather and cloth.":
        "La edición Drifter combina cuero y tela en marrón y naranja quemado.",
    "The Drifter edition features rich browns and leather arm coverings.":
        "La edición Drifter presenta intensos tonos marrones y protecciones de cuero en los brazos.",
    "Inspired by the classic armor worn by elite army units in the early days of the empire, the  Battalion armor is both functional and intimidating. With a thick inner layer reinforced by metal plating over vital areas, this armor allows for a full range of movement while still providing excellent protection.": (
        "Inspirada en las armaduras clásicas de las unidades militares de élite de los primeros tiempos del Imperio, "
        "Battalion es tan funcional como intimidante. Una gruesa capa interior reforzada con placas metálicas sobre "
        "las zonas vitales ofrece una protección excelente sin limitar los movimientos."
    ),
    "The First Legion R3 edition has been modified with the signature red and black coloration of the organization's fiercest warriors.":
        "La edición First Legion R3 luce la característica combinación roja y negra de los guerreros más feroces de la organización.",
    "Reserved for only the most ruthless leaders of the organization, the Tyrant edition boasts polished chrome to help them stand out on the battlefield and inspire the forces that serve under them.":
        "Reservada a los líderes más despiadados de la organización, la edición Tyrant emplea cromo pulido para destacar en el campo de batalla e inspirar a sus tropas.",
    "Inspired by the classic armor worn by elite army units in the early days of the empire, the  Battalion armor is both functional and intimidating. Featuring the unrelating visage of fearless warrior, this helmet has thick plating and anti-glare lenses to make sure nothing slips past your line of sight. Visor is AR crosshair compatible.": (
        "Inspirada en las armaduras clásicas de las unidades militares de élite de los primeros tiempos del Imperio, "
        "Battalion es tan funcional como intimidante. Este casco presenta el rostro implacable de un guerrero sin "
        "miedo, placas gruesas y lentes antirreflejos para que nada escape a tu vista. El visor admite retículas de realidad aumentada."
    ),
    "Strike fear into any unfortunate enough to cross you with the Galea helmet. With a full-coverage skull design and glowing anti-glare lenses, your enemies will be confronting their own mortality before the first bullet is fired. Visor is AR crosshair compatible.": (
        "Infunde miedo a cualquiera que se cruce contigo con el casco Galea. Su diseño integral de calavera y sus "
        "lentes antirreflejos luminosas harán que el enemigo contemple su propia mortalidad antes del primer disparo. "
        "El visor admite retículas de realidad aumentada."
    ),
    "The First Legion RX edition is made of black steel with red lenses, and is found among the higher ranking soldiers in the organization's ranks.":
        "La edición First Legion RX está fabricada en acero negro con lentes rojas y se reserva a los soldados de mayor rango de la organización.",
    "Reserved for only the most ruthless leaders of the organization, the Tyrant edition boasts polished chrome with a bold red crest to help them stand out on the battlefield and inspire the forces that serve under them.":
        "Reservada a los líderes más despiadados, la edición Tyrant combina cromo pulido con una llamativa cresta roja para destacar en el campo de batalla e inspirar a sus tropas.",
    "Endure the most brutal attacks with the DCP heavy armor. This set features easy-swing joints that provide freedom of movement in the heat of battle, and was crafted with a multi-layer shock-absorbing shell that helps its wearer shake off the hardest hits.": (
        "Resiste los ataques más brutales con la armadura pesada DCP. Sus articulaciones de movimiento fluido "
        "mantienen la libertad de acción en pleno combate, mientras que la coraza multicapa absorbe impactos y ayuda a soportar los golpes más duros."
    ),
    "When the battle gets rough, fight rougher with the dark brown and black Resolute edition.":
        "Cuando la batalla se complique, responde con más dureza gracias a la edición Resolute en marrón oscuro y negro.",
    "Show them all who's boss with the eye-catching Cremate edition, with its orange accents over a battle-torn black base.":
        "Deja claro quién manda con la llamativa edición Cremate, cuyos detalles naranjas destacan sobre una base negra marcada por el combate.",
    "When you want to look tough and feel tougher, the Corelight edition has you covered.":
        "Cuando quieras parecer duro y sentirte aún más resistente, la edición Corelight te cubrirá las espaldas.",
    "The First Legion edition sports the dark green and black color palate worn by members of the paramilitary group.":
        "La edición First Legion presenta la combinación verde oscuro y negra que distingue a los miembros del grupo paramilitar.",
    "Revolutionary when first released, the ADP heavy armor system was heralded as the pinnacle of personal protection. Clark Defense Systems' maximalist design provides plenty of attachment points and excellent protection against the elements and enemy fire. CDS refined and reshaped the ADP line over the years, but many still consider the original ADP to be the touchstone of military-grade heavy armor.": (
        "Revolucionario en su lanzamiento, el sistema de armadura pesada ADP fue considerado la cumbre de la "
        "protección personal. El diseño maximalista de Clark Defense Systems ofrece numerosos puntos de anclaje y "
        "una defensa excelente frente al entorno y el fuego enemigo. Aunque CDS ha perfeccionado la línea ADP con los años, muchos siguen considerando el modelo original la referencia en armaduras pesadas militares."
    ),
    "With the Deserter edition, which bears burnt orange highlights over its heavily fortified steel base, you'll be able to bring the world to heel with intimidation alone.":
        "La edición Deserter combina detalles naranja quemado con una base de acero fuertemente reforzada para imponerse mediante la sola intimidación.",
    "Dependable and durable armor never goes out of style. The ORC-mkV from Clark Defense Systems has been a battlefield staple for centuries. This highly regarded medium armor blends composite plating with a special fiber reinforced polymer to provide solid protection and a wide range of movement.": (
        "Una armadura fiable y resistente nunca pasa de moda. ORC-mkV de Clark Defense Systems lleva siglos siendo "
        "un habitual del campo de batalla. Esta reconocida armadura media combina placas compuestas con un polímero "
        "especial reforzado con fibras para ofrecer protección sólida y gran libertad de movimiento."
    ),
    "With silver battle-worn scratchings atop a dark brown base, the Deepwell edition makes you look as tough as you feel.":
        "Con arañazos plateados de combate sobre una base marrón oscura, la edición Deepwell te hará parecer tan duro como te sientes.",
    "The Suresteel edition, which features orange highlights over shiny silver plating, will make sure you are never overlooked.":
        "La edición Suresteel combina detalles naranjas con brillantes placas plateadas para que nunca pases desapercibido.",
    "Maintain your fear factor with the Stratum edition, which layers various light browns over silver battle scratches.":
        "Conserva tu aspecto intimidante con la edición Stratum, que superpone varios marrones claros a arañazos plateados de combate.",
    "The First Legion edition is an army green with a darker green, fragmented digital pattern.":
        "La edición First Legion combina verde militar con un patrón digital fragmentado de verde más oscuro.",
    "The First Legion R1 edition is black with a bright red, fragmented digital pattern.":
        "La edición First Legion R1 es negra y presenta un llamativo patrón digital fragmentado en rojo.",
    "The First Legion's reign of iron is made clear in everything they do, and what they wear is no different. This flight jacket features synthetic leather dyed a militaristic green and is emboldened with the First Legion logo.":
        "El férreo dominio de First Legion se refleja incluso en su ropa. Esta chaqueta de vuelo de cuero sintético teñido en verde militar luce con orgullo el logotipo de First Legion.",
    "This edition is a deep army green.":
        "Esta edición presenta un intenso verde militar.",
    "This edition features dark jet black coloring.":
        "Esta edición presenta un intenso color negro azabache.",
    "The Combat Camo edition features a digital print pattern for when you need to blend into the battlefield.":
        "La edición Combat Camo incorpora un patrón digital para pasar desapercibido en el campo de batalla.",
    "Make a bold statement in this dark brown and orange Rocksteady edition.":
        "Destaca con la edición Rocksteady en marrón oscuro y naranja.",
    "Stay warm and dry against the elements in the Zelena pants and the Bisbee boots. Both made with water-repellent materials and built-in sweat-wicking technology, they'll be your go-to choice for adventures on even the most hostile worlds.":
        "Mantente abrigado y seco con los pantalones Zelena y las botas Bisbee. Sus materiales hidrófugos y la tecnología integrada de evacuación del sudor los convierten en una opción ideal incluso para los mundos más hostiles.",
    "The Combat Camo edition is green with a dark green digital camoflage pattern on the sleeves and color.":
        "La edición Combat Camo es verde y presenta un patrón de camuflaje digital verde oscuro en las mangas y el cuello.",
    "Maintain your mobility with the Lynx combat armor. A high tech polymer weave allows the wearer to withstand enough damage to quickly escape danger. The suit's striking look became famous after being worn by the Seeker in the widely popular \"Fire and Fury\" vids of the mid-2800s.":
        "Conserva la movilidad con la armadura de combate Lynx. Su tejido polimérico de alta tecnología permite resistir suficiente daño para escapar rápidamente del peligro. Su llamativo aspecto se hizo famoso cuando Seeker la utilizó en los populares vídeos «Fire and Fury» de mediados del siglo XXIX.",
    "Strength and speed combine with the new Inquisitor armor set. Strong yet lightweight alloy plating works alongside reinforced polyfiber weaving to save your skin, but not slow you down. When combined with Kastak Arms' intimidating aesthetic, it's easy to see why this medium armor has become infamous across the Empire.":
        "El conjunto Inquisitor combina fuerza y velocidad. Sus placas de aleación, resistentes pero ligeras, trabajan junto al tejido de polifibra reforzada para protegerte sin frenarte. Sumada a la intimidante estética de Kastak Arms, esta armadura media se ha ganado su fama en todo el Imperio.",
    "If you're in need of top-of-the-line protection enhanced with bleeding-edge technology, look no further than the Antium Armor Set. Developed by the award-winning engineering team at Quirinus Tech, the suit is fully enclosed to protect its wearer against hazardous environments and the dangers of the battlefield. Instead of a traditional laminate faceplate, the helmet utilizes a suite of sensors to create an uncompromised field of vision.":
        "Si necesitas protección de primera línea con tecnología de vanguardia, el conjunto Antium es la respuesta. Desarrollado por el premiado equipo de Quirinus Tech, está completamente sellado frente a entornos peligrosos y riesgos de combate. En lugar de una visera laminada tradicional, el casco emplea varios sensores para ofrecer un campo de visión sin concesiones.",
    "Elegant design meets innovation with the Palatino armor from Quirinus Tech. This armor set masterfully mixes reinforced plating with patented new materials that are light-weight and flexible, yet rated to withstand heavy damage allowing the wearer to be fashionable, light on their feet, and able to withstand serious firepower.":
        "La armadura Palatino de Quirinus Tech combina diseño elegante e innovación. Mezcla placas reforzadas con materiales patentados, ligeros y flexibles, pero capaces de soportar daños graves para mantener al usuario ágil, protegido y con estilo.",
    "The First Legion R-1 edition is plated with black steel with deep blood-red accents, made exclusively for the higher ranking soldiers in the organization's ranks.":
        "La edición First Legion R-1 está revestida de acero negro con intensos detalles rojo sangre y se fabrica en exclusiva para los soldados de mayor rango de la organización.",
    "The First Legion RX edition is black with deep blood-red accents, made exclusively for the higher ranking soldiers in the organization's ranks.":
        "La edición First Legion RX es negra con intensos detalles rojo sangre y se fabrica en exclusiva para los soldados de mayor rango de la organización.",
    "The First Legion R1 edition is dark black and made exclusively for the higher ranking soldiers in the organization's ranks.":
        "La edición First Legion R1 luce un negro intenso y se fabrica en exclusiva para los soldados de mayor rango de la organización.",
    "The First Legion R2 edition has bright red highlighting atop a black base, and is most often found on high ranking members of the paramilitary group.":
        "La edición First Legion R2 añade llamativos detalles rojos sobre una base negra y suele verse entre los miembros de mayor rango del grupo paramilitar.",
    "The First Legion R1 edition is plated with black steel with deep blood-red accents, made exclusively for the higher ranking soldiers in the organization's ranks.":
        "La edición First Legion R1 está revestida de acero negro con intensos detalles rojo sangre y se fabrica en exclusiva para los soldados de mayor rango de la organización.",
    "The Char edition keeps its cool by covering you in bold undertones of light grey and dark brown.":
        "La edición Char mantiene la sobriedad con marcados matices gris claro y marrón oscuro.",
    "Put your enemies in their place with the Sharplight edition, which features silver over dark brown and black.":
        "Pon a tus enemigos en su sitio con la edición Sharplight, que combina plata, marrón oscuro y negro.",
    "The Remarque edition makes a strong statement with light brown and tan highlights.":
        "La edición Remarque destaca con detalles marrón claro y tostados.",
    "Whether you're planetside or in vacuum, RSI's MacFlex industrial armor set has your back. Reinforced plating keeps you safe from environmental hazards while the array of pouches keep your tools accessible.":
        "Tanto en la superficie como en el vacío, el conjunto de armadura industrial MacFlex de RSI te protege. Sus placas reforzadas resguardan de los peligros ambientales y sus numerosos bolsillos mantienen las herramientas al alcance.",
    "Adept at surviving firefights in both atmosphere and in space, the Caudillo helmet provides solid head protection while offering the wearer the stylish look of classical armor thanks to its visually striking metal crest.":
        "Preparado para sobrevivir a tiroteos tanto en atmósfera como en el espacio, el casco Caudillo ofrece una protección sólida y el elegante aspecto de una armadura clásica gracias a su llamativa cresta metálica.",
    "Stegman's classic worker's jacket has been a staple of job sites for over seventy years. This duotone pattern is cut from the toughest material meaning you can wear it anywhere, anytime, making it perfect for the job site or on the move.":
        "La clásica chaqueta de trabajo de Stegman's lleva más de setenta años siendo habitual en todo tipo de obras. Su resistente tejido bicolor permite llevarla en cualquier lugar y momento, tanto trabajando como de viaje.",
    "Designed to be an EVA-compliant light combat suit, the Calico set is the perfect armor suit for infiltrators, snipers, thieves, basically anyone who likes to avoid kicking in doors. Built out of a combination of PAB3 armor and a custom helmet, it can help you weather some incoming fire without slowing you down.":
        "Diseñado como traje de combate ligero compatible con EVA, el conjunto Calico es perfecto para infiltrados, francotiradores, ladrones y cualquiera que prefiera no derribar puertas. Combina armadura PAB3 con un casco personalizado para resistir fuego enemigo sin perder velocidad.",
    "This armor was created using repurposed parts from a Caldera armor set to provide the wearer with an extra layer of protection against aggressors and harsh environments.":
        "Esta armadura utiliza piezas reutilizadas de un conjunto Caldera para aportar una capa adicional de protección frente a atacantes y entornos hostiles.",
    "Tehachapi's Harapi leg armor is the epitome of the company's high durability forf low cost mantra. With reinforced padding over the legs' vital arteries and breathable mixed polymer, fight to your heart's content safe in the knowledge that this armor has you covered.":
        "La armadura de piernas Harapi de Tehachapi encarna la filosofía de máxima resistencia a bajo coste. El acolchado reforzado protege las arterias principales y el polímero mixto transpirable permite combatir con confianza.",
    "The First Legion R2 edition is plated with black polymer, made exclusively for the higher ranking soldiers in the paramilitary group.":
        "La edición First Legion R2 está revestida de polímero negro y se fabrica en exclusiva para los soldados de mayor rango del grupo paramilitar.",
    "Fear no frontier while wearing the Aztalan armor. This mixture of armor plating and reinforced fabrics will keep you safe yet swift on your feet. Tehachapi's masterful design gives the armor a subtle yet unmistakable frontier style that also providing ample storage. Suitable for everything from sand dunes to bustling backstreets, the Aztalan is the ideal choice for your next adventure.":
        "No temas ninguna frontera con la armadura Aztalan. Su combinación de placas y tejidos reforzados protege sin restar agilidad. El diseño de Tehachapi aporta un discreto pero inconfundible estilo fronterizo y abundante almacenamiento. Desde dunas hasta callejones abarrotados, Aztalan es una elección ideal para la próxima aventura.",
    "This hard backpack from Virgil, Ltd. makes travel easy. Whether you need a place to carry your weapons or you've decided to bring some extra rations along for a long journey, this backpack was designed to handle any occasion. The interior features a generous, closeable pocket to keep your small items from falling out of place.":
        "Esta mochila rígida de Virgil, Ltd. facilita cualquier viaje. Ofrece espacio para armas, raciones y todo lo necesario para una travesía larga. En su interior, un amplio bolsillo con cierre mantiene los objetos pequeños en su sitio.",
    "The Battalion edition is inspired by the classic gear used by elite army units in the early days of the empire.":
        "La edición Battalion se inspira en el equipo clásico de las unidades militares de élite de los primeros tiempos del Imperio.",
    "The First Legion RX edition features the black and red color palate found exclusively among the First Legion higher-ups.":
        "La edición First Legion RX presenta la combinación negra y roja reservada a los altos mandos de First Legion.",
})


def read_raw(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Devuelve valores por clave normalizada y la grafía real de cada clave."""
    values: dict[str, str] = {}
    raw_keys: dict[str, str] = {}
    last_key: str | None = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line or line.startswith((";", "[")):
            continue
        if "=" not in line:
            if last_key is not None and line.startswith(r"\n"):
                values[last_key] += line
            continue
        raw_key, value = line.split("=", 1)
        key = normalize(raw_key)
        last_key = key
        values[key] = value
        raw_keys[key] = raw_key
    return values, raw_keys


def translate_changed_descriptions(
    old: dict[str, str], new: dict[str, str], current: dict[str, str], changed: set[str]
) -> dict[str, str]:
    def paragraphs(value: str) -> list[str]:
        return re.split(r"\\n[ \t]*\\n", value)

    memory: dict[str, list[str]] = defaultdict(list)
    for key, source in old.items():
        if key in changed or key not in current:
            continue
        source_parts = paragraphs(source)
        target_parts = paragraphs(current[key])
        if len(source_parts) != len(target_parts):
            continue
        for source_part, target_part in zip(source_parts, target_parts):
            if clean(source_part) and clean(source_part) != clean(target_part):
                memory[clean(source_part)].append(target_part)

    def remembered(part: str) -> str | None:
        values = list(dict.fromkeys(memory.get(clean(part), [])))
        return values[0] if len(values) == 1 else None

    translations: dict[str, str] = {}
    unresolved: list[tuple[str, str]] = []
    for key in sorted(changed):
        if not key.startswith(("item_Desc", "vehicle_Desc")):
            continue
        parts: list[str] = []
        failed = False
        for part in paragraphs(new[key]):
            stripped = part.strip()
            if not stripped:
                parts.append("")
                continue
            translated = (
                remembered(stripped)
                or BODY_BY_CLEAN.get(clean(stripped))
                or EDITION_BY_CLEAN.get(clean(stripped))
                or MANUAL_BODY_TRANSLATIONS.get(stripped)
                or translate_stats(stripped)
            )
            if translated is None:
                unresolved.append((key, stripped))
                failed = True
                break
            parts.append(translated)
        if not failed:
            translations[key] = r"\n\n".join(parts)

    if unresolved:
        details = "\n".join(f"{key}: {part}" for key, part in unresolved)
        raise SystemExit(f"Segmentos sin traducción:\n{details}")

    cleanup = (
        ("Core Compatibility: Todas", "Compatibilidad de torso: Todas"),
        ("Core Compatibility: Pesadas", "Compatibilidad de torso: Pesada"),
        ("Core Compatibility: Ligeras", "Compatibilidad de torso: Ligera"),
        ("Mochilas: All", "Mochilas: Todas"),
        ("Mochilas: Light", "Mochilas: Ligeras"),
        ("Mochilas: Medium", "Mochilas: Medias"),
        ("Mochilas: Heavy", "Mochilas: Pesadas"),
        ("Carry Capacidad:", "Capacidad:"),
        ("Tipo de objeto: Battery", "Tipo de objeto: Batería"),
    )
    for key, value in list(translations.items()):
        for source, target in cleanup:
            value = value.replace(source, target)
        translations[key] = value.rstrip()
    return translations


def update_harvestables(current: str) -> str:
    blocks = current.split(r"\n\n")
    if len(blocks) == 26 and all(
        name in current for name in ("GATALA FUNGI", "LUMBORB POD", "POUCHWEED")
    ):
        return current
    if len(blocks) != 23:
        raise SystemExit(f"La guía de recolectables debería tener 23 bloques, no {len(blocks)}")

    gatala = (
        "GATALA FUNGI\\nUn hongo micorrícico que establece una relación simbiótica "
        "con las plantas cercanas. Gatala se conecta con otra flora mediante una "
        "red de raíces que intercambia nutrientes y señales químicas de alerta. "
        "Lo que distingue a este hongo de otras micorrizas es su singular función "
        "coagulante, empleada como mecanismo defensivo para evitar que sus raíces "
        "sean seccionadas. Las investigaciones en curso estudian posibles "
        "aplicaciones de este efecto coagulante en la medicina humana."
        "\\nDónde encontrar: Nyx I"
    )
    lumborb = (
        "LUMBORB POD\\nEstas plantas esféricas crecen en suelos ricos en metales "
        "naturales, que absorben y utilizan para formar sus bulbosas y resistentes "
        "vainas de semillas. Las vainas tienen un tallo débil pero una cabeza "
        "resistente, por lo que se desprenden con facilidad y recorren grandes "
        "distancias, propagándose por las zonas donde terminan asentándose. Debido "
        "a sus propiedades singulares, algunos metalúrgicos investigan posibles "
        "aplicaciones para crear aleaciones mejoradas.\\nDónde encontrar: Nyx I"
    )
    pouchweed = (
        "POUCHWEED\\nSuele encontrarse en las orillas. Pouchweed es una hierba "
        "acuática viscosa y nudosa, muy resistente, que se enreda en la fauna "
        "acuática de paso y viaja así entre distintos entornos. Al filtrar el agua "
        "por su estructura, acumula bacterias ambientales y las convierte en "
        "nutrientes ricos en polifenoles. Los científicos estudian si estos "
        "polifenoles pueden mejorar los procesos de refinado metalúrgico."
        "\\nDónde encontrar: Nyx I"
    )
    bluemoon = blocks[21].replace("Euterpe (Stanton 4c)", "Euterpe (Stanton 4c), Nyx I")
    heart = blocks[4].replace("microTech (Stanton IV)", "microTech (Stanton IV), Nyx I")
    sunset = blocks[9].replace("microTech (Stanton IV)", "microTech (Stanton IV), Nyx I")

    updated = [
        blocks[0], blocks[1], blocks[2], blocks[3], blocks[5], blocks[6],
        blocks[7], blocks[8], blocks[10], blocks[11], blocks[12], blocks[13],
        blocks[14], blocks[15], blocks[16], blocks[17], gatala, lumborb,
        blocks[18], pouchweed, blocks[19], blocks[20], bluemoon, heart,
        blocks[22], sunset,
    ]
    return r"\n\n".join(updated)


def update_mining_guide(current: str) -> str:
    blocks = current.split(r"\n\n")
    insert_after = {
        "Agricium": "MIC-L4",
        "Aluminium": "MIC-L5",
        "Aslarite": "MIC-L4",
        "Beryl": "MIC-L4",
        "Bexalite": "Keeger Belt",
        "Copper": "MIC-L4",
        "Gold": "MIC-L3",
        "Hephaestanite": "Monox",
        "Laranite": "Lyria",
        "Quartz": "Daymar",
        "Sadaryx": None,
        "Savrilium": "Keeger Belt",
        "Tin": "Monox",
        "Titanium": "Magda",
        "Torite": "MIC-L5",
    }
    for mineral, predecessor in insert_after.items():
        title = f"<EM3>{mineral}</EM3>"
        try:
            title_index = blocks.index(title)
        except ValueError as exc:
            raise SystemExit(f"No se encontró {mineral} en la guía minera") from exc
        location_index = next(
            (i for i in range(title_index + 1, min(title_index + 4, len(blocks)))
             if "Dónde encontrarlo:" in blocks[i]),
            None,
        )
        if location_index is None:
            raise SystemExit(f"No se encontró el bloque de ubicaciones de {mineral}")
        lines = blocks[location_index].split(r"\n")
        if "- Nyx I" in lines:
            continue
        if predecessor is None:
            lines.insert(1, "- Nyx I")
        else:
            needle = f"- {predecessor}"
            if needle not in lines:
                raise SystemExit(f"No se encontró {needle} en {mineral}")
            lines.insert(lines.index(needle) + 1, "- Nyx I")
        blocks[location_index] = r"\n".join(lines)
    return r"\n\n".join(blocks)


def main() -> int:
    old, old_raw = read_raw(OLD_EN)
    new, new_raw = read_raw(NEW_EN)
    current, _ = read_raw(GLOBAL)
    changed = (new.keys() - old.keys()) | {
        key for key in new.keys() & old.keys() if new[key] != old[key]
    }
    schema_changed = {
        key for key in new.keys() & old.keys() if new_raw[key] != old_raw[key]
    }
    rewrite = set(changed) | schema_changed | (new.keys() - current.keys())

    translations = translate_changed_descriptions(old, new, current, changed)
    for key in changed:
        if key.startswith(("item_Name", "item_name", "vehicle_Name")):
            translations[key] = new[key]

    translations.update({
        "ContractScope_SolarSystem": "Intrasistema",
        "hmd_OptionsWheelAttachMode": "[Experimental] RV - Menú radial fijo",
        "hmd_OptionsWheelScale": "[Experimental] RV - Escala del menú radial",
        "Starchitect_Location_Archtype_RemoteLocation_0001": new[
            "Starchitect_Location_Archtype_RemoteLocation_0001"
        ],
        "vehicle_room_battle_stations": new["vehicle_room_battle_stations"],
        "Journal_General_Harvestables_Content": update_harvestables(
            current["Journal_General_Harvestables_Content"]
        ),
        "Journal_General_Mining_Compendium_Content": update_mining_guide(
            current["Journal_General_Mining_Compendium_Content"]
        ),
    })

    raw = GLOBAL.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    output: list[str] = []
    emitted: set[str] = set()
    for line in text.splitlines():
        if "=" not in line or line.startswith((";", "[")):
            output.append(line)
            continue
        raw_key, value = line.split("=", 1)
        key = normalize(raw_key)
        if key not in rewrite:
            output.append(line)
            continue
        if key in emitted:
            continue
        target_key = new_raw.get(key, raw_key)
        target_value = translations.get(key, value)
        output.append(f"{target_key}={target_value}")
        emitted.add(key)

    for key in sorted(rewrite - emitted):
        if key not in new_raw:
            continue
        value = translations.get(key, current.get(key, new[key]))
        output.append(f"{new_raw[key]}={value}")
        emitted.add(key)

    missing = rewrite - emitted
    if missing:
        raise SystemExit(f"No se pudieron escribir estas claves: {sorted(missing)}")

    encoded = (newline.join(output) + newline).encode("utf-8")
    GLOBAL.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    print(
        f"PTU 5.0.202.10025: {len(changed)} valores revisados, "
        f"{len(schema_changed)} claves migradas y {len(translations)} traducciones aplicadas."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
