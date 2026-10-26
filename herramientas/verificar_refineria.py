#!/usr/bin/env python3
"""Comprueba que los nueve métodos de refinería no vuelvan a cruzarse."""

from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
GLOBAL_INI = RAIZ / "global.ini"

ESPERADO = {
    "refinery_ui_ProcessingType_FastCareful": "Pyrometric Chromalysis",
    "refinery_ui_ProcessingType_FastCareful_Details,P": "Velocidad baja // Alto coste // Alto rendimiento",
    "refinery_ui_ProcessingType_FastNormal": "Gaskin Process",
    "refinery_ui_ProcessingType_FastNormal_Details,P": "Velocidad alta // Alto coste // Rendimiento moderado\\n",
    "refinery_ui_ProcessingType_FastWasteful": "XCR Reaction",
    "refinery_ui_ProcessingType_FastWasteful_Details,P": "Velocidad alta // Alto coste // Bajo rendimiento",
    "refinery_ui_ProcessingType_NormalCareful": "Ferron Exchange",
    "refinery_ui_ProcessingType_NormalCareful_Details,P": "Velocidad baja // Coste moderado // Alto rendimiento",
    "refinery_ui_ProcessingType_NormalNormal": "Electrostarolysis",
    "refinery_ui_ProcessingType_NormalNormal_Details,P": "Velocidad moderada // Coste moderado // Rendimiento moderado\\n",
    "refinery_ui_ProcessingType_NormalWasteful": "Cormack Method",
    "refinery_ui_ProcessingType_NormalWasteful_Details,P": "Velocidad alta // Coste moderado // Bajo rendimiento",
    "refinery_ui_ProcessingType_SlowCareful": "Dinyx Solventation",
    "refinery_ui_ProcessingType_SlowCareful_Details,P": "Velocidad muy baja // Bajo coste // Alto rendimiento",
    "refinery_ui_ProcessingType_SlowNormal": "Thermonatic Deposition",
    "refinery_ui_ProcessingType_SlowNormal_Details,P": "Velocidad baja // Bajo coste // Rendimiento moderado",
    "refinery_ui_ProcessingType_SlowWasteful": "Kazen Winnowing",
    "refinery_ui_ProcessingType_SlowWasteful_Details,P": "Velocidad moderada // Bajo coste // Bajo rendimiento",
}


def cargar_ini(ruta: Path) -> tuple[dict[str, str], list[str]]:
    valores: dict[str, str] = {}
    duplicadas: list[str] = []
    for numero, linea in enumerate(ruta.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not linea or linea.startswith(";") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        if clave in valores:
            duplicadas.append(f"{clave} (línea {numero})")
        valores[clave] = valor
    return valores, duplicadas


def main() -> int:
    valores, duplicadas = cargar_ini(GLOBAL_INI)
    errores = []
    for clave, esperado in ESPERADO.items():
        actual = valores.get(clave)
        if actual != esperado:
            errores.append(f"{clave}: esperado {esperado!r}; encontrado {actual!r}")

    duplicadas_refineria = [d for d in duplicadas if d.startswith("refinery_ui_ProcessingType_")]
    errores.extend(f"Clave duplicada: {d}" for d in duplicadas_refineria)

    if errores:
        print("ERROR: la tabla de métodos de refinería no es coherente:")
        for error in errores:
            print(f"- {error}")
        return 1

    print("OK: 9 métodos y 9 rótulos de refinería verificados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
