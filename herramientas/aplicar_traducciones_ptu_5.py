#!/usr/bin/env python3
"""Aplica traducciones revisadas específicas del catálogo PTU 5.0."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GLOBAL_INI = ROOT / "global.ini"

TRANSLATIONS = {
    # Terminales de Starchitect. Los nombres generados de ubicaciones se conservan en inglés.
    "starchitect_TER_M_AccessComplete,P": "Acceso completado",
    "starchitect_TER_M_AccessProgress,P": "Progreso del acceso",
    "starchitect_TER_M_AccessingData,P": "Accediendo a los datos",
    "starchitect_TER_M_Authenticating,P": "Autenticando...\\n",
    "starchitect_TER_M_BiosignFound,P": "Bioseñal encontrada",
    "starchitect_TER_M_BiosignMonitor,P": "Monitor de bioseñales",
    "starchitect_TER_M_BiosignMonitorLabel,P": "Sistema de seguimiento de personal en tiempo real",
    "starchitect_TER_M_BiosignNotFound,P": "Bioseñal no encontrada",
    "starchitect_TER_M_DataStorage,P": "Almacenamiento de datos",
    "starchitect_TER_M_DataStorageLabel,P": "Conserva los archivos digitales esenciales",
    "starchitect_TER_M_DiagnosticTerminal,P": "Terminal de diagnóstico",
    "starchitect_TER_M_DiagnosticsLabel,P": "Estado actual del sistema",
    "starchitect_TER_M_DriveEjected,P": "Unidad externa expulsada",
    "starchitect_TER_M_EjectingDrive,P": "Expulsando unidad externa",
    "starchitect_TER_M_ExtDriveDetected,P": "Unidad externa detectada",
    "starchitect_TER_M_InsertBlade,P": "Insertar módulo",
    "starchitect_TER_M_Install,P": "Instalar",
    "starchitect_TER_M_InstallComplete,P": "Instalación completada",
    "starchitect_TER_M_Installing,P": "Instalando...",
    "starchitect_TER_M_LocateBiosign,P": "Localizar bioseñal",
    "starchitect_TER_M_LockedDoorFluff,P": "// BLOQUEADO // BLOQUEADO // BLOQUEADO // BLOQUEADO // BLOQUEADO // BLOQUEADO //",
    "starchitect_TER_M_NewExecutableDetected,P": "Nuevo ejecutable detectado",
    "starchitect_TER_M_PersonnelOffsite,P": "El personal está fuera de las instalaciones",
    "starchitect_TER_M_ProcessingDoorFluff,P": "// PROCESANDO // PROCESANDO // PROCESANDO // PROCESANDO // PROCESANDO //",
    "starchitect_TER_M_RunProgram": "Ejecutar programa",
    "starchitect_TER_M_ServiceNode,P": "Nodo de servicio",
    "starchitect_TER_M_ServiceNodeLabel,P": "Gestión de datos y red del sistema",
    "starchitect_TER_M_TransferProcess,P": "Proceso de transferencia",
    "starchitect_TER_M_TransferringData,P": "Transfiriendo datos",
    "starchitect_TER_M_TransferringToDrive,P": "Transfiriendo a la unidad externa",
    "starchitect_TER_M_UploadingCoordinates,P": "Subiendo coordenadas...",

    # Tablones y contratos.
    "MB_Applicant,P": "Solicitante",
    "MB_AssetsReward,P": "Recompensas de objetos",
    "MB_BlueprintRewards,P": "Recompensas de planos",
    "MB_CareerBoard,P": "Contratos de gremio",
    "MB_ContractAccepted,P": "Contrato aceptado",
    "MB_ContractLimitReached,P": "Límite de contratos alcanzado: %i/%i",
    "MB_ContractNoLongerAvailable,P": "El contrato ya no está disponible",
    "MB_FindLocalWorkHere,P": "Buscar trabajo local aquí",
    "MB_GlobalContract,P": "Contrato global",
    "MB_InteractToViewContracts,P": "Interactúa para ver los contratos",
    "MB_LocalContract,P": "Contrato local",
    "MB_LocalContracts,P": "Contratos locales",
    "MB_NegativePopupMessage1,P": "El contrato ya no está disponible",
    "MB_NoContractsAvailable,P": "No hay contratos disponibles actualmente\\nSelecciona otra pestaña",
    "MB_NoticeBoard,P": "Contratos personales",
    "MB_PositivePopupMessage1,P": "Contrato aceptado y añadido al mobiGlas",
    "MB_RegionalContract,P": "Contrato regional",
    "MB_ReputationRewards,P": "Recompensas de reputación",
    "MB_SelectContractToView,P": "Selecciona un contrato para ver los detalles",
    "MB_SponsoredBy,P": "Patrocinado por",
    "MB_UseTerminalBelow,P": "Usa el terminal para contactar con personas cercanas que necesitan ayuda.",
    "MB_ViewContracts,P": "Ver contratos",

    # Ascensores de carga.
    "FreightElevator_ClaimMode_ExternalFilterName,P": "Ocultar objetos locales",
    "FreightElevator_ItemTransferFailed_MissionOrdersFailed": "No se han podido actualizar los contratos de misión. Inténtalo de nuevo más tarde.",
    "FreightElevator_ItemTransferFailed_TooManyItems": "Hay demasiados objetos sueltos. Agrúpalos en contenedores.",
    "FreightElevator_ItemTransferFailed_TransfersFailed": "Se ha producido un error al transferir uno o varios objetos.",
    "FreightElevator_ItemTransferFailed_UnstowingFailed": "Se ha producido un error al colocar los objetos en la plataforma.",
    "FreightElevator_ItemValidationFailed_Mission": "No se pueden guardar aquí los objetos de misión.",
    "FreightElevator_ItemValidationFailed_Stolen": "No se pueden guardar aquí los objetos robados.",
    "FreightElevator_ProcessingItemTransfers": "Procesando transferencias de objetos...",
    "FreightElevator_ProcessingOrders": "Procesando los datos del contrato...",
    "FreightElevator_ProcessingUnstowing": "Colocando objetos en la plataforma...",
    "FreightElevator_RaisingElevator": "Subiendo el ascensor...",

    # Mapas y fabricación.
    "Maps_Amenities_CareerBoard_AcademyOfSciences,P": "Contratos de AOS",
    "Maps_Amenities_CareerBoard_InterstellarTransportGuild,P": "Contratos de ITG",
    "Maps_Amenities_CareerBoard_MercenaryGuild,P": "Contratos mercenarios",
    "Maps_Amenities_CareerBoard_UnitedResourceWorkers,P": "Contratos de URW",
    "Maps_Amenities_NoticeBoard,P": "Contratos personales",
    "Maps_KeyHint_Ping,P": "Pulso",
    "Maps_Ping,P": "Pulso",
    "Maps_Tooltips_Untracked,P": "Mostrar u ocultar las misiones sin seguimiento.",
    "Maps_Zoom,P": "Zoom",
    "crafting_ui_modifier_source_from,P": "de",
    "crafting_ui_modifier_source_gameplaystat,P": "Estadística",
    "crafting_ui_modifier_source_machine,P": "Máquina",
    "crafting_ui_time_modifier_blueprint,P": "Plano",

    # Objetivos reutilizados por las nuevas misiones.
    "AttackDestructibleEntities_AttackLong,P": "Alcanza y destruye los ~mission(Objects) marcados.",
    "AttackDestructibleEntities_AttackObj": "~mission(Objects) destruidos",
    "AttackDestructibleEntities_AttackObjectiveMarker": "Ubicación de ~mission(Objects)",
    "AttackDestructibleEntities_AttackShort,P": "Alcanza y destruye ~mission(Objects)",
    "AttackDestructibleEntities_LocateAttackLong": "Localiza y destruye los ~mission(Objects) marcados.",
    "AttackDestructibleEntities_LocateAttackShort": "Localiza y destruye ~mission(Objects)",
    "Cornerstone_Powerable_Collect_obj_long_01": "Recoge un depósito de plasma.",
    "Cornerstone_Powerable_Collect_obj_marker_01": "Depósito de plasma",
    "Cornerstone_Powerable_Collect_obj_short_01": "Recoge el depósito de plasma",
    "Cornerstone_Powerable_EquipmentId_Antenna": "Antena de comunicaciones",
    "Cornerstone_Powerable_EquipmentId_Extractor": "Extractor minero",
    "Cornerstone_Powerable_EquipmentId_Relay": "Repetidor planetario",
    "Cornerstone_Powerable_EquipmentId_Sprinkler": "Aspersor",
    "Cornerstone_Powerable_obj_long_01": "Activa ~mission(EquipmentId).",
    "Cornerstone_Powerable_obj_short_01": "Activa ~mission(EquipmentId)",
    "DataDownload_Diagnostics_Terminal,P": "Terminal de diagnóstico",
    "DataDownload_Diagnostics_item,P": "Disco de datos",
    "DataDownload_Espionage_Terminal,P": "Terminal de datos",
    "DataDownload_Espionage_item,P": "Disco de datos",
    "DataDownload_Espionage_obj_long_01,P": "Encuentra el terminal y descarga los datos en el disco de almacenamiento.",
    "DataDownload_Espionage_obj_long_02,P": "Ve al terminal y descarga los datos en el disco de almacenamiento.",
    "DataDownload_Espionage_obj_short_01,P": "Encuentra el terminal y descarga los datos",
    "DataDownload_Espionage_obj_short_02,P": "Ve al terminal y descarga los datos",
    "EliminateAll_obj_long_01": "Elimina a todos los hostiles en ~mission(Location|Address).",
    "EliminateAll_obj_long_02": "Elimina a todos los hostiles en ~mission(Location01|Address).",
    "EliminateAll_obj_long_03": "Elimina a todos los hostiles en ~mission(Location02|Address).",
    "EliminateAll_obj_marker_01": "Eliminar",
    "EliminateAll_obj_short_01": "Elimina a los hostiles en ~mission(Location)",
    "EliminateAll_obj_short_02": "Elimina a los hostiles en ~mission(Location01)",
    "EliminateAll_obj_short_03": "Elimina a los hostiles en ~mission(Location02)",
    "KillShip_EliminateMulti_Long_01,P": "Elimina a los objetivos",
    "KillShip_EliminateMulti_Short_01,P": "Elimina a los objetivos",
    "KillShip_Eliminate_Long_01,P": "Elimina a ~mission(Target).",
    "KillShip_Eliminate_Short_01,P": "Elimina a ~mission(Target)",
    "LocateKill_TravelObjective_Long": "~mission(TargetName) se encuentra en ~mission(Location|Address).",
    "LocateKill_TravelObjective_Short": "~mission(TargetName) localizado en ~mission(Location)",

    # Títulos de contratos de Adagio Holdings.
    "Adagio_LawfulSalvage_BuyInHuge_H_Title_001": "Oferta importante de salvamento: ~mission(Ship)",
    "Adagio_LawfulSalvage_BuyInLarge_M_Title_001": "Nueva concesión de salvamento: ~mission(Ship)",
    "Adagio_LawfulSalvage_BuyInSmall_E_Title_001": "Derechos de salvamento disponibles: ~mission(Ship)",
    "Adagio_RecoverComponent_Cooler_E_Title_001": "Recogida de refrigerador",
    "Adagio_RecoverComponent_Cooler_H_Title_001": "Pedido de refrigerador usado",
    "Adagio_RecoverComponent_Cooler_M_Title_001": "Recogida de refrigerador recuperado",
    "Adagio_RecoverComponent_Powerplant_E_Title_001": "Recogida de planta de energía",
    "Adagio_RecoverComponent_Powerplant_H_Title_001": "Pedido de planta de energía usada",
    "Adagio_RecoverComponent_Powerplant_M_Title_001": "Recogida de planta de energía recuperada",
    "Adagio_RecoverComponent_Quantum_E_Title_001": "Recogida de motor cuántico",
    "Adagio_RecoverComponent_Quantum_H_Title_001": "Pedido de motor cuántico usado",
    "Adagio_RecoverComponent_Quantum_M_Title_001": "Recogida de motor cuántico recuperado",
    "Adagio_RecoverComponent_Shield_E_Title_001": "Recogida de generador de escudos",
    "Adagio_RecoverComponent_Shield_H_Title_001": "Pedido de generador de escudos usado",
    "Adagio_RecoverComponent_Shield_M_Title_001": "Recogida de generador de escudos recuperado",
    "Adagio_ResourceGathering_LrgList_H_Title_001": "Gran encargo de salvamento",
    "Adagio_ResourceGathering_MedList_M_Title_001": "Encargo de salvamento de un cliente nuevo",
    "Adagio_ResourceGathering_SmallList_E_Title_001": "Encargo de salvamento",
    "Adagio_ResourceGathering_SmallList_VE_Title_001": "Encargo de salvamento (RMC)",

    # Títulos de Bit Zeros.
    "BitZeros_DestroyGenerators_EliminateAll_Title_001": "Destruye los generadores y elimina a los hostiles",
    "BitZeros_DestroyItems_EliminateAll_Title_001": "Sabotaje sin contemplaciones",
    "BitZeros_DestroyItems_EliminateSpecific_Title_001": "Entrega de karma",
    "BitZeros_DestroyItems_Generators_Title_001": "¿Te apetece destruir?",
    "BitZeros_DestroyItems_Multiple_Title_001": "Daños materiales",
    "BitZeros_DestroyItems_Servers_Locked_Title_001": "Demoler servidores",
    "BitZeros_DestroyItems_Servers_Title_001": "Operación de demolición",
    "BitZeros_DestroyItems_Upload_Title_001": "Borrado total",
    "BitZeros_DownloadMultiple_Title_001": "El triple de datos, el triple de emoción",
    "BitZeros_DownloadSingle_Title_001": "Un jugoso robo de datos",
    "BitZeros_UploadMultiple_Title_001": "Infectar y destruir",
    "BitZeros_UploadSingle_Locked_Title_001": "Infiltrarse e infectar",
    "BitZeros_UploadSingle_Title_001": "Una dura lección",

    # Títulos y acciones de Cornerstone Maintenance.
    "CB_URWG_G_Cornerstone_Diagnostics_Download_Single_H_Title_001": "Se necesita personal para ejecutar un diagnóstico",
    "CB_URWG_G_Cornerstone_PowerOn-Antenna_3Locations_H_Title_001": "Se necesita reactivar varias antenas",
    "CB_URWG_G_Cornerstone_PowerOn-Extractor_Multi_M_Title_001": "Varios extractores mineros necesitan baterías",
    "CB_URWG_G_Cornerstone_PowerOn-Relay_3Location_H_Title_001": "Se necesitan baterías para varios repetidores",
    "CB_URWG_G_Cornerstone_PowerOn-Relay_5Location_VH_Title_001": "Se necesita personal para reactivar numerosos repetidores",
    "CB_URWG_L_Cornerstone_Diagnostics_Download_Single_E_Title_001": "Se necesita descargar un diagnóstico",
    "CB_URWG_L_Cornerstone_PowerOn-Antenna_Single_E_Title_001": "Cambio rápido del fusible de una antena",
    "CB_URWG_L_Cornerstone_PowerOn-Extractor_Single_E_Title_001": "Ayuda con un extractor minero",
    "CB_URWG_L_Cornerstone_PowerOn-Sprinkler_Single_E_Title_001": "Un aspersor necesita un fusible nuevo",
    "CB_URWG_R_Cornerstone_Diagnostics_Download_Single_M_Title_001": "Se necesitan datos de diagnóstico",
    "CB_URWG_R_Cornerstone_PowerOn-Antenna_Multi_M_Title_001": "Varias antenas necesitan energía",
    "CB_URWG_R_Cornerstone_PowerOn-Extractor_Multi_H_Title_001": "Cambio de baterías para varios extractores mineros",
    "CB_URWG_R_Cornerstone_PowerOn-Relay_Single_M_Title_001": "Un repetidor planetario necesita energía",
    "CB_URWG_R_Cornerstone_PowerOn-Sprinkler_Multi_M_Title_001": "Varios aspersores necesitan energía",
    "Cornerstone_DownloadData_E_Title_001": "Informe de estado actualizado",

    # Títulos de transporte de Covalex.
    "Covalex_HaulCargo_1to3_AidConstruction_Reverse_L_Title_001": "Gran reparto de materiales de construcción",
    "Covalex_HaulCargo_1to3_AidConstruction_Reverse_M_Title_001": "Reparto mediano de materiales de construcción",
    "Covalex_HaulCargo_1to3_AidConstruction_Reverse_Title": "Pequeño reparto de materiales de construcción",
    "Covalex_HaulCargo_1to3_ResourceRequired_L_Title_001": "Gran reparto de suministros",
    "Covalex_HaulCargo_1to3_ResourceRequired_M_Title_001": "Reparto mediano de suministros",
    "Covalex_HaulCargo_1to3_ResourceRequired_Reverse_L_Title_001": "Gran recogida de suministros en varios puntos",
    "Covalex_HaulCargo_1to3_ResourceRequired_Reverse_M_Title_001": "Recogida mediana de suministros en varios puntos",
    "Covalex_HaulCargo_1to3_ResourceRequired_Reverse_Title": "Pequeña recogida de suministros en varios puntos",
    "Covalex_HaulCargo_1to3_ResourceRequired_Title_001": "Pequeño reparto de suministros",
    "Covalex_HaulCargo_3to1_AidConstruction_L_Title_001": "Gran recogida de materiales de construcción",
    "Covalex_HaulCargo_3to1_AidConstruction_M_Title_001": "Recogida mediana de materiales de construcción",
    "Covalex_HaulCargo_3to1_AidConstruction_Title": "Pequeña recogida de materiales de construcción",
    "Covalex_HaulCargo_AToB_Nyx_MassResource_L_Title_001": "Gran entrega de suministros al planeta",
    "Covalex_HaulCargo_AToB_Nyx_MassResource_M_Title_001": "Entrega mediana de suministros al planeta",
    "Covalex_HaulCargo_AToB_Nyx_MassResource_Reverse_L_Title_001": "Gran entrega extraplanetaria de suministros mineros",
    "Covalex_HaulCargo_AToB_Nyx_MassResource_Reverse_M_Title_001": "Entrega mediana extraplanetaria de suministros mineros",
    "Covalex_HaulCargo_AToB_Nyx_MassResource_Reverse_Title": "Pequeña entrega extraplanetaria de suministros mineros",
    "Covalex_HaulCargo_AToB_Nyx_MassResource_Title": "Pequeña entrega de suministros al planeta",

    # Títulos de la agencia Hockrow.
    "Hockrow_DestroyItems_Generators_Title_001": "Contrato de demolición de generadores",
    "Hockrow_DestroyItems_Servers_EliminateAll_Title_001": "Ataque total contra servidores",
    "Hockrow_DestroyItems_Servers_Locked_Title_001": "Destruir servidores con propiedad intelectual robada",
    "Hockrow_DestroyItems_Servers_Multiple_Title_001": "Ataque a hardware en varias ubicaciones",
    "Hockrow_DestroyItems_Servers_Title_001": "Ataque contra servidores: tierra quemada",
    "Hockrow_DestroyItems_Upload_Locked_Title_001": "Borrar datos y retirar el hardware",
    "Hockrow_DownloadMultiple_Title_001": "Recuperar datos de varias ubicaciones",
    "Hockrow_DownloadSingle_Locked_Title_001": "Recuperar datos pirateados",
    "Hockrow_DownloadSingle_Title_001": "Recuperación de datos confidenciales",
    "Hockrow_MissingPerson_Campsite_Local_Title_001": "Campista desaparecido: ~mission(TargetName)",
    "Hockrow_MissingPerson_Campsite_Regional_Title_001": "Explorador desaparecido: ~mission(TargetName)",
    "Hockrow_MissingPerson_Title_001": "Desaparecido: ~mission(TargetName)",
    "Hockrow_RecoverItem_Multiple_Title_001": "Recuperación en varias ubicaciones",
    "Hockrow_RecoverItem_Single_Title_001": "Recuperar la carga",
    "Hockrow_RecoverSingle_Title_001": "Recuperar un objeto de gran valor",
    "Hockrow_UploadMultiple_Title_001": "Borrado de servidores en red",
    "Hockrow_UploadSingle_EliminateAll_Title_001": "Borrado total de datos",
    "Hockrow_UploadSingle_Locked_Title_001": "Cargar un virus en un servidor clandestino",
    "Hockrow_UploadSingle_Title_001,P": "Purga del servidor",

    # Títulos de Ling Family Hauling.
    "LingFamilyHauling_Delivery_Nyx_MiningGoodsNeeded_Title": "Entrega de suministros mineros de Ling",
    "LingFamilyHauling_Delivery_Nyx_RelocatePersonalEffects_Title": "Traslado de carga de Ling",
    "LingFamilyHauling_Delivery_Nyx_SmallOreDelivery_Title": "Envío de mineral de Ling",
    "LingFamilyHauling_HaulCargo_1to5_SmallBitsReverse_Title": "Recogida de Ling en varios puntos",
    "LingFamilyHauling_HaulCargo_1to5_SmallBits_Title": "Reparto de Ling en varios puntos",
    "LingFamilyHauling_RecoverVehicle_Safe_Title": "Traslado de vehículo de Ling",
    "LingFamily_Delivery_Nyx_MiningGoodsNeeded_L_Title_001": "Entrega de suministros mineros de Ling (grande)",
    "LingFamily_Delivery_Nyx_MiningGoodsNeeded_M_Title_001": "Entrega de suministros mineros de Ling (mediana)",
    "LingFamily_Delivery_Nyx_RelocatePersonalEffects_L_Title_001": "Traslado de carga de Ling (grande)",
    "LingFamily_Delivery_Nyx_RelocatePersonalEffects_M_Title_001": "Traslado de carga de Ling (mediano)",
    "LingFamily_Delivery_Nyx_SmallOreDelivery_L_Title_001": "Envío de mineral de Ling (grande)",
    "LingFamily_Delivery_Nyx_SmallOreDelivery_M_Title_001": "Envío de mineral de Ling (mediano)",
    "LingFamily_HaulCargo_1to5_SmallBitsReverse_L_Title_001": "Recogida de Ling en varios puntos (grande)",
    "LingFamily_HaulCargo_1to5_SmallBitsReverse_M_Title_001": "Recogida de Ling en varios puntos (mediana)",
    "LingFamily_HaulCargo_1to5_SmallBits_L_Title_001": "Reparto de Ling en varios puntos (grande)",
    "LingFamily_HaulCargo_1to5_SmallBits_M_Title_001": "Reparto de Ling en varios puntos (mediano)",
}


def main() -> int:
    raw = GLOBAL_INI.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw[3:].decode("utf-8") if has_bom else raw.decode("utf-8")
    seen: set[str] = set()
    changed = 0
    output: list[str] = []

    for raw_line in text.splitlines(keepends=True):
        content = raw_line.rstrip("\r\n")
        ending = raw_line[len(content):]
        if "=" not in content:
            output.append(raw_line)
            continue
        key, value = content.split("=", 1)
        if key in TRANSLATIONS:
            seen.add(key)
            replacement = TRANSLATIONS[key]
            if value != replacement:
                content = f"{key}={replacement}"
                changed += 1
        output.append(content + ending)

    missing = sorted(TRANSLATIONS.keys() - seen)
    if missing:
        raise SystemExit("No se encontraron estas claves: " + ", ".join(missing))

    encoded = "".join(output).encode("utf-8")
    GLOBAL_INI.write_bytes((b"\xef\xbb\xbf" if has_bom else b"") + encoded)
    print(f"Traducciones aplicadas o verificadas: {len(TRANSLATIONS)}")
    print(f"Valores modificados: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
