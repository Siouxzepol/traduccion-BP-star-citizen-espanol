#!/usr/bin/env python3
"""Verify mission reputation and blueprint annotations against the game catalog.

Usage:
  python herramientas/verificar_recompensas_misiones.py [catalog.json] [global.ini] [english.ini] [componentes.json]
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import integrar_recompensas_misiones as rewards


MARKER_RE = re.compile(r"^<EM\d+>(\[(?:BP|REP\s+[^\]]+)\])</EM\d+>\s*")
SPANISH_BP_WORDS_RE = re.compile(
    r"\b(?:brazales|coraza|perneras|casco|equipo de|láser|minero|minera|"
    r"cargador|bater[ií]a|herramienta|arboleda|magnetita|mediana|pesada|ligera|"
    r"dep[oó]sito|boquilla|salvamento)\b",
    re.IGNORECASE,
)


def markers(value: str) -> list[str]:
    found = []
    while match := MARKER_RE.match(value):
        found.append(match.group(1))
        value = value[match.end():]
    return found


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    catalog_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "datos" / "misiones_reputacion_planos.json"
    ini_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "global.ini"
    english_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    components_path = Path(sys.argv[4]) if len(sys.argv) > 4 else root / "datos" / "componentes_nave.json"

    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    contracts = catalog.get("contratos", [])
    strings = rewards.load_strings(ini_path)
    english = rewards.load_strings(english_path)
    components = rewards.load_component_names(components_path)
    errors: list[str] = []
    warnings: list[str] = []

    groups: dict[str, list[dict]] = defaultdict(list)
    blueprint_to_item: dict[str, set[str]] = defaultdict(set)
    item_to_names: dict[str, set[str]] = defaultdict(set)
    option_count = 0
    fallback_items: set[str] = set()
    visible_name_collisions = 0

    for contract in contracts:
        title = (contract.get("titulo_loc_id") or "").lstrip("@").strip()
        if title and title != "LOC_UNINITIALIZED":
            groups[title].append(contract)

        reputation = contract.get("reputacion", [])
        rep_identities = [
            (entry.get("faccion_loc_id"), entry.get("ambito_loc_id"), entry.get("cantidad"))
            for entry in reputation
        ]
        if len(rep_identities) != len(set(rep_identities)):
            errors.append(f"Reputación duplicada en {contract.get('contrato_id')}")
        for entry in reputation:
            if not entry.get("faccion_loc_id") or not entry.get("ambito_loc_id") or entry.get("cantidad") is None:
                errors.append(f"Reputación incompleta en {contract.get('contrato_id')}: {entry!r}")

        for pool in contract.get("planos", []):
            identities = []
            visible_names = []
            for option in pool.get("opciones", []):
                option_count += 1
                blueprint_id = option.get("id")
                item_id = option.get("objeto_id")
                if not blueprint_id or not item_id:
                    errors.append(f"BP incompleto en {contract.get('contrato_id')}: {option!r}")
                    continue
                identity = blueprint_id or item_id
                identities.append(identity)
                blueprint_to_item[blueprint_id].add(item_id)
                name = rewards.blueprint_item_name(option, english, components)
                visible_names.append(name)
                item_to_names[item_id].add(name)
                has_official_name = bool(
                    option.get("nombre_ingles")
                    or english.get(f"item_Name{item_id}")
                    or english.get(f"item_Name_{item_id}")
                    or components.get(item_id.lower())
                )
                if not has_official_name:
                    fallback_items.add(item_id)
                if not name:
                    errors.append(f"BP sin nombre en inglés: {blueprint_id}")
                elif SPANISH_BP_WORDS_RE.search(name):
                    errors.append(f"Nombre de BP no conservado en inglés: {blueprint_id} -> {name}")
            duplicate_ids = [value for value, count in Counter(identities).items() if count > 1]
            if duplicate_ids:
                errors.append(
                    f"BP repetido en {contract.get('contrato_id')} / {pool.get('pool')}: {duplicate_ids}"
                )
            duplicate_names = [value for value, count in Counter(visible_names).items() if value and count > 1]
            if duplicate_names:
                # Distinct game records can intentionally share the same official
                # visible name. The integrator collapses those repeated lines.
                visible_name_collisions += len(duplicate_names)

    for blueprint_id, item_ids in blueprint_to_item.items():
        if len(item_ids) != 1:
            errors.append(f"El BP {blueprint_id} apunta a varios objetos: {sorted(item_ids)}")
    for item_id, names in item_to_names.items():
        if len(names) != 1:
            errors.append(f"El objeto {item_id} tiene varios nombres ingleses: {sorted(names)}")

    checked_descriptions = 0
    ambiguous_descriptions = 0
    for title_key, variants in groups.items():
        expected_tags = rewards.title_reward_tags(variants)
        if title_key in strings:
            actual_tags = markers(strings[title_key])
            if actual_tags != expected_tags:
                errors.append(
                    f"Etiquetas incorrectas en {title_key}: {actual_tags!r}; esperado {expected_tags!r}"
                )

        description_key = next(
            (key for key in rewards.candidate_description_keys(title_key) if key in strings),
            None,
        )
        if not description_key:
            continue
        value = strings[description_key]
        signatures = {rewards.reward_signature(contract) for contract in variants}
        if len(signatures) != 1:
            ambiguous_descriptions += 1
            if rewards.REWARD_BLOCK_RE.search(value):
                errors.append(f"Recompensa obsoleta en descripción ambigua: {description_key}")
            continue
        expected = rewards.reward_text(variants[0], strings, english, components)
        expected_suffix = r"\n\n" + expected
        checked_descriptions += 1
        if not value.endswith(expected_suffix):
            errors.append(f"Bloque de recompensas incorrecto o ausente: {description_key}")

    if fallback_items:
        warnings.append(
            f"{len(fallback_items)} BP únicos usan un nombre inglés determinista derivado del ID "
            "porque el parche no publica un nombre oficial."
        )
    if visible_name_collisions:
        warnings.append(
            f"Se colapsaron {visible_name_collisions} repeticiones de nombres oficiales dentro de sus grupos."
        )

    print(f"Contratos revisados: {len(contracts)}")
    print(f"Grupos de títulos revisados: {len(groups)}")
    print(f"Opciones de BP revisadas: {option_count} ({len(blueprint_to_item)} BP únicos)")
    print(f"Descripciones exactas revisadas: {checked_descriptions}")
    print(f"Descripciones ambiguas sin anotación: {ambiguous_descriptions}")
    for warning in warnings:
        print(f"AVISO: {warning}")
    if errors:
        print(f"ERRORES: {len(errors)}", file=sys.stderr)
        for error in errors[:100]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 100:
            print(f"- ... y {len(errors) - 100} errores más", file=sys.stderr)
        return 1
    print("OK: nombres de BP, duplicados, etiquetas y reputaciones coherentes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
