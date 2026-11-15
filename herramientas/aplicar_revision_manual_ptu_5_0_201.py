#!/usr/bin/env python3
"""Aplica la revisión humana final de textos nuevos y cambiados en PTU 5.0.201."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GLOBAL_INI = ROOT / "global.ini"
REWARD_HEADING = "\\n\\n<EM4>RECOMPENSAS DEL CONTRATO</EM4>"

OVERRIDES = {
    # Interfaz y objetivos: redacción corta para evitar desbordamientos.
    "MWCH01_Obj1_Marker": "Señal del ingeniero jefe",
    "MWCH01_Obj1_Short": "Localizar al ingeniero jefe",
    "MWCH01_Obj1_Long": "Localizar al ingeniero jefe en Control de flujo",
    "MWCH01_Obj1a_Long": "Usar el terminal para mover el puente",
    "MWCH01_Obj1a_Short": "Mover el puente desde el terminal",
    "MWCH01_Obj2_Long": "Ir a Control de flujo",
    "MWCH01_Obj2_Short": "Ir a Control de flujo",
    "MWCH01_Obj2a_Marker": "Ascensor a Sala de bombas",
    "MWCH01_Obj2b_Long": "Ir a la Sala de bombas",
    "MWCH01_Obj2b_Short": "Ir a la Sala de bombas",
    "MWCH01_Obj2d_Long": "Desactivar la puerta con fusible",
    "MWCH01_Obj2d_Short": "Desactivar la puerta con fusible",
    "MWCH01_Obj3_Long": "Sobrevivir a la emboscada de First Legion",
    "MWCH01_Obj3a_Long": "Eliminar hostiles de First Legion",
    "MWCH01_Obj3b_Long": "Eliminar al capitán de First Legion",
    "MWCH01_Obj4_Long": "Ir a la sala de la centrífuga",
    "MWCH01_Obj4_Short": "Ir a la sala de la centrífuga",
    "MWCH01_Obj5a_Long": "Desactivar acopladores sobrecargados %ls",
    "MWCH01_Obj5b_Long": "Bajar la centrífuga desde el terminal",
    "MWCH01_Obj5b_Short": "Bajar la centrífuga",
    "MWCH01_Obj6_Long": "Eliminar al general de First Legion",
    "MWCH01_Obj6_Marker": "General",
    "MWCH01_Obj6_Short": "Eliminar al general",
    "MWCH01_Obj7a_Long": "Usa el ascensor para volver al vestíbulo",
    "MWCH01_Obj7a_Short": "Volver al vestíbulo en ascensor",
    "MWPrologue_Obj2_Long": "Restaurar el acceso a las instalaciones",
    "MWPrologue_Obj3_Long": "Eliminar a First Legion en la sala de bombas",
    "MWPrologue_Obj4_Long": "Usar el terminal de la sala de bombas",
    "MWPrologue_Obj4_Short": "Usar terminal de control",
    "MWPrologue_Obj4a_Long": "Restaurar el acceso desde los terminales de sensores",
    "MWPrologue_Obj4a_Short": "Usar terminales de sensores %ls",
    "MWPrologue_Obj6_Long": "Dejar los dispositivos en el vestíbulo",
    "SM_Probe_Button_ScanAndExtract": "Escanear y extraer",
    "SM_Probe_Button_Undeploy": "Replegar dispositivo",
    "SM_Probe_DataExtracted": "Completado",
    "SM_Probe_SampleExtracted": "Completado",
    "area_name_GuildHall": "Sede del gremio",
    "area_name_SurveyTower": "Torre topográfica",
    "interaction_condition_InSpace": "No está en el espacio",
    "pause_OptionsPlanetScattering": "Distancia de objetos (Nyx)",
    "pause_OptionsPlanetTerrainVirtualTextures": "Calidad del terreno (Nyx)",
    "port_Turret_BottomLeft": "Torreta inf. izq.",
    "port_Turret_BottomRight": "Torreta inf. der.",
    "port_Turret_Front": "Torreta delantera",
    "port_Turret_Rear": "Torreta trasera",
    "port_Turret_SideLeft": "Torreta lateral izq.",
    "port_Turret_SideRight": "Torreta lateral der.",
    "port_Turret_TopLeft": "Torreta sup. izq.",
    "port_Turret_TopRight": "Torreta sup. der.",
    "cargoTransfer_HUD_NoCargoOrder": "Este vehículo no tiene pedido. Haz uno en un terminal.",
    "cargoTransfer_HUD_TransferUnavailable": "No se puede transferir. Revisa el pedido en el terminal.",
    "cargoTransfer_HUD_CargoSlotReservationTimeOut": "Entra en la zona de carga asignada",
    "cargoTransfer_HUD_CargoSlotRevokedSubtext": "Solicita otra zona de carga para continuar.",
    "cargoTransfer_HUD_CargoSlotRevokedTitle": "Permiso de carga revocado",
    "cargoTransfer_HUD_CargoWaitingForVehicleStateChange": "Extiende del todo los husillos de carga",
    "cargoTransfer_HUD_VehicleLeftAreaTitle": "Pedido de carga pendiente",
    "cargoTransfer_HUD_VehicleMovedOutOfArea": "Vuelve a la zona de carga asignada.",
    "cargoTransfer_HUD_VehicleMustLeaveCargoSlotSubtext": "El vehículo será retirado por la fuerza.",
    "cargoTransfer_HUD_VehicleMustLeaveCargoSlotTitle": "Sal de la zona de carga",
    "Temp_CovalexShipping_Remove": "ERROR:\\nRetira los objetos incorrectos",
    "Temp_CovalexShipping_Inaction": "Por inactividad,\\nel objeto ha sido confiscado",
    # Títulos locales revisados: naturales, concisos y sin falsos amigos.
    "Local_CourierSingleToMulti_2Items_Title_002": "El equipo de investigación necesita ayuda",
    "Local_CourierSingleToMulti_2Items_Title_003": "Reparto de correo",
    "Local_CourierSingleToMulti_2Items_Title_004": "Pequeña entrega en dos paradas",
    "Local_CourierSingle_Title_003": "Estoy enfermo",
    "Local_CourierSingle_Title_004": "Entrega de una caja pequeña",
    "Local_CourierSingle_Title_005": "Mecánico en apuros",
    "Local_CourierSingle_Title_010": "Recoger basura en ~mission(Location)",
    "Local_CourierSingle_Title_011": "Objetos olvidados en ~mission(Location)",
    "Local_CourierSingle_Title_012": "Recoger datos en ~mission(Location)",
    "Local_CourierSingle_Title_013": "Recoger ropa en ~mission(Location)",
    "Local_CourierSingle_Title_015": "Suministros urgentes para ~mission(Destination)",
    "Local_CourierSingle_Title_016": "Medicinas para ~mission(Destination)",
    "Local_CourierSingle_Title_017": "Cerveza sorpresa para ~mission(Destination)",
    "Local_CourierSingle_Title_018": "Recogida de cerveza",
    "Local_CourierSingle_Title_019": "Galletas para ~mission(Destination)",
    "Local_CourierSingle_Title_020": "Llevar ropa a ~mission(Destination)",
    "Local_DeliveryMultiToSingle_3Items_Title_002": "Suministros para el puesto",
    "Local_DeliveryMultiToSingle_3Items_Title_003": "Mensajero para una obra",
    "Local_DeliveryMultiToSingle_3Items_Title_004": "Gran entrega con varias paradas",
    "Local_DeliveryPersonalEffects_Title_002": "Arreglar el error del anterior",
    "Local_DeliverySingleToMulti_2Items_Title_002": "Reparto urgente",
    "Local_DeliverySingleToMulti_2Items_Title_003": "Entregar mis rocas",
    "Local_DeliverySingleToMulti_2Items_Title_004": "Entrega con varias paradas",
    "Local_DeliverySingle_Title_001": "Mudanza desastrosa",
    "Local_DeliverySingle_Title_003": "Falló el repartidor",
    "Local_DestroyItems_Servers_Title_001": "¡Salva la salsa de Nonna!",
    "Local_DestroyItems_Servers_Title_003": "Suegra monstruosa",
    "Local_DestroyItems_Servers_Title_007": "Destruir servidores de estafadores",
    "Local_DownloadSingle_Title_001": "Burlar a la cazafortunas",
    "Local_DownloadSingle_Title_002": "La cita infernal",
    "Local_DownloadSingle_Title_004": "Acceder a datos bloqueados",
    "Local_DownloadSingle_Title_006": "Fuga de datos",
    "Local_DownloadSingle_Title_008": "Recuperar y entregar datos",
    "Local_KillSingle_Title_003": "En memoria de mi hermana",
    "Local_KillSingle_Title_009": "Justicia kármica",
    "Local_RecoverSingle_Title_002": "Entrega atrasada",
    "Local_RecoverSingle_Title_003": "Recuperar envío perdido",
    "Local_RecoverSingle_Title_005": "Recuperar propiedad robada",
    "Local_RecoverSingle_Title_008": "Recuperar propiedad antigua",
    "Local_RecoverSingle_Title_009": "Recuperar objetos robados",
    "Local_ResourceGathering_FPSMining_LowQuantity_Title_001": "Ayuda para un artista",
    "Local_ResourceGathering_FPSMining_MediumQuantity_Title_002": "Dos veces engañado",
    "Local_ResourceGathering_FPSMining_MediumQuantity_Title_003": "El novato necesita ayuda",
    "Local_ResourceGathering_Fauna_LowQuantity_Title_001": "Evítame el sobreprecio",
    "Local_ResourceGathering_Fauna_MediumQuantity_Title_001": "Gemas Marok urgentes",
    "Local_ResourceGathering_Fauna_MediumQuantity_Title_003": "Frena a los especuladores",
    "Local_ResourceGathering_GroundVehicleMining_LowQuantity_Title_001": "Emergencia en la granja",
    "Local_ResourceGathering_GroundVehicleMining_LowQuantity_Title_002": "Reparación tras la llamarada",
    "Local_ResourceGathering_GroundVehicleMining_MediumQuantity_Title_002": "Una apuesta arriesgada",
    "Local_ResourceGathering_Plants_LowQuantity_Title_002": "Pouchweed atrasada",
    "Local_ResourceGathering_Plants_MediumQuantity_Title_002": "Salva a este despistado",
    # Títulos de facciones y nombres de objetos de misión.
    "EckhartSecurity_ChainLocate_KillSingle_E_Title_001": "Expulsar a ~mission(TargetName)",
    "EckhartSecurity_KillMultiple_M_Title_001": "Aguar la fiesta",
    "EckhartSecurity_KillSingle_Locked_E_Title_001": "~mission(TargetName) no puede escapar",
    "EckhartSecurity_KillSingle_VE_Title_001": "Orden de cese: ~mission(TargetName)",
    "EckhartSecurity_Locate_KillSingle_Locked_H_Title_001": "Dar con ~mission(TargetName)",
    "EckhartSecurity_MultiEliminateAll_S_Title_001": "Acabar con la ocupación hostil",
    "EckhartSecurity_MultiEliminateAll_S_Title_003": "Detener la ocupación hostil",
    "EckhartSecurity_MultiLocate_KillSingle_H_Title_001": "Buscar a ~mission(TargetName)",
    "Headhunters_DestroyItems_Gas_Title_001": "Venganza por el secuestro",
    "Headhunters_DestroyItems_Supplies_Title_001": "Poner en su sitio a los advenedizos",
    "Headhunters_StealItems_Single_Locked_Title_001": "Golpe rápido",
    "Northrock_DestroyItems_Gas_Hostiles_Title_001": "Destruir combustible de forajidos",
    "Northrock_DestroyItems_Gas_Title_001": "Ataque al punto de paso",
    "Northrock_DestroyItems_Supplies_Hostiles_Title_001": "Demoler el depósito de suministros",
    "Northrock_DestroyItems_Supplies_Title_001": "Destruir suministros de forajidos",
    "RedWind_Courier_Nyx_SmallDelivery_Title": "Reparto bajo amenaza",
    "Vaughn_ChainLocate_KillSingle_Title_001": "Salvar la situación",
    "Vaughn_KillMultiple_Title_001": "Los necios se separan pronto",
    "Vaughn_KillSingle_Upload_Locked_Title_001": "Mantener el statu quo",
    "Vaughn_MultiLocate_KillSingle_Locked_Title_001": "Escarmentado",
    "Vaughn_MultiLocate_KillSingle_Title_002": "Un desafortunado lío",
    "UploadSabotage_Collect_obj_long": "Recoge la Virus Blade.",
    "UploadSabotage_Collect_obj_short": "Recoger Virus Blade",
    "UploadSabotage_Item": "Virus Blade",
    "UploadSabotage_obj_long_01": "Localiza el bastidor correcto e inserta la Virus Blade.",
    "UploadSabotage_obj_long_02": "Usa el terminal para insertar la Virus Blade.",
    "UploadSabotage_obj_short_02": "Insertar Virus Blade desde el terminal",
    "bhg_Locate-Kill_001_obj_01": "Acceder al monitor de bioseñales para hallar al objetivo",
    "bhg_Locate-Kill_001_obj_short_01": "Obtener información del terminal",
    "bhg_Locate-Kill_001_obj_short_02": "Localizar el terminal de datos",
    "bhg_Locate-Kill_Terminal_Id": "Monitor de bioseñales",
    "bhg_MultiLocate-Kill_001_obj_01": "Hallar el monitor con la ubicación del objetivo",
    "bhg_MultiLocate-Kill_001_obj_short_01": "Localizar el terminal correcto",
    "delivery_vehicle_exit_obj_long": "Sal de ~mission(Vehicle) para completar el contrato.",
    "delivery_vehicle_exit_obj_short": "Salir de ~mission(Vehicle)",
    "destroyitems_title_Starchitect": "Sabotear sus operaciones",
    # Cambios semánticos de la compilación 5.0.
    "Highpoint_RepUI_Description": "Highpoint Wilderness fue fundada por Terri Chauvet tras la disolución del departamento de Gestión Ecológica de la UEE y la privatización del control de fauna. Tras comprobar los graves problemas ambientales del imperio, desde infraestructuras que alteran el entorno hasta especies invasoras que destruyen ecosistemas, Terri fundó una empresa dedicada a proteger y controlar la fauna con un enfoque prudente y equilibrado.",
    "MWCH1_Main_Title": "Capítulo 1",
    "MWCH1_Main_Desc": "Usa tu acceso de seguridad de nivel 1 para entrar en Control de flujo y encontrar al ingeniero jefe desaparecido.",
    "Name_PotentialMarokLocation": "Marok",
    "Nyx1_Desc": "Nyx I es un planeta sin núcleo que orbita muy cerca del sol del sistema Nyx. Antes considerado imposible de terraformar, Nyx I ha cambiado radicalmente gracias a la tecnología experimental de Genesis Terraforming.\\n\\nMinerales para naves potenciales:\\nAgricium\\nAluminum\\nAslarite\\nBeryl\\nBexalite\\nCopper\\nGold\\nHephaestanite\\nLaranite\\nQuartz\\nSavrillium\\nTin\\nTitanium\\nTorite\\n\\nMinerales manuales potenciales:\\nAphorite\\nDolivine\\nSadaryx\\n\\nRecursos recolectables potenciales:\\nGatala Fungus\\nHeart of the Woods\\nPouchweed\\nSunset Berry\\n",
    "P2M1_delivery_dropoff_long": "Entrega los datos de anomalías energéticas en la taquilla de ~mission(Destination|Address).",
    "P2M1_delivery_dropoff_objectivedisplay": "Entregar datos de anomalías a ~mission(Destination)",
    "P2M1_delivery_dropoff_short": "Entregar datos de anomalías a ~mission(Destination)",
    "P2M2_delivery_dropoff_long": "Entrega los datos de seguridad en la taquilla de ~mission(Destination|Address).",
    "P2M3_delivery_dropoff_long": "Entrega los datos sísmicos en la taquilla de ~mission(Destination|Address).",
    "P2M4_delivery_dropoff_long": "Entrega los datos de consumo en la taquilla de ~mission(Destination|Address).",
    "P2M4_delivery_dropoff_marker": "Entregar datos de consumo",
    "P2M4_delivery_dropoff_objectivedisplay": "Entregar datos de consumo a ~mission(Destination)",
    "P2M4_delivery_dropoff_short": "Entregar datos de consumo a ~mission(Destination)",
    "location_delivery_target_item_port": "el punto marcado en %s",
    "mission_location_nyx_socialstation_002a_0": "People's Service Station Delta at NYX1 L1",
    # Descripciones de objetos nuevas que ya no son marcadores provisionales.
    "item_DescGPI_ReadableChip_Mission_ServerBlade_Sabotage": "Esta placa de servidor contiene un virus ejecutable capaz de borrar datos concretos.",
    "item_DescMRAI_Pulse_Mount_Gimbal": "Fabricante: Mirai\\nTipo: soporte de arma\\nTamaño: 2\\n\\nAlinea el disparo perfecto con este soporte cardán S2. Mirai lo diseñó para la Pulse y funciona junto a la ametralladora láser Thlilye.",
    "item_Desc_srvl_utility_medium_arms_01_01_01": "Tipo: armadura media\\nReducción de daño: 30 %\\nRango térmico: -65 / 80 °C\\nProtección contra radiación: 26000 REM\\nTasa de descontaminación: 145,8 REM/s\\n\\nMarca estilo con cuero grueso, puños metálicos, hombreras y guantes con púas.",
    "item_Desc_srvl_utility_medium_core_01_01_01": "Tipo: armadura media\\nReducción de daño: 30 %\\nRango térmico: -65 / 80 °C\\nProtección contra radiación: 26000 REM\\nTasa de descontaminación: 145,8 REM/s\\nCapacidad: 15k µSCU\\nMochilas: ligeras y medias\\n\\nQuienes viven en la frontera saben que sobrevivir es lo primero. La curtida armadura Outback combina cuero reforzado, una gruesa capucha y faldones superpuestos. No garantiza que veas otro día, pero te da una oportunidad de luchar.",
    "item_Desc_srvl_utility_medium_helmet_01_01_01": "Tipo: armadura media\\nReducción de daño: 30 %\\nRango térmico: -65 / 80 °C\\nProtección contra radiación: 26000 REM\\nTasa de descontaminación: 145,8 REM/s\\n\\nEste casco integral de cuero reforzado incorpora gafas oscuras y un respirador de alto rendimiento para entornos con poco oxígeno. La visera admite retículas de realidad aumentada.",
    "item_Desc_srvl_utility_medium_legs_01_01_01": "Tipo: armadura media\\nReducción de daño: 30 %\\nRango térmico: -65 / 80 °C\\nProtección contra radiación: 26000 REM\\nTasa de descontaminación: 145,8 REM/s\\nCapacidad: 10k µSCU\\n\\nEstos resistentes pantalones de cuero reforzado facilitan el avance por terrenos hostiles, mientras las botas con placas metálicas protegen durante el largo camino.",
    "item_Desc_hdtc_jacket_01_06_01": "Reducción de daño: 20 %\\nCapacidad: 0,4K µSCU\\n\\nElegante, funcional y letal: Bellator encaja tanto en una cena como en un tiroteo. El grafeno tejido en sus fibras aporta protección de combate, y el forro interior permite ocultar armas y dispositivos pequeños.\\n\\nLa edición Tuxedo combina negro clásico, solapas de satén, pañuelo blanco y un alfiler decorativo.",
    "item_Desc_hdtc_pants_01_07_01": "Reducción de daño: 20 %\\nCapacidad: 0,4K µSCU\\n\\nElegante, funcional y letal: Bellator encaja tanto en una cena como en un tiroteo. El grafeno tejido en estos pantalones entallados aporta protección de combate.\\n\\nLa edición Tuxedo luce negro clásico con una franja lateral de satén negro.",
    "item_Desc_hdtc_shirt_03_01_01": "Reducción de daño: 20 %\\n\\nElegante, funcional y letal: Bellator encaja tanto en una cena como en un tiroteo. Esta camisa con corbata de seda integra grafeno tejido para aportar protección de combate.\\n\\nLa edición Tuxedo combina camisa blanca y pajarita negra.",
    "item_Desc_hdtc_shirt_04_01_01": "Reducción de daño: 20 %\\n\\nElegante, funcional y letal: Bellator encaja tanto en una cena como en un tiroteo. La camisa, la corbata de seda y el chaleco entallado integran grafeno tejido para aportar protección de combate.\\n\\nLa edición Tuxedo combina chaleco negro, camisa blanca y pajarita negra.",
    "item_Desc_hdtc_shoes_01_07_01": "Los zapatos Spettro, fabricados a mano con cuero Quasi Grazer de primera calidad, son una incorporación elegante y refinada para cualquier armario. Su diseño clásico combina con cualquier atuendo formal.\\n\\nLa edición Tuxedo luce un negro pulido clásico.",
    "item_DescFlair_Model_Station_ICC_Probe_a": "Esta maqueta holográfica reproduce las sondas Deep Space Scanning & AstroGraphical construidas y operadas por el Imperial Cartography Center. Estas estaciones vigilan todos los rincones de la UEE en busca de posibles puntos de salto.",
    "item_DescFlair_Model_Station_IMS_Bolliver_a": "Esta maqueta holográfica muestra la estación IMS Bolliver. Construida en Sol durante la Primera Guerra Tevarin, debía servir como plataforma de infantería ante una posible invasión Tevarin.",
    "item_DescFlair_Model_Station_Icarus-One_a": "Esta maqueta holográfica muestra la estación de transferencia Icarus One. Construida en 2148 como escala entre la Tierra y Marte, acabó convertida en una estación civil para pioneros que querían comenzar una nueva vida.",
    "item_DescFlair_Model_Station_Port_Olisar_a": "Esta maqueta holográfica muestra Port Olisar. Operada por Crusader Industries, la estación daba acceso a sus astilleros orbitales de Stanton II y ofrecía vistas espectaculares del planeta.",
}

MODEL_INFO = {
    "item_DescFlair_Model_350r": ("Origin", "350r"),
    "item_DescFlair_Model_Aegis_Avenger": ("Aegis", "Avenger"),
    "item_DescFlair_Model_Aegis_Gladius": ("Aegis", "Gladius"),
    "item_DescFlair_Model_AuroraLN": ("RSI", "Aurora LN"),
    "item_DescFlair_Model_Constellation": ("RSI", "Constellation"),
    "item_DescFlair_Model_Freelancer": ("MISC", "Freelancer"),
    "item_DescFlair_Model_Hornet_F7C-R": ("Anvil", "Hornet F7C-R"),
    "item_DescFlair_Model_Khartu-Al": ("Aopoa", "Khartu-al"),
    "item_DescFlair_Model_M50": ("Origin", "M50"),
    "item_DescFlair_Model_Mustang_Alpha": ("CNOU", "Mustang Alpha"),
    "item_DescFlair_Model_Mustang_Beta": ("CNOU", "Mustang Beta"),
    "item_DescFlair_Model_Mustang_Delta": ("CNOU", "Mustang Delta"),
    "item_DescFlair_Model_Mustang_Gamma": ("CNOU", "Mustang Gamma"),
    "item_DescFlair_Model_Reliant": ("MISC", "Reliant"),
    "item_DescFlair_Model_Sabre": ("Aegis", "Sabre"),
    "item_DescFlair_Model_Starfarer": ("MISC", "Starfarer"),
}

MODEL_BOXES = {
    "item_DescFlair_Model_350r_Box": "350r",
    "item_DescFlair_Model_Aegis_Avenger_Box": "Avenger",
    "item_DescFlair_Model_Aegis_Gladius_Box": "Gladius",
    "item_DescFlair_Model_AuroraLN_Box": "Aurora LN",
    "item_DescFlair_Model_Constellation_Box": "Constellation",
    "item_DescFlair_Model_Freelancer_Box": "Freelancer",
    "item_DescFlair_Model_Hornet_F7C-R_Box": "Hornet F7C-R",
    "item_DescFlair_Model_Khartu-Al_Box": "Khartu'Al",
    "item_DescFlair_Model_M50_Box": "M50",
    "item_DescFlair_Model_Mustang_Alpha_Box": "Mustang Alpha",
    "item_DescFlair_Model_Mustang_Beta_Box": "Mustang Beta",
    "item_DescFlair_Model_Mustang_Delta_Box": "Mustang Delta",
    "item_DescFlair_Model_Mustang_Gamma_Box": "Mustang Gamma",
    "item_DescFlair_Model_Reliant_Box": "Reliant",
    "item_DescFlair_Model_Sabre_Box": "Sabre",
    "item_DescFlair_Model_Starfarer_Box": "Starfarer",
}

GOLD_MODELS = {
    "item_DescFlair_Model_Aurora_Gold": ("RSI", "Aurora"),
    "item_DescFlair_Model_Avenger_Gold": ("Aegis", "Avenger"),
    "item_DescFlair_Model_Constellation_Gold": ("RSI", "Constellation"),
    "item_DescFlair_Model_Freelancer_Gold": ("MISC", "Freelancer"),
    "item_DescFlair_Model_Herald_Gold": ("Drake", "Herald"),
    "item_DescFlair_Model_Hornet_Gold": ("Anvil", "Hornet"),
}


def item_description(specs: list[str], body: str, edition: str) -> str:
    """Compone una descripción de objeto con terminología uniforme."""
    return "\\n".join(specs) + "\\n\\n" + body + "\\n\\n" + edition


# Descripciones que CIG sustituyó por contenido real en 5.0. Se revisan a mano
# para evitar traducciones literales y conservar fabricantes, facciones y ediciones.
WARMONGER = (
    "La edición Warmonger luce el símbolo de Shattered Blade mediante cortes rojos "
    "pintados a mano sobre una base negra y plateada."
)
BLOODBATH = (
    "Con inquietantes cortes rojos sobre una superficie negra y plateada oscura, "
    "la edición Bloodbath infunde miedo a los enemigos de Shattered Blades."
)
DESOLATE = (
    "Habitual entre los cazadores veteranos de Shattered Blade, la edición Desolate "
    "combina una imponente pintura de guerra blanca con una base negra y plateada oxidada."
)
MARROW = (
    "La edición Marrow de Shattered Blades combina su base negra oxidada con un acabado "
    "rojo y amarillo desgastado, rematado con llamativos cortes blancos pintados a mano."
)
HAVOC = (
    "La edición Havoc incorpora piezas recuperadas con acabado dorado sobre negro y gris "
    "hierro, además de cortes blancos pintados a mano, para dar a quien la lleva en "
    "Shattered Blade un aspecto imponente."
)
OVERTHROW = (
    "Con pintura de guerra blanca de Shattered Blade sobre placas negras y plateadas "
    "oscuras, la edición Overthrow está hecha para imponer autoridad."
)
CHAIRMANS_CLUB = (
    "La edición Chairman's Club presenta un elegante acabado negro con costosos adornos "
    "dorados, inspirado en el club al que pertenece."
)

DOOM_BODY = (
    "Lo último de Doomsday en protección para la cabeza combina practicidad con el estilo "
    "característico de la marca. Incluye filtración integrada en una resistente máscara "
    "esquelética moldeada a mano, metal grueso pero ligero y protección ocular avanzada, "
    "sin que los inquietantes LED rojos afecten a la visión."
)
MONDE_BODY = (
    "De los maestros diseñadores de Kilgore & Poole llega la armadura pesada Monde. Sus "
    "placas de triple laminado integran la última tecnología defensiva para ofrecer "
    "protección de combate, gran comodidad y articulaciones flexibles especializadas."
)
ANTIUM_BODY = (
    "Esta armadura Antium modifica el modelo original con colmillos y huesos cuidadosamente "
    "seleccionados que le confieren un aspecto primitivo."
)
WRECKER_BODY = (
    "Favorita de los cazadores más brutales, la armadura Wrecker combina metal desechado "
    "y tela robada para proteger mientras se acecha a la presa. Lleva pintura naranja, "
    "fragmentos de hueso y piezas de armadura Vanduul."
)
CARRION_BODY = (
    "Forjada con metales recuperados y ropa desgarrada, la armadura Carrion es una tosca "
    "mezcla de materiales reutilizados que demuestra que harás lo necesario para sobrevivir."
)
AZTALAN_BODY = (
    "No temas a ninguna frontera con la armadura Aztalan. Sus placas y tejidos reforzados "
    "ofrecen protección y agilidad. El diseño de Tehachapi aporta un estilo fronterizo "
    "inconfundible y mucho espacio de almacenamiento, ideal para cualquier aventura."
)
CARNIFEX_BODY = (
    "Esta armadura improvisada ofrece una protección mínima, pero mucha actitud. Su "
    "diseño agresivo, con calaveras y accesorios intimidantes, puede mantener a la gente "
    "alejada… o atraerla."
)

OVERRIDES.update(
    {
        "item_Desc_cds_combat_heavy_backpack_01_02_01": item_description(
            ["Tipo: mochila pesada", "Capacidad: 150K µSCU", "Corazas compatibles: pesadas"],
            "Prepárate para cualquier situación con la mochila CSP-68H. Diseñada para las exigencias del apoyo en combate, destaca por su resistencia y por un conector patentado que la mantiene cómoda y equilibrada en la espalda.",
            MARROW,
        ),
        "item_Desc_doom_undersuit_helmet_01_02_01": item_description(
            ["Tipo: casco de vuelo", "Reducción de daño: 5 %", "Rango térmico: -30 a 60 °C", "Protección radiológica: 15 200 rem", "Tasa de eliminación radiológica: 81 rem/s"], DOOM_BODY, WARMONGER
        ),
        "item_Desc_doom_undersuit_helmet_01_03_01": item_description(
            ["Tipo: casco de vuelo", "Reducción de daño: 5 %", "Rango térmico: -30 a 60 °C", "Protección radiológica: 15 200 rem", "Tasa de eliminación radiológica: 81 rem/s"], DOOM_BODY, BLOODBATH
        ),
        "item_Desc_doom_undersuit_helmet_01_04_01": item_description(
            ["Tipo: casco de vuelo", "Reducción de daño: 5 %", "Rango térmico: -30 a 60 °C", "Protección radiológica: 15 200 rem", "Tasa de eliminación radiológica: 81 rem/s"], DOOM_BODY, DESOLATE
        ),
        "item_Desc_hdtc_utility_light_backpack_01_03_01": item_description(
            ["Tipo: mochila ligera", "Capacidad: 75K µSCU", "Corazas compatibles: todas"],
            "La Cataby es una elegante mochila de Hardin Tactical preparada para las aventuras más exigentes. Su estructura rectangular rígida protege un interior acolchado, resistente y ampliable, con dos bolsillos de cremallera para acceder rápidamente a lo esencial.", DESOLATE
        ),
        "item_Desc_qrt_combat_medium_backpack_02_03_01": item_description(
            ["Tipo: mochila media", "Capacidad: 105K µSCU", "Corazas compatibles: medias y pesadas"],
            "La mochila Testudo parece ligera como una pluma, pero soporta un peso considerable gracias al mismo blindaje resistente y liviano que emplea la armadura.", HAVOC
        ),
        "item_Desc_srvl_undersuit_01_02_01": item_description(
            ["Tipo: traje interior", "Reducción de daño: 5 %", "Rango térmico: -30 a 60 °C", "Protección radiológica: 15 200 rem", "Tasa de eliminación radiológica: 81 rem/s", "Tolerancia a fuerzas G: +90 %"],
            "Con la misma construcción relativamente fiable que el casco Why Not, el Second Life da una nueva vida a viejos trajes interiores desgastados.",
            "La edición Malice es habitual entre los reclutas de Shattered Blade."
        ),
    }
)

MACFLEX_BODY = (
    "Tanto en la superficie como en el vacío, la armadura industrial MacFlex de RSI te "
    "protege. Sus placas reforzadas resisten los peligros ambientales y sus bolsillos "
    "mantienen las herramientas al alcance."
)
for suffix, edition in {"02": WARMONGER, "03": BLOODBATH, "04": DESOLATE}.items():
    OVERRIDES[f"item_Desc_rsi_deckcrew_armor_light_legs_01_{suffix}_01"] = item_description(
        ["Tipo: armadura ligera", "Reducción de daño: 20 %", "Rango térmico: -37 a 67 °C", "Protección radiológica: 26 000 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Capacidad: 2,0 µSCU"],
        MACFLEX_BODY, edition
    )

for suffix, specs in {
    "arms": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -77 a 107 °C", "Protección radiológica: 26 800 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Capacidad: 7,5 µSCU"],
    "core": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -77 a 107 °C", "Protección radiológica: 26 800 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Capacidad: 12,0 µSCU", "Mochilas: todas"],
    "helmet": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -77 a 107 °C", "Protección radiológica: 26 800 rem", "Tasa de eliminación radiológica: 145,8 rem/s"],
    "legs": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -77 a 107 °C", "Protección radiológica: 26 800 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Capacidad: 7,5 µSCU"],
}.items():
    body = MONDE_BODY if suffix != "helmet" else MONDE_BODY.replace("armadura pesada Monde", "casco Monde").replace(" y articulaciones flexibles especializadas", "")
    OVERRIDES[f"item_Desc_kap_combat_heavy_{suffix}_02_11_01"] = item_description(specs, body, CHAIRMANS_CLUB)

for suffix, specs in {
    "arms": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -95 a 120 °C", "Protección radiológica: 52 800 rem", "Tasa de eliminación radiológica: 251,1 rem/s"],
    "core": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -95 a 120 °C", "Protección radiológica: 52 800 rem", "Tasa de eliminación radiológica: 251,1 rem/s", "Capacidad: 8,0 µSCU", "Mochilas: todas"],
    "helmet": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -85 a 115 °C", "Protección radiológica: 52 800 rem", "Tasa de eliminación radiológica: 251,1 rem/s"],
    "legs": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -95 a 120 °C", "Protección radiológica: 52 800 rem", "Tasa de eliminación radiológica: 251,1 rem/s", "Capacidad: 8,0 µSCU"],
}.items():
    OVERRIDES[f"item_Desc_qrt_combat_heavy_{suffix}_02_04_01"] = item_description(specs, ANTIUM_BODY, OVERTHROW)

for suffix, specs in {
    "arms": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -70 a 100 °C", "Protección radiológica: 26 800 rem", "Tasa de eliminación radiológica: 145,8 rem/s"],
    "core": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -70 a 100 °C", "Protección radiológica: 26 800 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Capacidad: 8K µSCU", "Mochilas: todas"],
    "helmet": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -70 a 100 °C", "Protección radiológica: 26 800 rem", "Tasa de eliminación radiológica: 145,8 rem/s"],
    "legs": ["Tipo: armadura pesada", "Reducción de daño: 40 %", "Rango térmico: -70 a 100 °C", "Protección radiológica: 26 800 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Capacidad: 8K µSCU"],
}.items():
    body = WRECKER_BODY if suffix != "helmet" else WRECKER_BODY.split(" Lleva", 1)[0] + " El casco cerrado incorpora cuatro sensores rojos que mantienen al portador conectado con su entorno."
    OVERRIDES[f"item_Desc_srvl_combat_heavy_{suffix}_03_04_01"] = item_description(specs, body, MARROW)

for suffix, specs in {
    "arms": ["Tipo: armadura media", "Reducción de daño: 30 %", "Rango térmico: -50 a 80 °C", "Protección radiológica: 26 400 rem", "Tasa de eliminación radiológica: 145,8 rem/s"],
    "core": ["Tipo: armadura media", "Reducción de daño: 30 %", "Rango térmico: -50 a 80 °C", "Protección radiológica: 26 400 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Capacidad: 8K µSCU", "Mochilas: medias y ligeras"],
    "helmet": ["Tipo: armadura media", "Reducción de daño: 30 %", "Rango térmico: -50 a 80 °C", "Protección radiológica: 26 400 rem", "Tasa de eliminación radiológica: 145,8 rem/s"],
    "legs": ["Tipo: armadura media", "Reducción de daño: 30 %", "Rango térmico: -50 a 80 °C", "Protección radiológica: 26 400 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Capacidad: 4K µSCU"],
}.items():
    body = CARRION_BODY if suffix != "helmet" else CARRION_BODY + " El casco tiene una cresta de barras de hierro y una visera opaca que permite ver con claridad sin mostrar el rostro."
    OVERRIDES[f"item_Desc_srvl_combat_medium_{suffix}_03_02_01"] = item_description(specs, body, HAVOC)

for suffix, edition in {"02": WARMONGER, "03": BLOODBATH, "04": DESOLATE}.items():
    OVERRIDES[f"item_Desc_thp_light_arms_01_{suffix}_01"] = item_description(
        ["Tipo: armadura ligera", "Reducción de daño: 20 %", "Rango térmico: -38 a 68 °C", "Protección radiológica: 26 000 rem", "Tasa de eliminación radiológica: 145,8 rem/s"], AZTALAN_BODY, edition
    )

for suffix, edition in {"06": WARMONGER, "07": BLOODBATH, "08": DESOLATE}.items():
    OVERRIDES[f"item_desc_gys_jacket_01_{suffix}_01"] = item_description(
        ["Tipo: armadura ligera", "Reducción de daño: 20 %", "Rango térmico: -5 a 38 °C", "Protección radiológica: 26 000 rem", "Tasa de eliminación radiológica: 145,8 rem/s", "Mochilas compatibles: ligeras"], CARNIFEX_BODY, edition
    )

# Rótulos de espacio muy limitado.
OVERRIDES.update(
    {
        "UploadSabotage_obj_short_01": "Buscar bastidor",
        "Local_ResourceGathering_GroundVehicleMining_MediumQuantity_Title_001": "Faltan existencias",
        "Local_ResourceGathering_FPSMining_MediumQuantity_Title_001": "Suministros urgentes",
        "Local_ResourceGathering_GroundVehicleMining_MediumQuantity_Title_002": "Apuesta difícil",
        "itemport_keycard_required_level_01": "Requiere pase de nivel 1",
        "itemport_keycard_required_level_02": "Requiere pase de nivel 2",
        "itemport_keycard_required_level_03": "Requiere pase de nivel 3",
        "UI_MF_Panel-Title_ATC-Monitor_01": "Monitor ATC_H01",
        "UI_MF_Panel-Title_ATC-Monitor_02": "Monitor ATC_D02",
        "UI_MF_Panel-Title_Sys-Overview": "Resumen sist.",
        "MWCH01_Obj2d_Short": "Desactivar puerta-fusible",
        "MWCH01_Obj7_Short": "Salir",
        "MWCH01_Obj7_Long": "Salir del recinto",
        "MWCH01_Obj3_Short": "Sobrevivir",
        "MWCH01_Obj3_Long": "Sobrevivir a First Legion",
        "MWPrologue_Obj1_Short": "Recuperar vestíbulo",
        "MWPrologue_Obj1_Long": "Recuperar vestíbulo",
        "MWCH01_Obj2d_Long": "Desactivar puerta-fusible",
        "bhg_Locate-Kill_001_obj_01": "Usar monitor para hallar objetivo",
        "MWPrologue_Obj2_Long": "Restaurar acceso",
        "MWPrologue_Obj1a_Short": "Eliminar hostiles del vestíbulo",
        "MWPrologue_Obj1a_Long": "Eliminar hostiles del vestíbulo",
        "starchitect_TER_M_BiosignMonitorLabel": "Seguimiento de personal",
        "MWPrologue_Exit_Short": "Salir del complejo",
        "MWCH01_Obj4_Short": "Ir a centrífuga",
        "MWCH01_Obj4_Long": "Ir a centrífuga",
        "MWCH01_Obj2c_Short": "Bajar pórtico desde terminal",
        "MWCH01_Obj2c_Long": "Bajar pórtico desde terminal",
        "DataDownload_Espionage_obj_short_01": "Buscar terminal y descargar",
        "interaction_condition_InSpace": "Fuera del espacio",
        "Adagio_LawfulSalvage_BuyInHuge_H_Title_001": "<EM4>[REP 200]</EM4> Gran salvamento: ~mission(Ship)",
        "Adagio_LawfulSalvage_BuyInSmall_E_Title_001": "<EM4>[REP 100]</EM4> Salvamento: ~mission(Ship)",
        "CB_URWG_G_Cornerstone_PowerOn-Relay_5Location_VH_Title_001": "Reactivar varios repetidores",
        "LingFamily_Delivery_Nyx_MiningGoodsNeeded_L_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Suministros mineros Ling (G)",
        "LingFamily_Delivery_Nyx_MiningGoodsNeeded_M_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Suministros mineros Ling (M)",
        "LingFamily_HaulCargo_1to5_SmallBitsReverse_L_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Recogida Ling multipunto (G)",
        "LingFamily_HaulCargo_1to5_SmallBitsReverse_M_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Recogida Ling multipunto (M)",
        "LingFamily_HaulCargo_1to5_SmallBits_L_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Reparto Ling multipunto (G)",
        "LingFamily_HaulCargo_1to5_SmallBits_M_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Reparto Ling multipunto (M)",
    }
)

# Cadenas que ya tenían anotaciones de recompensas y, por ello, no fueron
# detectadas como texto inglés exacto en la primera pasada.
OVERRIDES.update(
    {
        "Local_ResourceGathering_Fauna_MediumQuantity_Title_002": "Reposición médica urgente",
        "Headhunters_StealItems_Single_Title_001": "<EM4>[REP 100]</EM4> Golpe a la vieja escuela",
        "Headhunters_StealItems_Multi_Locked_Title_001": "<EM4>[REP 100]</EM4> Recuperar lo recuperado",
        "Northrock_RecoverCargo_Hostiles_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Devolver carga robada",
        "FTL_Courier_Nyx_MiningSupplies_Rank1_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> MENSAJERO: MINERÍA – EXP.: U",
        "FTL_Courier_Nyx_MiningSupplies_Rank1_Title_002": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> MENSAJERO: MINERÍA – EXP.: U",
        "FTL_Courier_Nyx_LocalSupplies_Rank1_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> MENSAJERO: SUMINISTROS – EXP.: U",
        "FTL_Courier_Nyx_LocalSupplies_Rank1_Title_002": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> MENSAJERO: SUMINISTROS – EXP.: U",
        "FTL_Courier_Nyx_RoundTheWorld_Rank2_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> RUTA DE MENSAJERÍA – EXP.: E",
        "FTL_Courier_Nyx_MultiDelivery_Rank1_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> MENSAJERO (1 A 3) – EXP.: E",
        "FTL_Courier_Nyx_MultiDeliveryReverse_Rank2_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> MENSAJERO (VARIOS A 1) – EXP.: E",
        "FTL_Courier_Nyx_MultiPickupDelivery_Rank2_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> MENSAJERO (RUTA MÚLTIPLE) – EXP.: E",
        "Shubin_Industrial_SMine_Nyx_MedQuantity_Ice_Hub_Title_001": "<EM4>[REP 100]</EM4> Pedido med.: materiales de nave",
        "Shubin_Industrial_SMine_Nyx_MedQuantity_Alum_Hub_Title_001": "<EM4>[REP 100]</EM4> Pedido med.: materiales de nave",
        "Shubin_Industrial_SMine_Nyx_MedQuantity_AlCopTinTia_Hub_Title_001": "<EM4>[REP 100]</EM4> Pedido med.: materiales de nave",
        "Shubin_Industrial_SMine_Nyx_IntroQuantity_Alum_Hub_Title_001": "<EM4>[REP 100]</EM4> Pedido peq.: materiales de nave",
        "Shubin_Industrial_GVMine_Nyx_MedQuantity_Glac_Hub_Title_001": "<EM4>[REP 100]</EM4> Pedido med.: materiales de vehículo",
        "Shubin_Industrial_GVMine_Nyx_MedQuantity_Glac_Feyn_Hub_Title_001": "<EM4>[REP 100]</EM4> Pedido med.: materiales de vehículo",
        "Shubin_Industrial_GVMine_Nyx_IntroQuantity_Glac_Hub_Title_001": "<EM4>[REP 100]</EM4> Pedido peq.: materiales de vehículo",
        "Shubin_Industrial_FPSMine_Nyx_MedQuantity_Apho_Doliv_Hub_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Pedido med.: minerales a mano",
        "Shubin_Industrial_FPSMine_Nyx_MedQuantity_Apho_Hub_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Pedido med.: materiales a mano",
        "Shubin_Industrial_FPSMine_Nyx_IntroQuantity_Apho_Hub_Title_001": "<EM4>[BP]</EM4> <EM4>[REP 100]</EM4> Pedido peq.: minerales a mano",
        "items_commodities_stolengoods_desc": "Propiedad obtenida ilegalmente.",
        "PU_BANISTER_ICC_F_MC_FindLocationMissionAccept_IG_002": "Me alegra saber de ti. Veamos el contrato… sí, esta vez no hay nada demasiado complicado: solo un escaneo localizado. Despliega una sonda, deja que haga su trabajo y trae los datos.",
        "PU_BANISTER_ICC_F_MC_TriangulateArriveatCrater_IG_001": "Vaya. Mira toda esa… ciencia. Me das mucha envidia, pero de la sana, de esa de que todos estamos en el mismo equipo.",
        "PU_BANISTER_ICC_F_MC_TriangulateArriveatCrater_IG_002": "Es precioso… Me encanta mi trabajo.",
        "PU_BANISTER_ICC_F_MC_GenericMissionUpdate_GP_003": "Atención, llega una actualización. ¡Sigue así! Confío en ti.",
        "PU_BANISTER_ICC_F_MC_ScanScanCompleteOneScanLeft_IG_001": "Ya casi hemos terminado. Solo falta un escaneo.",
        "BitZeros_DownloadSingle_Locked_Desc_001": "Hay un lote de datos comerciales muy valiosos en una cámara de <EM4>~mission(Location|Address)</EM4>. Sé que está ahí porque lo robamos hace tiempo y acabo de cerrar un trato con sus propietarios originales para recuperarlo. ¡Viva el capitalismo!\\n\\nEl lugar estará muy protegido, así que tendrás que acceder al terminal por cualquier medio y entregar los datos en <EM4>~mission(Destination|Target|Address)</EM4>.",
        "Hockrow_DestroyItems_Servers_EliminateAll_Desc_001": "Hockrow Agency\\nExpediente n.º KMZ49306\\nInvestigador principal: Arken Mallor\\n\\nResumen del caso:\\nUna investigación sobre una red clandestina de servidores que canaliza grandes cantidades de datos robados ha localizado su centro principal, designado para su demolición. Es muy probable que los responsables hayan instalado alarmas y respondan con violencia cuando se destruyan los servidores. Si ocurre, será imprescindible eliminar esas fuerzas para impedir que recuperen los datos.\\n\\nAcciones del investigador contratado:\\nAccede a las instalaciones de <EM4>~mission(Location|Address)</EM4>, destruye todos los servidores y elimina cualquier amenaza hostil que aparezca.\\n\\nNotas adicionales:\\nEs probable que los servidores dispongan de medidas antimanipulación y alarmas. Si detectan tu presencia, tienes autorización para usar fuerza extrema.",
        "Local_CourierSingle_Desc_011": "Busco a alguien que recoja unos efectos personales que dejé atrás al salir precipitadamente por un problema familiar. Solo necesito que lleves lo que no pude cargar a <EM4>~mission(Destination|Address)</EM4>.\\n\\nTe agradecería mucho la ayuda.\\n\\n<EM4>~mission(Owner)</EM4>",
        "Local_KillSingle_Desc_003": "<EM4>~mission(TargetName)</EM4> trabaja para las bandas locales. Presume de que nunca lo atraparán porque tiene comprada a la policía y sabe dónde están enterrados todos los cuerpos, incluido el de mi hermana pequeña.\\n\\nBusco a alguien dispuesto a entrar en <EM4>~mission(Location|Target|Address)</EM4> y enterrar allí a <EM4>~mission(TargetName)</EM4>.\\n\\n¿Eres tú?\\n\\n~mission(Owner)",
        "Local_KillSingle_Desc_004": "¿Puedes ayudarme? Lo he perdido todo y quiero devolvérsela al responsable en <EM4>~mission(Location|Address)</EM4>. El objetivo es <EM4>~mission(TargetName)</EM4>.\\n\\n<EM4>~mission(Owner|First)</EM4>",
        "Local_KillSingle_Desc_005": "No me queda nadie a quien acudir. Busco a alguien que se encargue de <EM4>~mission(TargetName)</EM4> en <EM4>~mission(Location|Address)</EM4>. Me salvarías la vida.\\n\\n<EM4>~mission(Owner)</EM4>",
        "Local_KillSingle_Desc_009": "Lo he intentado todo. <EM4>~mission(TargetName)</EM4> merece acabar colgado de una estaca y desangrado como un cerdo. Busco a alguien que le haga una visita en <EM4>~mission(Location|Name)</EM4>.\\n\\nNo lo pediría si no fuera en serio.\\n\\n<EM4>~mission(Owner|First)</EM4>",
        "Local_RecoverSingle_Desc_006": "Han localizado un <EM4>~mission(Item1)</EM4> robado en <EM4>~mission(Location|Address)</EM4>. Ofrezco un contrato para recuperarlo y entregarlo en <EM4>~mission(Destination|Target|Address)</EM4>.\\n\\nContacta conmigo si te interesa.\\n\\n<EM4>~mission(Owner)</EM4>",
        "Local_ResourceGathering_GroundVehicleMining_LowQuantity_Desc_001": "Busco Glacosite para una reparación urgente de la vivienda. Llévalo a <EM4>~mission(Destination|Address)</EM4> y nos salvarás la vida.\\n\\nGracias,\\n<EM4>~mission(Owner)</EM4>\\n",
        "Local_ResourceGathering_GroundVehicleMining_LowQuantity_Desc_002": "Una llamarada solar ha averiado todo el sistema de precursores de mi taller. Necesito a alguien que consiga Feynmaline y lo lleve a <EM4>~mission(Destination|Address)</EM4>.\\n\\nContacta conmigo si puedes.\\n\\n¡Gracias!\\n<EM4>~mission(Owner)</EM4>\\n",
    }
)

ADAGIO_DISCLAIMER = (
    "> Aviso <\\nLos contratistas deben asegurarse de recoger materiales de vehículos "
    "considerados salvamento legal por las leyes aplicables de la UEE. Adagio Holdings no "
    "se responsabiliza de los delitos cometidos por los contratistas ni indemnizará a las "
    "personas afectadas por sus acciones."
)
ADAGIO_REQUIREMENTS = (
    "> Requisitos <\\n     - Cualquier clase o tamaño de nave con espacio suficiente"
    "\\n     - Un haz tractor portátil"
)
OVERRIDES["Adagio_LawfulSalvage_BuyInHuge_H_Desc_001"] = (
    "Adagio Holdings\\nEmpleador comprometido con la igualdad de oportunidades"
    "\\n\\n> Sobre el trabajo <\\nSe ofrecen los derechos de una nueva reclamación de "
    "salvamento de gran tamaño y valor. Se recomienda disponer de una nave con una capacidad "
    "de carga muy elevada. La compra concede acceso exclusivo a las coordenadas del objetivo. "
    "El contrato seguirá activo y reservado al comprador hasta que este decida finalizarlo, "
    "sin penalización por cancelación anticipada. Al cancelarlo, las coordenadas desaparecerán "
    "del mapa estelar del operador.\\n\\n• NAVE: <EM4>~mission(Ship)</EM4>"
    "\\n• UBICACIÓN: <EM4>~mission(location)</EM4>\\n\\n"
    + ADAGIO_REQUIREMENTS + "\\n\\n" + ADAGIO_DISCLAIMER
)
OVERRIDES["Adagio_LawfulSalvage_BuyInLarge_M_Desc_001"] = (
    "Adagio Holdings\\nEmpleador comprometido con la igualdad de oportunidades"
    "\\n\\n> Sobre el trabajo <\\nSe han puesto a la venta los derechos de una nueva reclamación "
    "de salvamento. La compra permite acceder a las coordenadas de la nave objetivo, que serán "
    "exclusivas del comprador mientras el contrato esté activo. El contrato puede darse por "
    "completado en cualquier momento y retirar las coordenadas del mapa estelar sin penalización. "
    "Por la cantidad de material recuperable, no se recomienda esta reclamación a operadores de "
    "naves pequeñas.\\n\\n• NAVE: <EM4>~mission(Ship)</EM4>"
    "\\n• UBICACIÓN: <EM4>~mission(location)</EM4>\\n\\n"
    + ADAGIO_REQUIREMENTS + "\\n\\n" + ADAGIO_DISCLAIMER
)
OVERRIDES["Adagio_LawfulSalvage_BuyInSmall_E_Desc_001"] = (
    "Adagio Holdings\\nEmpleador comprometido con la igualdad de oportunidades"
    "\\n\\n> Sobre el trabajo <\\nEstán a la venta los derechos de una nueva reclamación de "
    "salvamento. Tras confirmar el pago, se facilitará acceso exclusivo a las coordenadas "
    "verificadas de la nave en espacio vigilado. Seguirán disponibles mientras el contrato esté "
    "activo y podrás finalizarlo antes de tiempo sin penalización; entonces se borrarán del mapa "
    "estelar.\\n\\nPara obtener consejos, consulta <EM4>Guía del recuperador para la "
    "recolección de materiales</EM4> en el diario de mobiGlas."
    "\\n\\n• NAVE: <EM4>~mission(Ship)</EM4>"
    "\\n• UBICACIÓN: <EM4>~mission(location)</EM4>\\n\\n"
    + ADAGIO_REQUIREMENTS + "\\n\\n" + ADAGIO_DISCLAIMER
)
OVERRIDES["Adagio_ResourceGathering_SmallList_VE_Desc_001"] = (
    "Adagio Holdings\\nEmpleador comprometido con la igualdad de oportunidades"
    "\\n\\n> Sobre el trabajo <\\nHay que desguazar una nave pequeña y llevar el RMC al "
    "ascensor de carga situado en <EM4>~mission(Destination|Address)</EM4>. Así daremos una "
    "segunda vida a estos materiales.\\n\\nPara obtener consejos, consulta <EM4>Guía del "
    "recuperador para la recolección de materiales</EM4> en el diario de mobiGlas."
    "\\n\\n> Requisitos <\\n     - Cualquier clase o tamaño de nave de salvamento"
    "\\n     - Un haz tractor portátil\\n\\n" + ADAGIO_DISCLAIMER
)
OVERRIDES["InterSec_ResourceGathering_Cryopods_Desc"] = (
    "ESPECIFICACIONES DE LA MISIÓN\\n\\nZona de operaciones: sistema Nyx"
    "\\nFuerzas hostiles: forajidos presentes y armados"
    "\\nEquipo: <EM4>nave con capacidad de carga</EM4>, armas personales y "
    "<EM4>haz tractor pesado</EM4>\\nInforme:\\nNuestros últimos datos indican que "
    "Shattered Blade ha repuesto sus existencias de cadáveres Vanduul y pronto los "
    "trasladará desde la antigua estación <EM4>QV Logistics</EM4> donde opera hasta un "
    "comprador interesado. La UEE no puede permitir otro incidente como el de ASD, así "
    "que quiere que <EM4>recuperemos las criocápsulas</EM4> y las entreguemos en "
    "<EM4>el ascensor de carga de ~mission(Destination|Address)</EM4>.\\n\\nLos miembros "
    "de Shattered Blade presentes podrían resistirse, pero no son el objetivo principal. "
    "Enfréntate a ellos si es necesario y recupera las criocápsulas."
    "\\n\\nAtentamente,\\n\\nDeacon Tobin\\nDirector de operaciones\\nInterSec Defense "
    "Solutions\\n\\nEsta comunicación contiene información confidencial destinada "
    "exclusivamente a su receptor. Si la recibes por error, ignórala y avisa al remitente. "
    "Todas las operaciones se realizan por cuenta y riesgo del contratista y deben cumplir "
    "las leyes de la UEE y del sistema aplicables."
)

BIOSIGN_KEYS = {
    "EckhartSecurity_ChainLocate_KillSingle_E_Desc_001",
    "EckhartSecurity_Locate_KillSingle_Locked_Download_S_Desc_001",
    "EckhartSecurity_Locate_KillSingle_Locked_H_Desc_001",
    "EckhartSecurity_Locate_KillSingle_Locked_Upload_S_Desc_001",
    "EckhartSecurity_Locate_KillSingle_VE_Desc_001",
    "EckhartSecurity_MultiLocate_KillMultiple_S_Desc_001",
    "EckhartSecurity_MultiLocate_KillSingle_E_Desc_001",
    "EckhartSecurity_MultiLocate_KillSingle_H_Desc_001",
    "EckhartSecurity_MultiLocate_KillSingle_Locked_VH_Desc_001",
    "Vaughn_MultiLocate_KillSingle_Desc_001",
    "Vaughn_MultiLocate_KillSingle_Desc_002",
}

for key, (manufacturer, ship) in MODEL_INFO.items():
    OVERRIDES[key] = (
        "Creada por Takuetsu Starships con láseres de precisión micrométrica, "
        f"esta maqueta acabada a mano reproduce la {ship} de {manufacturer} con gran detalle."
    )
for key, ship in MODEL_BOXES.items():
    OVERRIDES[key] = (
        f"Caja de coleccionista para la maqueta {ship}, con una imagen de la nave "
        "y detalles del modelo."
    )
for key, (manufacturer, ship) in GOLD_MODELS.items():
    OVERRIDES[key] = (
        "Creada por Takuetsu Starships con láseres de precisión micrométrica, "
        f"esta maqueta acabada a mano reproduce la {ship} de {manufacturer} con gran detalle. "
        "Esta exclusiva serie limitada luce un acabado bañado en oro."
    )


def normalize(key: str) -> str:
    return key[:-2] if key.endswith(",P") else key


def main() -> int:
    raw = GLOBAL_INI.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    output = []
    found = set()
    for line in text.splitlines():
        if "=" in line and not line.startswith((";", "[")):
            raw_key = line.split("=", 1)[0]
            key = normalize(raw_key)
            if key in OVERRIDES:
                current = line.split("=", 1)[1]
                value = OVERRIDES[key]
                if REWARD_HEADING in current and REWARD_HEADING not in value:
                    value += REWARD_HEADING + current.split(REWARD_HEADING, 1)[1]
                line = f"{raw_key}={value}"
                found.add(key)
            if key in BIOSIGN_KEYS:
                name, value = line.split("=", 1)
                value = value.replace("Biosign Monitors", "monitores de bioseñales")
                value = value.replace("Biosign Monitor", "monitor de bioseñales")
                value = value.replace("Monitores de Biosign", "monitores de bioseñales")
                value = value.replace("Monitores Biosign", "monitores de bioseñales")
                value = value.replace("CONTRATOS Y ENVÍO", "CONTRATOS Y DESPACHO")
                line = f"{name}={value}"
            if "=" in line:
                name, value = line.split("=", 1)
                value = value.replace("Transporte de la Familia Ling", "Ling Family Hauling")
                value = value.replace("Transporte Familiar Ling", "Ling Family Hauling")
                value = value.replace("Mudanzas de la Familia Ling", "Ling Family Hauling")
                value = value.replace("Agencia Hockrow", "Hockrow Agency")
                value = value.replace("Grupo de Servicios Northrock", "Northrock Service Group")
                value = value.replace("Primera Legión", "First Legion")
                value = value.replace("Primera legión", "First Legion")
                value = value.replace("Fabián", "Fabian")
                value = value.replace("rayo tractor portátil", "haz tractor portátil")
                value = value.replace("rayo tractor de mano", "haz tractor portátil")
                value = value.replace("rayo tractores portátil", "haz tractor portátil")
                value = value.replace("rayo tracción portátil", "haz tractor portátil")
                value = value.replace("haz de tractor de mano", "haz tractor portátil")
                value = value.replace("haz de tractor portátil", "haz tractor portátil")
                value = value.replace("haz tractor de mano", "haz tractor portátil")
                value = value.replace("rayo de tractor portátil", "haz tractor portátil")
                value = value.replace("rayo tractora de mano", "haz tractor portátil")
                value = value.replace("tractor de mano", "haz tractor portátil")
                value = value.replace("</EM4> un barco que", "</EM4> y una nave que")
                value = value.replace("un barco que", "una nave que")
                value = value.replace("espacio en su barco", "espacio en la nave")
                value = value.replace("El barco de nuestro mensajero", "La nave de nuestro mensajero")
                value = value.replace("traiga un barco", "traiga una nave")
                value = value.replace("Necesitamos algunos mozos de establo para trasladar", "Necesitamos pilotos fiables para trasladar")
                value = value.replace("estos son el tipo de contratos favoritos", "este es el tipo de contratos favorito")
                value = value.replace("realmente apreciaríamos una mano", "agradeceríamos mucho la ayuda")
                value = value.replace("¡Hay que amar cuando llega un pedido grande!", "¡Da gusto cuando llega un pedido grande!")
                value = value.replace("Coordinador de Envíos\\nLing Family Hauling", "Coordinadora de Envíos\\nLing Family Hauling")
                value = value.replace("Coordinadora de Envios", "Coordinadora de Envíos")
                value = value.replace("Una banda ha hecho un golpe con algunos restos del mercado negro", "Una banda ha dado un golpe y se ha apoderado de mercancía de salvamento del mercado negro")
                value = value.replace("disfrutar el aumento de su reputación", "disfrutar de su aumento de reputación")
                value = value.replace("lo lejos que estamos por encima de su nivel", "lo muy por encima que estamos")
                value = value.replace("Las coordenadas exactas del envío son dudosas", "Las coordenadas exactas del cargamento son imprecisas")
                value = value.replace("ha sido dividido entre al menos un par de lugares", "lo han dividido entre al menos un par de lugares")
                value = value.replace("un boleto caro <EM4>~mission(Item)</EM4>", "un valioso <EM4>~mission(Item)</EM4>")
                value = value.replace("Sea como sea que lo consiguieron, creo que es hora de que encuentre un hogar más adecuado con los Headhunters -", "Como sea que lo consiguieran, ya es hora de que encuentre un hogar más apropiado con los Headhunters:")
                value = value.replace("No puedo decir qué tan estricta será la seguridad", "No sé lo estricta que será la seguridad")
                value = value.replace("Ve por ellos.\\n\\nStows fuera.", "Ve a por él.\\n\\nStows, fuera.")
                value = value.replace("\\n\\nSe acabó.", "\\n\\nStows, fuera.")
                value = value.replace("VIAJE – Todas las necesidades de transporte deben ser organizadas por el mensajero.", "VIAJE – El mensajero debe organizar el transporte.")
                value = value.replace("VIAJE – Todos los medios de transporte deben ser organizados por el mensajero.", "VIAJE – El mensajero debe organizar el transporte.")
                value = value.replace("VIAJE – Todos los medios de transporte deben ser gestionados por el mensajero.", "VIAJE – El mensajero debe organizar el transporte.")
                value = value.replace("VIAJES: Todas las necesidades de transporte deben ser arregladas por mensajería.", "VIAJE – El mensajero debe organizar el transporte.")
                if key == "Covalex_HaulCargo_AToB_Nyx_MassResource_Reverse_Desc":
                    value = value.replace(
                        "<EM4>~mission(Location|Target|Address) a <EM4>~mission(Destination|Address)</EM4>",
                        "<EM4>~mission(Location|Target|Address) a ~mission(Destination|Address)</EM4>",
                    )
                line = f"{name}={value}"
        output.append(line)
    missing = set(OVERRIDES) - found
    if missing:
        raise SystemExit(f"Claves no encontradas: {sorted(missing)}")
    encoded = (newline.join(output) + newline).encode("utf-8")
    GLOBAL_INI.write_bytes((b"\xef\xbb\xbf" if bom else b"") + encoded)
    print(f"Aplicadas: {len(found)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
