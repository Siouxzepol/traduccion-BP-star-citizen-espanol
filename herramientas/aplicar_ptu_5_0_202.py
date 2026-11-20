#!/usr/bin/env python3
"""Integra y traduce las novedades de PTU 5.0.202.205.

El script es deliberadamente estricto: si una descripción nueva no puede
traducirse mediante memoria, una variante base o una revisión humana, termina
con error en vez de publicar texto inglés por accidente.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re

from aplicar_terminologia_e_interfaz_naves import load, normalize


ROOT = Path(__file__).resolve().parents[1]
GLOBAL = ROOT / "global.ini"
OLD_EN = ROOT.parent / "extracciones/ptu-5.0.201.16954/Data/Localization/english/global.ini"
NEW_EN = ROOT.parent / "extracciones/ptu-5.0.202.205/Data/Localization/english/global.ini"


OVERRIDES = {
    "Frontend_PU_Version": "Alpha 5.0",
    "Local_KillSingle_Desc_006": (
        "<EM4>~mission(TargetName)</EM4> me lo quitó todo y me obligó a mirar. "
        "\\n\\nEse cabrón está aquí: <EM4>~mission(Location|Name)</EM4>."
        "\\n\\nQuiero sangre. Me la merezco.\\n\\n<EM4>~mission(Owner|First)</EM4>"
    ),
    "EckhartSecurity_MultiElminateAll_VE_Desc_001": (
        "ECKHART SECURITY, LLC.\\nCONTRATOS Y DESPACHO\\n\\n"
        "TIPO DE CONTRATO: repeler hostiles\\nCÓDIGO DE APROBACIÓN = RF-32\\n\\n"
        "PARA PROCESAMIENTO INMEDIATO\\n\\nUnos forajidos se han infiltrado "
        "en las propiedades de nuestro cliente situadas en "
        "<EM4>~mission(Location|Address)</EM4>. Debes limpiar el emplazamiento "
        "de fuerzas hostiles antes de que causen daños permanentes.\\n\\n"
        "Este contrato no es negociable.\\n\\nEste mensaje puede contener "
        "información confidencial, exclusiva, privilegiada o privada. La "
        "información está destinada a la persona o entidad indicada anteriormente."
    ),
    "item_desc_hackingchip_001": (
        "AVISO DE RETIRADA: Hurston Dynamics y los demás organismos de gobierno "
        "de Stanton han declarado que esta criptoclave supone un grave riesgo de "
        "seguridad. Para retirar de la circulación este peligroso dispositivo, se "
        "ofrece una recompensa por entregarlo en la oficina de la TDD de Lorville."
    ),
    "item_desc_hackingchip_004": (
        "AVISO DE RETIRADA: ArcCorp y los demás organismos de gobierno de Stanton "
        "han declarado que esta criptoclave supone un grave riesgo de seguridad. "
        "Para retirar de la circulación este peligroso dispositivo, se ofrece una "
        "recompensa por entregarlo en la oficina de la TDD de Area18."
    ),
    "item_desc_hackingchip_005": (
        "AVISO DE RETIRADA: Crusader Industries y los demás organismos de gobierno "
        "de Stanton han declarado que esta criptoclave supone un grave riesgo de "
        "seguridad. Para retirar de la circulación este peligroso dispositivo, se "
        "ofrece una recompensa por entregarlo en la oficina de la TDD de Orison."
    ),
    "item_desc_hackingchip_006": (
        "AVISO DE RETIRADA: microTech y los demás organismos de gobierno de Stanton "
        "han declarado que esta criptoclave supone un grave riesgo de seguridad. "
        "Para retirar de la circulación este peligroso dispositivo, se ofrece una "
        "recompensa por entregarlo en la oficina de la TDD de New Babbage."
    ),
    "pause_OptionsGameTelemetryEnabled": "Telemetría del juego",
    "pause_OptionsGameTelemetryEnabledDesc": (
        "Envía datos del juego en tiempo real a dispositivos y aplicaciones "
        "externos. Al activarlo se inicia el servidor de servicios locales con el "
        "acceso indicado arriba; al desactivarlo se detiene."
    ),
    "pause_OptionsLocalServicesAccess": "Acceso a servicios locales",
    "pause_OptionsLocalServicesAccessDesc": (
        "Indica qué equipos pueden conectarse a servicios locales como la "
        "telemetría. «Solo local» acepta conexiones de este equipo. «Externo» "
        "también permite equipos de tu red, que podrán leer datos del juego y "
        "activar acciones como abrir puertas o eyectar. Cambiarlo reinicia el "
        "servidor y desconecta las aplicaciones conectadas."
    ),
    "pause_OptionsLocalServicesAccess_External": "Externo",
    "pause_OptionsLocalServicesAccess_LocalOnly": "Solo local",
    "ui_hmd_theater_screen_move": "[Experimental] RV - Mover pantalla de cine (mantener)",
    "ui_hmd_theater_screen_move_desc": (
        "Mientras mantengas pulsado, la pantalla de cine se moverá frente a ti. "
        "Permanecerá ahí al soltar."
    ),
    "item_DescARMR_Vehicle": "Blindaje del casco",
    "item_Desc_Carryable_2H_SQ_CollectorMaterial_002": (
        "Esto ser prueba de metamaterial hecho por Wikelo. Creo que ayudar a que "
        "cosas vayan más rápido. Dos últimas pruebas no tan buenas, pero quizá esta funcionar."
    ),
    "item_Desc_Carryable_2H_SQ_CollectorMaterial_003": (
        "Tengo nuevo metamaterial para probar. Este ser muy fuerte, pero también "
        "doblarse. Puede romperse. ¡Puede que no!"
    ),
    "item_Desc_Carryable_2H_SQ_CollectorMaterial_004": (
        "Esta ser nueva prueba de metamaterial diseñado por Wikelo. Última prueba "
        "demasiado pesada, así que esta ser más ligera."
    ),
    "item_Desc_Carryable_2H_SQ_CollectorMaterial_005": (
        "Esta prueba de metamaterial ser nuevo diseño de Wikelo. Intentar que "
        "material no haga daño al tocar. Wikelo aprender lección por las malas."
    ),
    "item_Desc_Carryable_2H_SQ_CollectorMaterial_006": (
        "Esta ser nueva prueba de metamaterial diseñado por Wikelo. Intentar que "
        "no se derrita con mucho calor. Será bueno para naves y para cocinar."
    ),
    "item_Desc_Carryable_2H_SQ_CollectorMaterial_007": (
        "Wikelo hacer nuevo metamaterial para probar. Tener buen presentimiento. "
        "Wikelo aprender del fracaso, así que haber aprendido mucho."
    ),
    "item_Desc_Carryable_2H_SQ_CollectorMaterial_008": (
        "Metamaterial ser nuevo y necesitar pruebas. Diseño ser de Wikelo. Si "
        "prueba salir bien, mucha gente querer material. ¡Wikelo hacerse muy rico "
        "y fabricar más cosas!"
    ),
    "TheCollector_Recipes_Title_IroncladAssault": "Ironclad luchar mejor",
    "TheCollector_Recipes_Title_IroncladBase": "Ironclad trabajar más",
    "TheCollector_Recipes_Title_M80": "M80 merecer número mayor",
    "TheCollector_Recipes_Title_Pitbull": "Pitbull no ladrar",
    "TheCollector_Recipes_Title_Starlite": "Starlite brillar más",
    "TheCollector_Recipes_Title_Tiburon": "¿Tiburon? ¿Tú querer?",
    "TheCollector_Recipes_Desc_IroncladAssault": (
        "Ironclad ser buena nave. Assault luchar muy duro. Wikelo saber hacer que "
        "luche más duro. Wikelo muy bueno en trabajo. Traerme lo que quiero y "
        "plano poder intercambiarse."
    ),
    "TheCollector_Recipes_Desc_IroncladBase": (
        "Ironclad ser buena nave. Pero incluso buena nave poder ser mejor. Wikelo "
        "saber cómo. Traer lo que Wikelo quiere e intercambiar plano de Ironclad mejorado."
    ),
    "TheCollector_Recipes_Desc_M80": (
        "Origin hacer buen trabajo con M80, pero Wikelo poder mejorar. Quizá M82 o "
        "M86. Hacer silenciosa y buena para escabullirse. Tú deber probar. Traerme "
        "intercambio y plano ser tuyo."
    ),
    "TheCollector_Recipes_Desc_Pitbull": (
        "Wikelo conocer pitbull una vez. Muy ruidoso, incluso para oídos Banu. "
        "Siempre ladrar. Cuando Wikelo conocer Drake Pitbull pensar en hacer que "
        "no ladre. Ahora tener más sigilo. Poder intercambiar plano de nave."
    ),
    "TheCollector_Recipes_Desc_Starlite": (
        "Cuando no haber combustible, MISC Starlite traer más. Eso ser muy bueno. "
        "Gran nave heroica, ¿verdad? Wikelo hacer que ayude mejor. Ahora nave ser "
        "heroica de verdad. Dar plano a cambio."
    ),
    "TheCollector_Recipes_Desc_Tiburon": (
        "Empresa humana hacer nueva versión de nave Hammerhead. No saber qué "
        "significa Tiburon, pero ser impresionante. Arma muy grande. Wikelo estudiar "
        "muy bien y saber todo. Poder darte plano del diseño y fabricarla.\\n\\n"
        "Poder comerciar. Traerme lo pedido y yo darte plano."
    ),
}


HMD = {
    "hmd_OptionsTheaterMode3D": "[Experimental] RV - Imagen 3D del modo cine",
    "hmd_OptionsTheaterMode3DOff": "Desactivada",
    "hmd_OptionsTheaterMode3DOn": "Activada",
    "hmd_OptionsTheaterMode3DStrong": "Intensa",
    "hmd_OptionsTheaterModeEnvironment": "[Experimental] RV - Entorno del modo cine",
    "hmd_OptionsTheaterModeEnvironmentAurora": "Aurora",
    "hmd_OptionsTheaterModeEnvironmentBlack": "Negro",
    "hmd_OptionsTheaterModeEnvironmentDayAndNight": "Día y noche",
    "hmd_OptionsTheaterModeEnvironmentOrbit": "Órbita",
    "hmd_OptionsTheaterModeEnvironmentStars": "Estrellas",
    "hmd_OptionsTheaterModeEnvironmentStorm": "Tormenta",
    "hmd_OptionsTheaterModeEnvironmentUnderwater": "Bajo el agua",
    "hmd_OptionsTheaterModeFloor": "[Experimental] RV - Suelo del modo cine",
    "hmd_OptionsTheaterModeFollow": "[Experimental] RV - Seguimiento de pantalla",
    "hmd_OptionsTheaterModeFollowAround": "A mi alrededor",
    "hmd_OptionsTheaterModeFollowOff": "Desactivado",
    "hmd_OptionsTheaterModeFollowWhereILook": "Donde mire",
    "hmd_OptionsTheaterModeGlow": "[Experimental] RV - Brillo de pantalla",
    "hmd_OptionsTheaterModeHeight": "[Experimental] RV - Altura del modo cine",
    "hmd_OptionsTheaterModeMirror": "[Experimental] RV - Imagen del monitor",
    "hmd_OptionsTheaterModeMirrorGame": "Juego",
    "hmd_OptionsTheaterModeMirrorTheater": "Cine",
    "hmd_OptionsTheaterModePreset": "[Experimental] RV - Tamaño de pantalla",
    "hmd_OptionsTheaterModePresetCinema": "Cine",
    "hmd_OptionsTheaterModePresetGiant": "Pantalla gigante",
    "hmd_OptionsTheaterModePresetLivingRoom": "Salón",
    "hmd_OptionsTheaterModePresetMonitor": "Monitor",
}
OVERRIDES.update(HMD)


VEHICLES = {
    "vehicle_DescAEGS_Tiburon_Collector_Military": (
        "Fabricante: Aegis Dynamics\\nEnfoque: Cañonera pesada\\n\\n"
        "Evolución de un diseño probado de Aegis, la configuración antinave "
        "capital del Tiburon combina un arma de haz frontal montada en el lomo "
        "con torretas laterales.\\n\\nWikelo aquí. Hacer modificaciones útiles "
        "para que nave sea mucho más cazadora. Muy impresionante."
    ),
    "vehicle_DescDRAK_Ironclad_Assault_Collector_Military": (
        "Fabricante: Drake Interplanetary\\nEnfoque: Nave de desembarco\\n\\n"
        "Cuando la entrega especial consiste en una incursión a gran escala, "
        "necesitas la Drake Ironclad Assault. Su bodega admite varios vehículos "
        "terrestres, dispone de torretas inferiores para despejar la zona de "
        "aterrizaje e incluso incluye un taller para reparaciones de emergencia."
        "\\n\\nWikelo aquí. Hacer modificaciones útiles para que nave sea mucho "
        "más cazadora. Muy impresionante."
    ),
    "vehicle_DescDRAK_Ironclad_Collector_Indust": (
        "Fabricante: Drake Interplanetary\\nEnfoque: Carga pesada\\n\\n"
        "El universo es cada vez más peligroso y ganarse la vida puede resultar "
        "mortal. Por eso Drake creó uno de los cargueros más resistentes, armado "
        "con una intimidante serie de torretas, una amplia bodega y un práctico "
        "rayo tractor.\\n\\nHola, Wikelo. Hacer modificaciones útiles para que "
        "nave sea aún más industrial. Te gustará."
    ),
    "vehicle_DescDRAK_Pitbull_Collector_Stealth": (
        "Fabricante: Drake Interplanetary\\nEnfoque: Caza auxiliar\\n\\n"
        "Una máquina de combate compacta y feroz. El Pitbull combina gran "
        "maniobrabilidad con potencia de fuego bruta en un pequeño vehículo para "
        "un solo piloto.\\n\\nWikelo aquí. Hacer modificaciones útiles para que "
        "nave sea mucho más difícil de ver. Sigilosa."
    ),
    "vehicle_DescMISC_Starlite_Collector_Indust": (
        "Fabricante: MISC\\nEnfoque: Repostaje ligero\\n\\n"
        "Si hay algo seguro en el universo es que las naves terminan quedándose "
        "sin combustible. Ahí entra el Starlite. Con dos depósitos estándar y un "
        "diseño estilizado, los ingenieros de MISC lo crearon para repostar naves "
        "varadas allí donde se encuentren.\\n\\nHola, Wikelo. Hacer modificaciones "
        "útiles para que nave sea aún más industrial. Te gustará."
    ),
    "vehicle_DescORIG_M80_Collector_Stealth": (
        "Fabricante: Origin Jumpworks\\nEnfoque: Caza pesado\\n\\n"
        "Disfruta de la elegancia sin renunciar a la defensa con el M80. Bajo el "
        "elegante diseño característico de Origin, el casco oculta un agresivo "
        "sistema de armas que puede desplegarse contra los atacantes en un instante."
        "\\n\\nWikelo aquí. Hacer modificaciones útiles para que nave sea mucho "
        "más difícil de ver. Sigilosa."
    ),
}
OVERRIDES.update(VEHICLES)


ARIL_BASE = (
    "Tipo de objeto: Armadura media\\nReducción de daño: 30%\\n"
    "Rango térmico: -61 / 91 °C\\nProtección radiactiva: 26400 REM\\n"
    "Eliminación de radiación: 145.8 REM/s\\n \\n"
    "Diseñada originalmente para mineros, la armadura Aril incorpora un cuello "
    "alto que aporta apoyo y protección adicionales al cuello y la nuca. Un "
    "cinturón de herramientas integrado y una mochila acoplable permiten llevar "
    "herramientas y suministros sin ocupar las manos."
)
OVERRIDES.update({
    "item_Desc_GRIN_utility_medium_arms_01_03_01": (
        ARIL_BASE + " La variante Fulcrum presenta un discreto gris oscuro."
    ),
    "item_Desc_GRIN_utility_medium_arms_01_04_10": (
        ARIL_BASE.replace(
            "incorpora un cuello alto",
            "incorpora un casco completamente cerrado y un cuello alto",
        ) + " La variante Bonebreaker combina blanco y gris."
    ),
    "item_Desc_grin_utility_medium_arms_01_03_02": (
        ARIL_BASE + " La variante Capstone combina tonos óxido y tierra."
    ),
    "item_Desc_grin_utility_medium_arms_01_03_03": (
        ARIL_BASE + " La variante MotherLode combina verde y marrón claro."
    ),
})


BODY_TRANSLATIONS = {
    "The smart choice for survival on the frontier, the Miasma is crafted from reinforced leather and offers protection without slowing you down. Perfect for someone who likes to move fast when the firefight starts.":
        "La Miasma, una elección inteligente para sobrevivir en la frontera, está fabricada con cuero reforzado y protege sin entorpecer los movimientos. Es perfecta para quien necesite moverse deprisa cuando empiecen los disparos.",
    "Lightweight and hardwearing, the Miasma Helmet is crafted from reinforced leather that offers full head protection without sacrificing flexibility. The reinforced face plate includes an attachment point for an external air supply.":
        "Ligero y resistente, el casco Miasma está fabricado con cuero reforzado y protege toda la cabeza sin sacrificar flexibilidad. La placa facial reforzada incluye un punto de conexión para un suministro de aire externo.",
    "When your survival depends on speed and mobility, the Miasma backpack won't let you down.  It's big enough to carry your extra load-out and survival gear and strong enough to keep it safe and ready for the moment you need it most.":
        "Cuando tu supervivencia dependa de la velocidad y la movilidad, la mochila Miasma no te fallará. Tiene espacio para equipo adicional y suministros de supervivencia, y es lo bastante resistente para mantenerlos seguros y listos.",
    "With its excellent design and eye-catching style, the Arden-SL armor exemplifies why security specialists love Roussimoff Rehabilitation Systems. This versatile armor set lets the wearer stay agile but safe thanks to the precise placement of special composite armor plating and fabrics. It also features a toolbelt for easy access to important gear.":
        "Con su excelente diseño y llamativo estilo, la armadura Arden-SL demuestra por qué los especialistas en seguridad confían en Roussimoff Rehabilitation Systems. La colocación precisa de placas y tejidos compuestos permite mantener la agilidad sin renunciar a la protección. También incorpora un cinturón para acceder rápidamente al equipo.",
    "With its excellent design and eye-catching style, the Arden-SL armor exemplifies why security specialists love Roussimoff Rehabilitation Systems. This versatile armor set lets the wearer stay agile but safe thanks to the precise placement of special composite armor plating and fabrics.":
        "Con su excelente diseño y llamativo estilo, la armadura Arden-SL demuestra por qué los especialistas en seguridad confían en Roussimoff Rehabilitation Systems. La colocación precisa de placas y tejidos compuestos permite mantener la agilidad sin renunciar a la protección.",
    "This specialist set of leggings designed by RRS utilize reinforced denim to provide the freedom and flexibility of pants, while providing essential protection. Metallic kneepads offer additional defense and support, ideal for security and workers alike.":
        "Estas perneras especializadas de RRS emplean tejido vaquero reforzado para ofrecer la libertad y flexibilidad de unos pantalones con la protección esencial. Las rodilleras metálicas añaden defensa y apoyo para personal de seguridad y trabajadores.",
    "Virgil's TrueDef line of personal body armor provide strategic protection of vital areas while keeping you fast and mobile. Numerous planetary law enforcement organizations and even the Advocacy use versions of the TrueDef to protect their officers and agents.":
        "La línea de armaduras personales TrueDef de Virgil protege de forma estratégica las zonas vitales sin restar velocidad ni movilidad. Numerosos cuerpos policiales planetarios, e incluso la Advocacy, utilizan variantes de TrueDef para proteger a sus agentes.",
    "Lightweight and breathable, this durable jumpsuit was designed by Stegman's to meet the precise needs of everyday engineers. Iterating on a classic, the Versa Coveralls features many quality of life improvements such as adjustable bracers, enhanced elbow and knee protection, and a slight elasticity in all the right places.":
        "Ligero, transpirable y resistente, este mono de Stegman's fue diseñado para las necesidades diarias de los ingenieros. El Versa Coveralls moderniza un clásico con brazales ajustables, mayor protección en codos y rodillas y elasticidad en los puntos adecuados.",
    "This comprehensive Tactical Combat Suit provides a complete sealed suit against vacuum, free range of motion, and interfaces seamlessly with compatible armor systems.":
        "Este completo traje de combate táctico sella al usuario frente al vacío, permite total libertad de movimientos y se integra sin problemas con sistemas de armadura compatibles.",
    "CDS’ Field Recon Suit is the perfect solution for the combat operator who wants a little extra protection without compromising any of their situational agility. EdgeCore composite plating is strategically sewn into the nano-weave suit to cover vital organs while keeping the suit flexible.":
        "El traje Field Recon de CDS es la solución ideal para quien busque más protección sin perder agilidad. Las placas compuestas EdgeCore están cosidas estratégicamente al tejido nanofibroso para cubrir los órganos vitales sin restar flexibilidad.",
    "CDS's quest to create the ideal light armor continues with the FBL-8a. This light armor will keep you fast on your feet with its strategic mix of protective plating and reinforced nano-weave fabrics. While the armor works with any undersuit, it was specifically designed to match the FBL-8u undersuit with special attention given to how the two fit together to make the set as streamlined and responsive as possible. Visor is AR crosshair compatible.":
        "CDS continúa buscando la armadura ligera ideal con la FBL-8a. Su combinación estratégica de placas y tejido nanofibroso reforzado mantiene al usuario rápido y protegido. Es compatible con cualquier traje interior, aunque se diseñó para encajar con el FBL-8u y formar un conjunto ágil y aerodinámico. El visor admite retículas de realidad aumentada.",
    "Be ready for any situation with the CSP-68L Backpack. Originally designed for the rigors of combat support, this light backpack has become popular thanks to its durability and a patented core connector that helps the CSP-68L sit comfortably and balanced on the back.":
        "Prepárate para cualquier situación con la mochila CSP-68L. Diseñada para las exigencias del apoyo de combate, se ha popularizado por su resistencia y por un conector patentado que la mantiene cómoda y equilibrada sobre la espalda.",
    "Comfortable and distinct, this soft-domed, billed hat from Code Blue Apparel makes for an ideal accessory to any security professional's uniform.":
        "Cómoda y distintiva, esta gorra de visera y copa blanda de Code Blue Apparel es el complemento ideal para el uniforme de cualquier profesional de seguridad.",
    "The Ajax Security Uniform Jacket is a standard security accessory produced by Code Blue Apparel's professional division. The jacket is a uniform intended for security professionals and does not provide any armored protection.":
        "La chaqueta de uniforme de seguridad Ajax es una prenda estándar de la división profesional de Code Blue Apparel. Está destinada al personal de seguridad y no ofrece protección blindada.",
    "The Ajax Security Uniform Pants are a standard security accessory produced by Code Blue Apparel's professional division. Flexible and durable, the pants are designed to match the Ajax Security Uniform Jacket and feature the same high-visibility piping. The pants are flexible and allow for a full range of motion.":
        "Los pantalones de uniforme de seguridad Ajax son una prenda estándar de la división profesional de Code Blue Apparel. Flexibles y resistentes, combinan con la chaqueta Ajax, comparten sus ribetes de alta visibilidad y permiten total libertad de movimiento.",
    "Originally designed as a strength enhancement suit to give factory workers better lifting power, CDS found wider application in utilizing its defensive capabilities. Its triple-enforced armor plating provides extreme physical protection, with deliberate placing of materials to protect the most vulnerable parts of the body. A series of pneumatic levers offer increased flexibility in the joints, alleviating pressure and weight in key areas to create an accessible and highly protective armor despite its heavy weight.":
        "Diseñada originalmente para aumentar la fuerza de los trabajadores de fábrica, CDS amplió sus usos al descubrir sus cualidades defensivas. Las placas con triple refuerzo ofrecen una protección física extrema y protegen las zonas más vulnerables. Un conjunto de palancas neumáticas mejora la flexibilidad de las articulaciones y alivia la presión y el peso en puntos clave.",
    "Originally designed as a strength enhancement suit to give factory workers better lifting power, CDS found wider application in utilizing its defensive capabilities. It's triple-enforced armor plating provides extreme physical protection, with deliberate placing of materials to protect the most vulnerable parts of the body. A series of pneumatic levers offer increased flexibility in the joints, alleviating pressure and weight in key areas to create an accessible and highly protective armor despite its heavy weight.":
        "Diseñada originalmente para aumentar la fuerza de los trabajadores de fábrica, CDS amplió sus usos al descubrir sus cualidades defensivas. Las placas con triple refuerzo ofrecen una protección física extrema y protegen las zonas más vulnerables. Un conjunto de palancas neumáticas mejora la flexibilidad de las articulaciones y alivia la presión y el peso en puntos clave.",
    "Reinforced alloys are carefully layered to recreate the appearance of warriors from Humanity's past to create an armor that's intimidating and fuctional. A decorative leather belt completes the look.":
        "Varias capas de aleaciones reforzadas recrean el aspecto de los guerreros del pasado de la Humanidad en una armadura intimidante y funcional. Un cinturón decorativo de cuero completa el conjunto.",
    "When your survival depends on speed and mobilty rather than sheer brute force, the leather-covered, triple weave of the IronCloud won't let you down. Offering life-saving protection without compromising your ability to make your move when the time is right.":
        "Cuando sobrevivir depende más de la velocidad y la movilidad que de la fuerza bruta, el entramado triple recubierto de cuero de la IronCloud no te fallará. Ofrece una protección vital sin impedirte moverte en el momento adecuado.",
    "Virgil's ForceFlex is the next generation in undersuit technology. Rated for combat as well as industrial work, you can rest assured that the comboweave will keep you protected in whatever situation you put it through.":
        "ForceFlex de Virgil representa la nueva generación de trajes interiores. Homologado tanto para combate como para trabajos industriales, su tejido compuesto te protegerá en cualquier situación.",
    "DMC's K7 are an all-purpose cargo pants. Four easy access pockets provide extra storage while the triple-stitched polymer weave fabric is designed to withstand all kinds of weather conditions.":
        "Los K7 de DMC son unos pantalones de carga multiuso. Cuatro bolsillos de fácil acceso aportan espacio adicional y el tejido polimérico con triple costura resiste todo tipo de condiciones meteorológicas.",
    "The Taberna jacket delivers refined design for rugged conditions. It features a weather resistant outer shell with additional paneling on the torso and arms. An integrated hood and shawl provide extra protection from the elements while a spacious toolbelt ensures gear remains within reach.":
        "La chaqueta Taberna combina un diseño refinado con resistencia para condiciones adversas. Su capa exterior soporta la intemperie y añade paneles en torso y brazos. La capucha y el chal integrados protegen de los elementos, mientras el amplio cinturón mantiene el equipo al alcance.",
    "Fearlessly face any weather with the Taos balaclava and goggles. An ultra-soft inner lining provides warmth and comfort while a special exterior coating repels precipitation. The adjustable headband ensures an ideal fit, and the padding of the anti-fog goggles is integrated directly into the fabric to seal out the elements.":
        "Afróntate a cualquier clima con el pasamontañas y las gafas Taos. El forro ultrasuave aporta calor y comodidad, y un revestimiento exterior repele la precipitación. La cinta ajustable garantiza un buen ajuste y el acolchado antivaho está integrado en el tejido para aislar de los elementos.",
    "Strong, practical, and stylish, these high-cut boots with reinforced straps will be just the thing you need for those long outdoor treks. The slip- and abrasion-resistant soles were constructed from a proprietary composite of recycled plastic and rubber to improve traction without sacrificing flexibility.":
        "Resistentes, prácticas y elegantes, estas botas altas con correas reforzadas son ideales para largas travesías. Las suelas antideslizantes y resistentes a la abrasión usan un compuesto de plástico reciclado y caucho que mejora el agarre sin sacrificar flexibilidad.",
    "The Alban is a long sleeve shirt made from comfortable, natural fabrics. Featuring a deep V-neck, its asymmetrical patchwork design provides it with a bit of texture and a two-toned look.":
        "Alban es una camisa de manga larga confeccionada con tejidos naturales y cómodos. Su profundo cuello en V y el diseño asimétrico de retales le aportan textura y un aspecto bicolor.",
    "Let the opposition know know you're not just a pretty face with this impassive ablative mask.":
        "Deja claro al enemigo que no eres solo una cara bonita con esta impasible máscara ablativa.",
    "Gyson delivers another unique softshell helmet with the J-5. Large optic sensors and an oversized breathing apparatus deliver a striking visage. The distinct design is space-rated and provides a modicum of protection, while keeping the helmet lightweight and affordable. This edition comes in a lighter tint.":
        "Gyson presenta otro singular casco flexible con el J-5. Sus grandes sensores ópticos y el respirador sobredimensionado crean un aspecto imponente. El diseño está homologado para el espacio y ofrece cierta protección sin dejar de ser ligero y asequible. Esta edición presenta un tono más claro.",
    "Gyson delivers another unique softshell helmet with the J-5. Large optic sensors and an oversized breathing apparatus deliver a striking visage. The distinct design is space-rated and provides a modicum of protection, while keeping the helmet lightweight and affordable. This edition comes in a darker tint with a contrasting reforced panel.":
        "Gyson presenta otro singular casco flexible con el J-5. Sus grandes sensores ópticos y el respirador sobredimensionado crean un aspecto imponente. El diseño está homologado para el espacio y ofrece cierta protección sin dejar de ser ligero y asequible. Esta edición presenta un tono más oscuro con un panel reforzado en contraste.",
    "Gyson delivers another unique softshell helmet with the J-5. Large optic sensors and an oversized breathing apparatus deliver a striking visage. The distinct design is space-rated and provides a modicum of protection, while keeping the helmet lightweight and affordable. This edition features a contrasting reforced panel.":
        "Gyson presenta otro singular casco flexible con el J-5. Sus grandes sensores ópticos y el respirador sobredimensionado crean un aspecto imponente. El diseño está homologado para el espacio y ofrece cierta protección sin dejar de ser ligero y asequible. Esta edición incorpora un panel reforzado en contraste.",
    "Fitting like a second skin, the Scaleweave undersuit boasts a hard-to-beat combination of durability and flexibility. Rated for industrial use and combat, it offers protection from hostile environments, vacuum included, without sacrificing freedom of movement. Whatever your choice of armor, the Haut edition is a solid foundation.":
        "El traje interior Scaleweave se ajusta como una segunda piel y ofrece una combinación difícil de superar de resistencia y flexibilidad. Homologado para uso industrial y combate, protege de entornos hostiles, incluido el vacío, sin limitar los movimientos. La edición Haut es una base sólida para cualquier armadura.",
    "Elegant design meets innovation with the Palatino armor from Quirinus Tech. The fully-enclosed helmet comes equipped with a suite of sensors that connects the wearer to the wider world while providing supreme protection. Visor is AR crosshair compatible. The Deadlift variant features blood-red accents inspired by the Claw Slamander aesthetic.":
        "La armadura Palatino de Quirinus Tech combina diseño elegante e innovación. Su casco completamente cerrado incorpora sensores que mantienen al usuario conectado con el exterior y ofrece una protección excepcional. El visor admite retículas de realidad aumentada. La variante Deadlift luce detalles rojo sangre inspirados en la estética Claw Slamander.",
    "With its excellent design and eye-catching style, the Arden-SL armor exemplifies why security specialists love Roussimoff Rehabilitation Systems. This versatile armor set lets the wearer stay agile but safe thanks to the precise placement of special composite armor plating and fabrics. This variant retains the protection of the original armor with the careful placement of strengthened shoulder pads and elbow braces.":
        "Con su excelente diseño y llamativo estilo, la armadura Arden-SL demuestra por qué los especialistas en seguridad confían en Roussimoff Rehabilitation Systems. La colocación precisa de placas y tejidos compuestos permite mantener la agilidad sin renunciar a la protección. Esta variante conserva la defensa original y añade hombreras y refuerzos de codo reforzados.",
    "Salvaged pieces of disused protective gear were welded together to make this intimidating armor set. The Deadlift edition includes a varigated grey cape, made from an old Banu wall-hanging.":
        "Varias piezas recuperadas de equipos de protección en desuso se soldaron para crear este intimidante conjunto. La edición Deadlift incluye una capa gris jaspeada confeccionada con un antiguo tapiz Banu.",
    "Salvaged ship parts and pieces of disused protective gear were welded together to make this intimidating armor set. The Bonebreaker edition comes in gray and white.":
        "Piezas de nave recuperadas y equipos de protección en desuso se soldaron para crear este intimidante conjunto. La edición Bonebreaker combina gris y blanco.",
    "When your survival depends on speed and mobilty, the IronCloud backpackwon't let you down.  It's big enough to carry your extra load-out and survival gear and strong enough to keep it safe and ready for the moment you need it most.":
        "Cuando tu supervivencia dependa de la velocidad y la movilidad, la mochila IronCloud no te fallará. Tiene espacio para equipo adicional y suministros de supervivencia, y es lo bastante resistente para mantenerlos seguros y listos.",
    "Perfected through centuries of innovation, Syang Fabrication's sleek and stylish Xanthule flight suit has been meticulously adapted to the Human physique. The Xanthule suit features breathable lightweight plating made with a carbon-silk weave that provides reliable protection while maintaining the famed House's signature aesthetic.":
        "Perfeccionado durante siglos de innovación, el elegante traje de vuelo Xanthule de Syang Fabrication ha sido adaptado minuciosamente a la fisonomía humana. Sus placas ligeras y transpirables, fabricadas con seda de carbono, ofrecen una protección fiable sin perder la estética característica de la célebre Casa.",
    "Perfected through centuries of innovation, Syang Fabrication's sleek and stylish Xanthule flight suit has been meticulously adapted to the Human physique. The Xanthule suit features breathable lightweight plating made with a carbon-silk weave that provides reliable protection while maintaining the famed House's signature aesthetic. This special IAE 2953 edition is decorated with a copper and white pattern inspired by Gatac Manufacture's Syulen.":
        "Perfeccionado durante siglos de innovación, el elegante traje de vuelo Xanthule de Syang Fabrication ha sido adaptado minuciosamente a la fisonomía humana. Sus placas ligeras y transpirables, fabricadas con seda de carbono, ofrecen una protección fiable sin perder la estética característica de la célebre Casa. Esta edición especial IAE 2953 luce un patrón cobre y blanco inspirado en la Syulen de Gatac Manufacture.",
    "The Verdict from Kastak Arms is an exemplary LMG with a special difference. As things begin to overheat during combat, operators can switch the Verdict to an alternate mode that will utilize the excess thermal buildup to fire intense plasma rounds.":
        "La Verdict de Kastak Arms es una ametralladora ligera ejemplar con una particularidad. Cuando empieza a sobrecalentarse durante el combate, el operador puede cambiar al modo alternativo y aprovechar el exceso de energía térmica para disparar potentes proyectiles de plasma.",
    "This battery for the Verdict LMG holds enough energy for 75 shots.":
        "Esta batería para la ametralladora ligera Verdict almacena energía para 75 disparos.",
    "Klaus & Werner’s Arrowhead Model VI long-range energy rifle features a fiberglass composite body capable of withstanding any number of rigorous environments both in atmosphere and out. Built with a precision stock, compound scope and built-in bipod, the Arrowhead offers a stable and devastating weapon for operators who want to keep their distance, but stay in the fight.":
        "El fusil de energía de largo alcance Arrowhead Model VI de Klaus & Werner incorpora un cuerpo de fibra de vidrio compuesta capaz de soportar entornos extremos, tanto dentro como fuera de la atmósfera. Su culata de precisión, mira compuesta y bípode integrado ofrecen un arma estable y devastadora para quien prefiera combatir a distancia.",
}


EDITION_TRANSLATIONS = {
    "The Tripwire edition dons your gun with dark green camo print over a black base.": "La edición Tripwire combina camuflaje verde oscuro con una base negra.",
    "The Adder Camo edition blends dark browns, greens and blacks for a look that's ready to strike.": "La edición Adder Camo mezcla marrones oscuros, verdes y negros.",
    "This special camo edition features dark shades of gray well-suited for urban environments.": "Esta edición de camuflaje emplea grises oscuros ideales para entornos urbanos.",
    "The Dire edition features white and light gray digital camo to create a stark finish.": "La edición Dire presenta un marcado camuflaje digital blanco y gris claro.",
    "With multiple shades of dark green, the Copse digital camo is ideal for when the front lines are in the backwoods.": "El camuflaje digital Copse combina varios verdes oscuros, ideal para combatir en zonas boscosas.",
    "The Debonair edition features an elegant white and black finish sure to appeal to those with sophisticated tastes.": "La edición Debonair presenta un elegante acabado blanco y negro para gustos refinados.",
    "The Deadlift edition is primarily gray and white.": "La edición Deadlift es principalmente gris y blanca.",
    "The Bonebreaker edition is primarily gray and white.": "La edición Bonebreaker es principalmente gris y blanca.",
    "This edition comes in a forest green livery.": "Esta edición presenta una librea verde bosque.",
    "The Capstone edition is comes in a lowkey rust brown palette.": "La edición Capstone presenta una discreta paleta marrón óxido.",
    "The Capstone edition comes in varigated earth tones.": "La edición Capstone combina distintos tonos tierra.",
    "The Pacesetter edition features light brown and green tones.": "La edición Pacesetter combina tonos marrón claro y verde.",
    "The Wraith variant features a gray-on-gray colorway with brown accents and armored reinforcements.": "La variante Wraith combina varios grises, detalles marrones y refuerzos blindados.",
    "The Shubin II-A edition is a combination of grays.": "La edición Shubin II-A combina varios tonos de gris.",
    "The Shubin II-A edition is predominately gray with orange accents.": "La edición Shubin II-A es principalmente gris con detalles naranjas.",
    "The Shubin II-A edition is gray with orange stripes.": "La edición Shubin II-A es gris con franjas naranjas.",
    "The Shubin II-B edition is predominately gray with orange accents.": "La edición Shubin II-B es principalmente gris con detalles naranjas.",
    "The Shubin II-B edition features a combination of grays and stripes.": "La edición Shubin II-B combina varios grises y franjas.",
    "The People's Alliance S-1 edition is a combination of dark gray and deep navy blue.": "La edición People's Alliance S-1 combina gris oscuro y azul marino intenso.",
    "The People's Alliance S-1 edition is a slate gray with a blue, fragmented digital pattern.": "La edición People's Alliance S-1 es gris pizarra con un patrón digital azul fragmentado.",
    "The People's Alliance S-1 edition is a deep navy blue, with light blue trims and black accents.": "La edición People's Alliance S-1 es azul marino intenso con ribetes azul claro y detalles negros.",
    "The People's Alliance S-2 edition is a deep navy blue and black with metallic gray accents.": "La edición People's Alliance S-2 combina azul marino intenso y negro con detalles gris metálico.",
    "The People's Alliance S-2 edition is a slate gray with a blue, fragmented digital pattern.": "La edición People's Alliance S-2 es gris pizarra con un patrón digital azul fragmentado.",
    "The Rayari edition is maroon red with black accents.": "La edición Rayari es rojo granate con detalles negros.",
    "The Rayari edition is black and maroon red with gray accents.": "La edición Rayari combina negro y rojo granate con detalles grises.",
    "The Rayari edition is mostly gray with maroon red accents.": "La edición Rayari es principalmente gris con detalles rojo granate.",
    "The Rayari edition is black with a fragmented digital camo pattern.": "La edición Rayari es negra con un patrón de camuflaje digital fragmentado.",
    "The Rayari PRX edition is black and maroon red with metallic gray accents.": "La edición Rayari PRX combina negro y rojo granate con detalles gris metálico.",
    "The Rayari PRX edition is black with red accents and a fragmented digital camo pattern.": "La edición Rayari PRX es negra con detalles rojos y camuflaje digital fragmentado.",
    "The Covalex Spec. edition is black and crimson red with metallic gray accents.": "La edición Covalex Spec. combina negro y rojo carmesí con detalles gris metálico.",
    "The Covalex edition is black with crimson red accents.": "La edición Covalex es negra con detalles rojo carmesí.",
    "The Covalex edition is black and crimson red with light orange accents.": "La edición Covalex combina negro y rojo carmesí con detalles naranja claro.",
    "The Covalex edition is mostly a crimson red with black accents.": "La edición Covalex es principalmente rojo carmesí con detalles negros.",
    "The Covalex edition is mostly black, with orange accents and a red fragmented digital pattern.": "La edición Covalex es principalmente negra, con detalles naranjas y un patrón digital rojo fragmentado.",
    "The Shubin edition is light gray with orange accents.": "La edición Shubin es gris claro con detalles naranjas.",
    "The Shubin edition is mostly a pale orange with black and gray accents.": "La edición Shubin es principalmente naranja pálido con detalles negros y grises.",
    "The Foxwell edition is mostly white with pale blue accents and touches of black.": "La edición Foxwell es principalmente blanca con detalles azul pálido y toques negros.",
    "The Overtime edition is a simple and straightforward dark gray.": "La edición Overtime presenta un sencillo gris oscuro.",
    "The Lateshift edition are a practical and professional black, suitable for any occasion.": "La edición Lateshift luce un negro práctico y profesional, adecuado para cualquier ocasión.",
    "The Packrat version comes in a pattern of variegated earth tones.": "La versión Packrat presenta un patrón de variados tonos tierra.",
    "The Sundown version comes in a dark rust colorway.": "La versión Sundown presenta un tono óxido oscuro.",
    "The Sundown version mixes rest red and dirty gray tones.": "La versión Sundown combina rojo óxido y gris sucio.",
    "The Huntsman edition features a subtly variegated moss green look.": "La edición Huntsman presenta sutiles variaciones de verde musgo.",
    "The Huntsman variant combines lived-in gray and brown tones.": "La variante Huntsman combina tonos grises y marrones desgastados.",
    "The Poacher variant comes in variegated browns.": "La variante Poacher combina distintos tonos marrones.",
    "The Poacher variant combines distressed gray and brown tones.": "La variante Poacher combina tonos grises y marrones desgastados.",
    "The Fulcrum edition is comes in a lowkey gray palette.": "La edición Fulcrum presenta una discreta paleta gris.",
    "The Memoir edition is a stoney gray with subdued red accents.": "La edición Memoir luce un gris pétreo con discretos detalles rojos.",
    "The Rancor edition is predominately a deep shade of crimson with subtle silver detailing.": "La edición Rancor presenta un intenso carmesí con discretos detalles plateados.",
    "The Barricade edition is a combination of rustic browns and subtle metallic dealings.": "La edición Barricade combina marrones rústicos con discretos detalles metálicos.",
    "The Chairman's Club edition is a chic black adorned with expensive gold trimmings in a style reminiscent of the club it belongs to.": "La edición Chairman's Club luce un elegante negro con lujosos remates dorados inspirados en el club al que pertenece.",
    "The People's Alliance edition is mostly black, with a distinct blue trim that runs through the middle of the cap, and the People's Alliance logo emblazoned on the front.": "La edición People's Alliance es principalmente negra, con una franja azul en el centro y el logotipo de People's Alliance en la parte frontal.",
    "The People's Alliance edition is mostly black with a distinct blue trim and the People's Alliance logo emblazoned on the arm.": "La edición People's Alliance es principalmente negra, con un ribete azul y el logotipo de People's Alliance en el brazo.",
    "The People's Alliance edition is mostly black with a distinct light blue trim.": "La edición People's Alliance es principalmente negra con un ribete azul claro.",
    "The People's Alliance edition is mostly a deep navy blue and black, with metallic gray accents and the People's Alliance logo attached.": "La edición People's Alliance combina azul marino intenso y negro, con detalles gris metálico y su logotipo.",
    "The Rayari edition is maroon red and light gray with the Rayari Incorporated logo attached.": "La edición Rayari combina rojo granate y gris claro con el logotipo de Rayari Incorporated.",
    "The Rayari PRX edition is mostly black and maroon red, with metallic gray accents and the Rayari logo attached.": "La edición Rayari PRX combina principalmente negro y rojo granate, con detalles gris metálico y el logotipo de Rayari.",
    "The Covalex edition is mostly black and crimson red, with metallic gray accents and Covalex Shipping's logo attached.": "La edición Covalex combina principalmente negro y rojo carmesí, con detalles gris metálico y el logotipo de Covalex Shipping.",
    "The Shubin edition is light gray with orange accents and the Shubin Interstellar logo.": "La edición Shubin es gris claro con detalles naranjas y el logotipo de Shubin Interstellar.",
    "The Rayari edition is mostly maroon red with black accents.": "La edición Rayari es principalmente rojo granate con detalles negros.",
    "The Fulcrum edition features earth-toned knee protectors and greaves.": "La edición Fulcrum presenta rodilleras y grebas en tonos tierra.",
    "The Poacher variant combines rust red and gray-brown tones.": "La variante Poacher combina rojo óxido y tonos marrón grisáceo.",
    "The Huntsman edition features a mix of green and brown tones.": "La edición Huntsman combina tonos verdes y marrones.",
    "The Poacher variant combines rust red and gray-brown tones and includes a rust-colored cowl.": "La variante Poacher combina rojo óxido y marrón grisáceo, e incluye una capucha de color óxido.",
    "The Sundown version features a rest red torso with a dirty cowl.": "La versión Sundown presenta un torso rojo óxido y una capucha desgastada.",
    "The Huntsman editions features a mix of green and brown tones, with a moss-green cowl.": "La edición Huntsman combina tonos verdes y marrones con una capucha verde musgo.",
    "Let the opposition know know you're not just a pretty face with this matt black ablative mask.": "Deja claro al enemigo que no eres solo una cara bonita con esta máscara ablativa negra mate.",
    "Let the opposition know know you're not just a pretty face with this dark gray ablative mask.": "Deja claro al enemigo que no eres solo una cara bonita con esta máscara ablativa gris oscuro.",
    "Let the opposition know know you're not just a pretty face, with this green-gray ablative mask.": "Deja claro al enemigo que no eres solo una cara bonita con esta máscara ablativa verde grisácea.",
    "Let the opposition know know you're not just a pretty face, with this blue-tinted ablative mask.": "Deja claro al enemigo que no eres solo una cara bonita con esta máscara ablativa de tono azulado.",
    "A polyester navy blue hat, with a black trim and light blue labelling, proudly displaying the People's Alliance logo.": "Gorra de poliéster azul marino con ribete negro, detalles azul claro y el logotipo de People's Alliance.",
    "A polyester maroon red hat, with a black trim and gray labelling, proudly displaying the Rayari Incorporated logo.": "Gorra de poliéster rojo granate con ribete negro, detalles grises y el logotipo de Rayari Incorporated.",
    "A polyester red hat, with a pale orange trim and white labelling, proudly displaying the Covalex Shipping logo.": "Gorra de poliéster roja con ribete naranja pálido, detalles blancos y el logotipo de Covalex Shipping.",
    "A polyester light gray hat, proudly displaying Shubin Interstellar's logo.": "Gorra de poliéster gris claro con el logotipo de Shubin Interstellar.",
    "A polyester navy blue t-shirt with a black trim, proudly displaying the People's Alliance logo.": "Camiseta de poliéster azul marino con ribete negro y el logotipo de People's Alliance.",
    "A polyester gray t-shirt with a maroon red trim, proudly displaying the Rayari Incorporated logo.": "Camiseta de poliéster gris con ribete rojo granate y el logotipo de Rayari Incorporated.",
    "A polyester black t-shirt with a red trim, proudly displaying the Covalex Shipping logo.": "Camiseta de poliéster negra con ribete rojo y el logotipo de Covalex Shipping.",
    "A polyester light gray t-shirt with a subtle orange trim, proudly displaying Shubin Interstellar's logo.": "Camiseta de poliéster gris claro con un discreto ribete naranja y el logotipo de Shubin Interstellar.",
    "The Poacher's color scheme complements a wide range of light armour types.": "La combinación de colores Poacher complementa una amplia variedad de armaduras ligeras.",
    "The Sundown's color scheme complements a wide range of light armour types.": "La combinación de colores Sundown complementa una amplia variedad de armaduras ligeras.",
    "The Packrat color scheme complements a wide range of light armour types.": "La combinación de colores Packrat complementa una amplia variedad de armaduras ligeras.",
    "The Huntsman's color scheme complements a wide range of light armour types.": "La combinación de colores Huntsman complementa una amplia variedad de armaduras ligeras.",
}


def clean(value: str) -> str:
    value = re.sub(r"(?:\\n)+$", "", value)
    value = value.replace("’", "'").replace("‘", "'").replace("�", "'")
    return re.sub(r"\s+", " ", value).strip()


BODY_BY_CLEAN = {clean(key): value for key, value in BODY_TRANSLATIONS.items()}
EDITION_BY_CLEAN = {clean(key): value for key, value in EDITION_TRANSLATIONS.items()}


def translate_stats(paragraph: str) -> str | None:
    if not re.search(r"^(?:Manufacturer|Item Type|Damage Reduction|Carrying Capacity|Magazine(?: Size)?|Battery(?: Size)?|Attachments):", paragraph):
        return None
    replacements = (
        ("Manufacturer:", "Fabricante:"), ("Item Type:", "Tipo de objeto:"),
        ("Class:", "Clase:"), ("Damage Reduction:", "Reducción de daño:"),
        ("Temp. Rating:", "Rango térmico:"),
        ("Radiation Protection:", "Protección radiactiva:"),
        ("Radiation Scrub Rate:", "Eliminación de radiación:"),
        ("G-Force Tolerance:", "Tolerancia a fuerzas g:"),
        ("Carrying Capacity:", "Capacidad:"), ("Backpacks:", "Mochilas:"),
        ("Magazine Size:", "Cargador:"), ("Magazine:", "Cargador:"),
        ("Battery Size:", "Batería:"), ("Battery:", "Batería:"),
        ("Capacity:", "Capacidad:"), ("Rate Of Fire:", "Cadencia:"),
        ("Effective Range:", "Alcance efectivo:"), ("Attachments:", "Accesorios:"),
        ("Heavy Armor", "Armadura pesada"), ("Medium Armor", "Armadura media"),
        ("Light Armor", "Armadura ligera"), ("Light Helmet", "Casco ligero"),
        ("Light Backpack", "Mochila ligera"), ("Heavy Backpack", "Mochila pesada"),
        ("Undersuit", "Traje interior"), ("Flight Suit", "Traje de vuelo"),
        ("Assault Rifle", "Fusil de asalto"), ("Sniper Rifle", "Fusil de francotirador"),
        ("Shotgun", "Escopeta"), ("Crossbow", "Ballesta"),
        ("Rifle", "Fusil"), ("Pistol", "Pistola"),
        ("Ballistic", "Balística"), ("Energy", "Energía"),
        ("Laser", "Láser"), ("All", "Todas"), ("Light, Medium", "Ligeras y medias"),
        ("Light", "Ligeras"), ("Heavy", "Pesadas"),
        ("Optics", "Óptica"), ("Barrel", "Cañón"), ("Underbarrel", "Accesorio inferior"),
        ("N/A", "N/D"),
    )
    out = paragraph
    for source, target in replacements:
        out = out.replace(source, target)
    return out


def ph_description(key: str, english: dict[str, str]) -> str:
    name_key = key.replace("item_Desc", "item_Name", 1)
    name = english.get(name_key)
    return f"(PH) Descripción de {name}" if name else "(PH) Descripción pendiente"


def main() -> int:
    old = load(OLD_EN)
    new = load(NEW_EN)
    current = load(GLOBAL)
    changed = {key for key in new if key not in old or new[key] != old[key]}

    # Memoria exacta de segmentos procedente solo de entradas que no cambiaron.
    memory: dict[str, list[str]] = defaultdict(list)
    for key, source in old.items():
        if key in changed or key not in current:
            continue
        target = current[key]
        source_parts = source.split(r"\n\n")
        target_parts = target.split(r"\n\n")
        if len(source_parts) == len(target_parts):
            for source_part, target_part in zip(source_parts, target_parts):
                if clean(source_part) and clean(source_part) != clean(target_part):
                    memory[clean(source_part)].append(target_part)

    def remembered(part: str) -> str | None:
        values = list(dict.fromkeys(memory.get(clean(part), [])))
        return values[0] if len(values) == 1 else None

    translations = dict(OVERRIDES)
    unresolved: list[tuple[str, str]] = []

    # Nombres propios de objetos/naves y ubicaciones nuevas o modificadas.
    for key in changed:
        if key.startswith(("item_Name", "item_name", "vehicle_Name", "mission_location_", "itemPort_", "port_")):
            translations[key] = new[key]

    description_keys = sorted(
        key for key in changed if key.startswith(("item_Desc", "vehicle_Desc"))
    )
    for key in description_keys:
        if key in translations:
            continue
        source = new[key]
        if re.match(r"^PH ?-? Description", source, re.IGNORECASE):
            translations[key] = ph_description(key, new)
            continue

        # Las ediciones de armas reutilizan la traducción comprobada del modelo base.
        base_key = re.sub(r"_(?:lr\d+|sf\d+)$", "", key)
        if base_key != key and base_key in current and "PH" not in current[base_key]:
            edition = source.split(r"\n\n")[-1].strip()
            edition_es = EDITION_TRANSLATIONS.get(clean(edition)) or remembered(edition)
            if edition_es:
                base = current[base_key].replace("Batería: 70", "Batería: 75").rstrip()
                translations[key] = f"{base}\\n\\n{edition_es}"
                continue

        parts: list[str] = []
        failed = False
        for part in source.split(r"\n\n"):
            stripped = part.strip()
            if not stripped:
                parts.append("")
                continue
            translated = (
                remembered(stripped)
                or BODY_BY_CLEAN.get(clean(stripped))
                or EDITION_BY_CLEAN.get(clean(stripped))
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
        print(f"ERROR: {len(unresolved)} segmentos nuevos siguen sin traducción:")
        for key, segment in unresolved:
            print(f"\n{key}\n{segment}")
        return 1

    cleanup_replacements = (
        ("Core Compatibility: Todas", "Compatibilidad de torso: Todas"),
        ("Core Compatibility: Pesadas", "Compatibilidad de torso: Pesada"),
        ("Core Compatibility: Ligeras", "Compatibilidad de torso: Ligera"),
        ("Mochilas: Light, Medium", "Mochilas: Ligeras y medias"),
        ("Mochilas: Light", "Mochilas: Ligeras"),
        ("Mochilas: Medium", "Mochilas: Medias"),
        ("Mochilas: Heavy", "Mochilas: Pesadas"),
        ("Mochilas: All", "Mochilas: Todas"),
        ("Tipo de objeto: LMG", "Tipo de objeto: Ametralladora ligera"),
        ("Tipo de objeto: Battery", "Tipo de objeto: Batería"),
        ("Tipo: Rifle", "Tipo: Fusil"),
        ("Tipo: Crossbow", "Tipo: Ballesta"),
    )
    for key, value in list(translations.items()):
        if key.startswith(("item_Desc", "vehicle_Desc")):
            for source, target in cleanup_replacements:
                value = value.replace(source, target)
            translations[key] = value.rstrip()

    raw = GLOBAL.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    output: list[str] = []
    applied: set[str] = set()
    for line in text.splitlines():
        if "=" in line and not line.startswith((";", "[")):
            raw_key, _ = line.split("=", 1)
            key = normalize(raw_key)
            if key in translations:
                line = f"{raw_key}={translations[key]}"
                applied.add(key)
        output.append(line)

    missing = set(translations) - applied
    if missing:
        raise SystemExit(f"Claves no encontradas en global.ini: {sorted(missing)}")

    encoded = (newline.join(output) + newline).encode("utf-8")
    GLOBAL.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    print(f"PTU 5.0.202: {len(applied)} entradas nuevas o modificadas revisadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
