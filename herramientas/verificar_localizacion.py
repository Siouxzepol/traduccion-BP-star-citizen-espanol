"""Comprueba la integridad del catálogo español frente al inglés de LIVE.

Uso:
    python herramientas/verificar_localizacion.py RUTA_AL_GLOBAL_INGLES
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SPANISH_PATH = ROOT / "global.ini"
MISSION_MACRO_RE = re.compile(r"~mission\([^)]*\)")
PRINTF_RE = re.compile(
    r"%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?(?:ll|l|h)?[diuoxXfFeEgGaAcspS]"
)
FORMAT_TAGS = ("EM1", "EM2", "EM3", "EM4")


def load_entries(
    path: Path,
    *,
    reject_replacement_characters: bool = True,
    validate_format_tags: bool = False,
) -> tuple[dict[str, tuple[int, str]], list[str]]:
    entries: dict[str, tuple[int, str]] = {}
    errors: list[str] = []
    raw_keys: set[str] = set()

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        if "=" not in line:
            errors.append(f"{path.name}:{line_number}: línea sin '='")
            continue

        raw_key, value = line.split("=", 1)
        key = raw_key.removesuffix(",P")
        if raw_key in raw_keys:
            errors.append(f"{path.name}:{line_number}: clave duplicada {raw_key}")
        if key in entries:
            errors.append(f"{path.name}:{line_number}: clave normalizada duplicada {key}")
        raw_keys.add(raw_key)
        entries[key] = (line_number, value)

        if reject_replacement_characters and "\ufffd" in value:
            errors.append(
                f"{path.name}:{line_number}: carácter de sustitución Unicode en {raw_key}"
            )

        if validate_format_tags and not key.startswith("text_ui_tags_"):
            for tag in FORMAT_TAGS:
                opened = value.count(f"<{tag}>")
                closed = value.count(f"</{tag}>")
                if opened != closed:
                    errors.append(
                        f"{path.name}:{line_number}: {raw_key} tiene etiquetas {tag} "
                        f"desequilibradas ({opened} aperturas, {closed} cierres)"
                    )

    return entries, errors


def compare_with_english(
    spanish: dict[str, tuple[int, str]], english: dict[str, tuple[int, str]]
) -> list[str]:
    errors: list[str] = []

    for key in sorted(english.keys() - spanish.keys()):
        errors.append(f"falta la clave inglesa {key}")

    for key in sorted(english.keys() & spanish.keys()):
        spanish_line, spanish_value = spanish[key]
        _, english_value = english[key]

        if english_value and not spanish_value:
            errors.append(
                f"global.ini:{spanish_line}: {key} está vacía, pero el inglés contiene texto"
            )

        english_macros = Counter(MISSION_MACRO_RE.findall(english_value))
        spanish_macros = Counter(MISSION_MACRO_RE.findall(spanish_value))
        missing_macros = english_macros - spanish_macros
        if missing_macros:
            errors.append(
                f"global.ini:{spanish_line}: {key} omite macros {dict(missing_macros)}"
            )

        english_printf = Counter(PRINTF_RE.findall(english_value))
        spanish_printf = Counter(PRINTF_RE.findall(spanish_value))
        if english_printf != spanish_printf:
            errors.append(
                f"global.ini:{spanish_line}: {key} altera parámetros printf: "
                f"inglés={dict(english_printf)}, español={dict(spanish_printf)}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("english_global", type=Path)
    args = parser.parse_args()

    spanish, errors = load_entries(SPANISH_PATH, validate_format_tags=True)
    english, english_errors = load_entries(
        args.english_global, reject_replacement_characters=False
    )
    errors.extend(f"catálogo inglés: {error}" for error in english_errors)
    errors.extend(compare_with_english(spanish, english))

    if errors:
        print(f"ERROR: {len(errors)} problemas de integridad:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print(
        f"OK: {len(spanish)} entradas españolas cubren las {len(english)} claves de LIVE "
        "sin pérdida de macros, parámetros dinámicos ni etiquetas de formato."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
