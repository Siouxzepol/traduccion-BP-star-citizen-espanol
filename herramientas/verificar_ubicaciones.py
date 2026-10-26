#!/usr/bin/env python3
"""Comprueba que los nombres de ubicaciones protegidos sigan en inglés."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
GLOBAL_ES = RAIZ / "global.ini"
LIVE_INGLES = Path(
    r"C:\Program Files\Roberts Space Industries\StarCitizen\LIVE\data\Localization\english\global.ini"
)

CLAVES_UBICACION = frozenset(
    """
Bacchus_AsteroidBelt1\nBacchus_Flotilla\nBacchus_JumpPoint_Garron\nBacchus_JumpPoint_Geddon\nBacchus_Star1\nBacchus_Star2\nCano_AsteroidBelt1\nCano_JumpPoint_Davien\nCano_JumpPoint_Pyro\nCastra_JumpPoint_Hadrian\nCastra_JumpPoint_Nyx\nCastra_JumpPoint_Oso\nCastra_JumpPoint_Oya\nCastra_JumpPoint_Pyro\nCollector_Station_01_Name\nCollector_Station_02_Name\nCollector_Station_03_Name\nEllis_AsteroidBelt1\nEllis_JumpPoint_Kilian\nEllis_JumpPoint_Magnus\nEllis_JumpPoint_Min\nEllis_JumpPoint_Nexus\nEllis_JumpPoint_Taranis\nGoss_JumpPoint_Helios\nGoss_JumpPoint_Osiris\nGoss_JumpPoint_Tayac\nGoss_JumpPoint_Terra\nGoss_JumpPoint_Tyrol\nHadrian_AsteroidBelt1\nHadrian_Flotilla\nHadrian_JumpPoint_Castra\nHadrian_JumpPoint_Gurzil\nHadrian_JumpPoint_Kiel\nHadrian_JumpPoint_Oya\nHadrian_JumpPoint_Pyro\nHadrian_JumpPoint_Terra\nHadrian_Star\nHurston_JumpPoint_MicroTech,P\nMagnus_JumpPoint_Ellis\nMagnus_JumpPoint_Stanton\nMagnus_JumpPoint_Terra\nNyx_AsteroidBelt1\nNyx_AsteroidBelt2\nNyx_JumpPoint_Bremen\nNyx_JumpPoint_Castra\nNyx_JumpPoint_Odin\nNyx_JumpPoint_Pyro\nNyx_JumpPoint_Tohil\nNyx_JumpPoint_Virgil\nNyx_MoraineBase_Address,P\nNyx_MoraineBase_Name,P\nNyx_OutlawStation_Glaciem\nNyx_OutlawStation_Keeger\nNyx_Pyro_JPStation_clinic\nNyx_SocialStation_001\nNyx_SocialStation_003\nNyx_SocialStation_004\nNyx_SocialStation_005\nNyx_Stanton_JPStation_clinic\nOso_JumpPoint_Castra\nOso_JumpPoint_Kallis\nOso_JumpPoint_Pyro\nOso_Star\nPyro1_ASD_Monorail_Compound_1A\nPyro1_ASD_Monorail_Compound_1B\nPyro1_ASD_Monorail_Compound_1C\nPyro1_ASD_Monorail_Compound_2A\nPyro1_ASD_Monorail_Compound_2B\nPyro1_ASD_Monorail_Compound_2C\nPyro1_ASD_Research_Facility_1A\nPyro1_ASD_Research_Facility_1B\nPyro1_ASD_Research_Facility_1C\nPyro1_ASD_Research_Facility_2A\nPyro1_ASD_Research_Facility_2B\nPyro1_ASD_Research_Facility_2C\nPyro1_L1_01_Entrance\nPyro1_L1_02_Entrance\nPyro1_L1_03_Entrance\nPyro1_L1_04_Entrance\nPyro1_L2_01_Entrance\nPyro1_L2_02_Entrance\nPyro1_L2_03_Entrance\nPyro1_L2_04_Entrance\nPyro1_L3_01_Entrance\nPyro1_L3_02_Entrance\nPyro1_L3_03_Entrance\nPyro1_L3_04_Entrance\nPyro1_L4_01_Entrance\nPyro1_L4_02_Entrance\nPyro1_L4_03_Entrance\nPyro1_L4_04_Entrance\nPyro1_L5_01_Entrance\nPyro1_L5_02_Entrance\nPyro1_L5_03_Entrance\nPyro1_L5_04_Entrance\nPyro1_Outpost_col_xs_dpt_otlw_001\nPyro2_L1_01_Entrance\nPyro2_L1_02_Entrance\nPyro2_L1_03_Entrance\nPyro2_L1_04_Entrance\nPyro2_L2_01_Entrance\nPyro2_L2_02_Entrance\nPyro2_L2_03_Entrance\nPyro2_L2_04_Entrance\nPyro2_L3_01_Entrance\nPyro2_L3_02_Entrance\nPyro2_L3_03_Entrance\nPyro2_L3_04_Entrance\nPyro2_L4_01_Entrance\nPyro2_L4_02_Entrance\nPyro2_L4_03_Entrance\nPyro2_L4_04_Entrance\nPyro2_L5_01_Entrance\nPyro2_L5_02_Entrance\nPyro2_L5_03_Entrance\nPyro2_L5_04_Entrance\nPyro2_MiningCompound_drlct_001_a\nPyro2_MiningCompound_drlct_001_b\nPyro2_MiningCompound_drlct_001_c\nPyro2_MiningCompound_drlct_001_d\nPyro2_MiningCompound_drlct_002_a\nPyro2_MiningCompound_drlct_002_b\nPyro2_MiningCompound_drlct_002_c\nPyro2_MiningCompound_drlct_002_d\nPyro2_Outpost_col_m_mng_otlw_002\nPyro2_Outpost_col_s_mng_otlw_001\nPyro2_Outpost_col_s_trdpst_otlw_001\nPyro2_Outpost_col_xs_dpt_otlw_001\nPyro2_Racetrack_FoolsRun\nPyro2_Racetrack_FoolsRun_add\nPyro3_L1_01_Entrance\nPyro3_L1_02_Entrance\nPyro3_L1_03_Entrance\nPyro3_L1_04_Entrance\nPyro3_L2_01_Entrance\nPyro3_L2_02_Entrance\nPyro3_L2_03_Entrance\nPyro3_L2_04_Entrance\nPyro3_L3_01_Entrance\nPyro3_L3_02_Entrance\nPyro3_L3_03_Entrance\nPyro3_L3_04_Entrance\nPyro3_L4_01_Entrance\nPyro3_L4_02_Entrance\nPyro3_L4_03_Entrance\nPyro3_L4_04_Entrance\nPyro3_L5_01_Entrance\nPyro3_L5_02_Entrance\nPyro3_L5_03_Entrance\nPyro3_L5_04_Entrance\nPyro3_Outpost_col_m_trdpst_otlw_006\nPyro4_Outpost_col_m_scrp_indy_001\nPyro4_Outpost_col_m_trdpst_indy_001\nPyro4_Outpost_col_s_trdpst_otlw_001\nPyro5_L1_01_Entrance\nPyro5_L1_02_Entrance\nPyro5_L1_03_Entrance\nPyro5_L1_04_Entrance\nPyro5_L2_01_Entrance\nPyro5_L2_02_Entrance\nPyro5_L2_03_Entrance\nPyro5_L2_04_Entrance\nPyro5_L3_01_Entrance\nPyro5_L3_02_Entrance\nPyro5_L3_03_Entrance\nPyro5_L3_04_Entrance\nPyro5_L4_01_Entrance\nPyro5_L4_02_Entrance\nPyro5_L4_03_Entrance\nPyro5_L4_04_Entrance\nPyro5_L5_01_Entrance\nPyro5_L5_02_Entrance\nPyro5_L5_03_Entrance\nPyro5_L5_04_Entrance\nPyro6_L1_01_Entrance\nPyro6_L1_02_Entrance\nPyro6_L1_03_Entrance\nPyro6_L1_04_Entrance\nPyro6_L2_01_Entrance\nPyro6_L2_02_Entrance\nPyro6_L2_03_Entrance\nPyro6_L2_04_Entrance\nPyro6_L3_01_Entrance\nPyro6_L3_02_Entrance\nPyro6_L3_03_Entrance\nPyro6_L3_04_Entrance\nPyro6_L4_01_Entrance\nPyro6_L4_02_Entrance\nPyro6_L4_03_Entrance\nPyro6_L4_04_Entrance\nPyro6_L5_01_Entrance\nPyro6_L5_02_Entrance\nPyro6_L5_03_Entrance\nPyro6_L5_04_Entrance\nPyro6_Outpost_col_m_frm_otlw_001\nPyro6_Outpost_col_m_scrp_otlw_001\nPyro6_Outpost_col_m_trdpst_indy_001\nPyro6_Outpost_col_s_scrp_indy_001\nPyro6_Outpost_col_xs_dpt_otlw_001\nPyro_JumpPoint_Cano\nPyro_JumpPoint_Castra\nPyro_JumpPoint_Hadrian\nPyro_JumpPoint_Nyx\nPyro_JumpPoint_Oso\nPyro_JumpPoint_Stanton\nPyro_JumpPoint_Terra\nPyro_asteroidbeltA\nStanton1_CRAS_UGF_001,P\nStanton1_Cave_Aband_01\nStanton1_CommArray_001\nStanton1_CommArray_002\nStanton1_CommArray_003\nStanton1_CommArray_004\nStanton1_CommArray_005\nStanton1_DerelictSettlement_PickersField\nStanton1_DerelictSettlement_WeepingCove\nStanton1_DistributionCenter_Greycat_01\nStanton1_DistributionCenter_Greycat_02\nStanton1_GRIN_UGF_001,P\nStanton1_GRIN_UGF_002,P\nStanton1_HurDynMining_001\nStanton1_HurDynMining_002\nStanton1_HurDynMining_003\nStanton1_HurDynMining_004\nStanton1_HurDynMining_005\nStanton1_HurDynMining_006\nStanton1_HurDynUGF_001\nStanton1_HurDynUGF_002\nStanton1_HurDynUGF_003\nStanton1_HurDynUGF_004\nStanton1_HurDynUGF_005\nStanton1_HurDynUGF_006\nStanton1_HurDynUGF_007\nStanton1_HurDynUGF_008\nStanton1_HurDynUGF_009\nStanton1_HurDynUGF_010\nStanton1_HurDynUGF_011\nStanton1_HurDynUGF_012\nStanton1_HurDynUGF_013\nStanton1_HurDynUGF_014\nStanton1_HurDynUGF_015\nStanton1_HurDynUGF_016\nStanton1_Hurston_Lorville_Hospital\nStanton1_Hurston_Lorville_L19Residences\nStanton1_Racetrack_LorvilleOutskirts_add\nStanton1_SalvageYard_001\nStanton1_SecUGF_001\nStanton1_UGF_secdep_name\nStanton2_AdminCenter\nStanton2_CloudrestRetreatCluster\nStanton2_CloudrestRetreatCluster_Add\nStanton2_CommArray_001\nStanton2_CommArray_002\nStanton2_CommArray_003\nStanton2_CommArray_004\nStanton2_EmpyreanParkCluster_Add\nStanton2_ProspectPointCluster_Add\nStanton2_Racetrack_CaplanCircuit\nStanton2_Racetrack_CaplanCircuit_add\nStanton2_Transfer_Seraphim\nStanton2_Transfer_Seraphim_clinic\nStanton3_Area18_Central\nStanton3_Area18_Hospital\nStanton3_CommArray_001\nStanton3_CommArray_002\nStanton3_CommArray_003\nStanton3_OrbitalRelay\nStanton3_Racetrack_SkyScraper\nStanton3_Racetrack_SkyScraper_add\nStanton3_Transfer_clinic\nStanton4_CRAS_UGF_001,P\nStanton4_CommArray_001\nStanton4_CommArray_002\nStanton4_CommArray_003\nStanton4_CommArray_004\nStanton4_DerelictSettlement_RazorsEdge\nStanton4_DistributionCenter_CryAstro_01\nStanton4_DistributionCenter_CryAstro_02\nStanton4_DistributionCenter_Greycat_01\nStanton4_EMShelter_001\nStanton4_EMShelter_002\nStanton4_EMShelter_003\nStanton4_EMShelter_004\nStanton4_NewBab_DomeSurfaceExit\nStanton4_NewBab_DomeSurfaceExit_GroundATC\nStanton4_NewBab_MetroLoop\nStanton4_NewBab_NBIS\nStanton4_NewBab_NBIS_ATC\nStanton4_NewBab_NBIS_GroundATC\nStanton4_NewBab_PlanetaryServices\nStanton4_NewBab_PlanetarySurfaceExit\nStanton4_NewBab_TheCommons\nStanton4_Rayari_001\nStanton4_Rayari_002\nStanton4_ReclaimerSettlement\nStanton4_Shubin_001\nStanton4_Shubin_002\nStanton4_Shubin_003\nStanton4_Shubin_004\nStanton4_Stash_001\nStanton4_Stash_002\nStanton4_Transfer_clinic\nStanton4_UGF_001\nStanton4_UGF_002\nStanton4_UGF_003\nStanton4_UGF_004\nStanton4_UGF_005\nStanton4_UGF_006\nStanton4_UGF_007\nStanton4_UGF_008\nStanton4_UGF_009\nStanton4_UGF_010\nStanton4_UGF_011\nStanton_JumpPoint_Magnus\nStanton_JumpPoint_Nyx\nStanton_JumpPoint_Pyro\nStanton_JumpPoint_Terra\nTaranis_AsteroidBelt1\nTaranis_AsteroidBelt2\nTaranis_JumpPoint_Ellis\nTaranis_JumpPoint_Genesis\nTaranis_JumpPoint_Helios\nTaranis_JumpPoint_Terra\nTayac_AsteroidBelt1\nTayac_JumpPoint_Baker\nTayac_JumpPoint_Goss\nTayac_JumpPoint_Terra\nTerra_AsteroidBelt1\nTerra_AsteroidBelt2\nTerra_JumpPoint_Goss\nTerra_JumpPoint_Hadrian\nTerra_JumpPoint_Magnus\nTerra_JumpPoint_Pyro\nTerra_JumpPoint_Stanton\nTerra_JumpPoint_Taranis\nTerra_JumpPoint_Tayac\nVirgil_AsteroidBelt1\nVirgil_JumpPoint_Kellog\nVirgil_JumpPoint_Nyx\nVirgil_JumpPoint_Oberon\nVirgil_JumpPoint_Tiber\nVirgil_JumpPoint_Vega\nVirgil_Star\npyro_asteroid_cluster_001\npyro_asteroid_cluster_003\npyro_asteroid_cluster_004\npyro_asteroid_cluster_005\npyro_asteroid_cluster_006\npyro_asteroid_cluster_007\npyro_asteroid_cluster_009\npyro_asteroid_cluster_010\npyro_asteroid_cluster_012\npyro_asteroid_cluster_013\npyro_asteroid_cluster_014\npyro_asteroid_cluster_015\npyro_asteroid_cluster_016\npyro_asteroid_cluster_018\npyro_asteroid_cluster_019\npyro_asteroid_cluster_022\npyro_asteroid_cluster_023\nstanton1_surface_relay\nstanton2_Shipping_Covalex\nstanton2_Shipping_Covalex_CargoBay\nstanton2_researchSatellite275\nstanton2_researchSatellite306\nstanton2_researchSatellite472\nstanton2_researchSatellite556\nstanton2_researchSatellite625\nstanton2_researchSatellite730\nstanton2_researchSatellite849\nstanton2_researchSatellite_126\nstanton2_restockStation042\nstanton2_restockStation126\nstanton2_restockStation275\nstanton2_restockStation306\nstanton2_restockStation472\nstanton2_restockStation556\nstanton2_restockStation625\nstanton2_restockStation730\nstanton2_restockStation849\nstanton2_restockStation_Generic\nstanton2_security_kareah\nstanton3_private_landingpad\nui_interactor_ST2_CrusaderShowroom\nui_interactor_ST2_GreenCircle\nui_interactor_ST2_commercial_platform\nui_interactor_ST2_industrial_platform\nui_interactor_ST2_spaceport\nui_interactor_ST2_transit_commercial\nui_interactor_ST2_transit_convention_centre\nui_interactor_ST2_transit_generic\nui_interactor_ST2_transit_industrial\nui_interactor_ST2_transit_spaceport\nui_interactor_ST2_voyager_bar\nui_interactor_ST3_ADF_Lobby\nui_interactor_ST3_ION_Centermass\nui_interactor_ST3_ION_Lobby\nui_interactor_ST3_Transit_Bevic\nui_interactor_ST3_Transit_central\nui_interactor_ST3_Transit_spaceport\nui_interactor_ST4_Tobin_ApexHall\nui_interactor_ST4_Tobin_ZenithHall\nui_interactor_ST4_Transit_Tobin\nui_interactor_ST4_Transit_spaceport
""".split()
)


def cargar(ruta: Path) -> tuple[dict[str, str], list[str]]:
    valores: dict[str, str] = {}
    duplicadas: list[str] = []
    for numero, linea in enumerate(ruta.read_text(encoding="utf-8-sig").splitlines(), 1):
        if "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        if clave in valores:
            duplicadas.append(f"{clave} (línea {numero})")
        valores[clave] = valor
    return valores, duplicadas


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compara con el catálogo inglés los nombres de ubicación protegidos."
    )
    parser.add_argument(
        "english_global",
        nargs="?",
        type=Path,
        default=LIVE_INGLES,
        help="global.ini inglés; por defecto usa la instalación LIVE",
    )
    args = parser.parse_args()

    if not args.english_global.is_file():
        print(f"ERROR: no existe el catálogo inglés: {args.english_global}")
        return 2

    espanol, duplicadas_es = cargar(GLOBAL_ES)
    ingles, duplicadas_en = cargar(args.english_global)
    errores: list[str] = []

    for clave in sorted(CLAVES_UBICACION):
        clave_ingles = clave if clave in ingles else clave.removesuffix(",P")
        if clave_ingles not in ingles:
            errores.append(f"{clave}: falta en el catálogo inglés")
        elif clave not in espanol:
            errores.append(f"{clave}: falta en global.ini")
        elif espanol[clave] != ingles[clave_ingles]:
            errores.append(
                f"{clave}: debe conservar {ingles[clave_ingles]!r}; "
                f"contiene {espanol[clave]!r}"
            )

    for duplicada in duplicadas_es:
        if duplicada.split(" ", 1)[0] in CLAVES_UBICACION:
            errores.append(f"Clave española duplicada: {duplicada}")
    for duplicada in duplicadas_en:
        if duplicada.split(" ", 1)[0] in CLAVES_UBICACION:
            errores.append(f"Clave inglesa duplicada: {duplicada}")

    if errores:
        print(f"ERROR: {len(errores)} problemas en nombres de ubicaciones:")
        for error in errores:
            print(f"- {error}")
        return 1

    print(
        f"OK: {len(CLAVES_UBICACION)} nombres de ubicaciones conservan exactamente "
        "el texto original inglés."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

