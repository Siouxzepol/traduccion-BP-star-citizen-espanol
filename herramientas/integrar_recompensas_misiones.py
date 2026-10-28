#!/usr/bin/env python3
"""Add safe, static reputation/blueprint notes to localized mission strings.

The game localization file cannot inspect the active contract at runtime. This
tool annotates titles with reward markers when all contracts sharing the title
agree on the marker, and descriptions when a title key maps unambiguously to a
reward signature and a matching description key exists in global.ini.

Usage:
  python herramientas/integrar_recompensas_misiones.py [catalog.json] [global.ini] [english.ini] [componentes.json]
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


REWARD_BLOCK_RE = re.compile(r"\\n\\n(?:<EM4>)?RECOMPENSAS DEL CONTRATO(?:</EM4>)?")
TITLE_MARKER_RE = re.compile(r"^(?:<EM\d+>)?\[(?:BP\??|REP\s+[^\]]+)\](?:</EM\d+>)?\s*")
PLACEHOLDER_TOKENS = {"", "@LOC_PLACEHOLDER", "@LOC_UNINITIALIZED"}


def title_reward_tags(contracts: list[dict]) -> list[str]:
    """Return only title tags that are accurate for every shared-title variant."""
    tags = []
    if contracts and all(contract.get("planos") for contract in contracts):
        tags.append("[BP]")

    standing_amounts = []
    for contract in contracts:
        amounts = {
            reward.get("cantidad")
            for reward in contract.get("reputacion", [])
            if reward.get("ambito_loc_id") == "@mobiGlas_Reputation_Standing"
            and reward.get("cantidad") is not None
        }
        # A contract with multiple standing awards cannot be summarized by one number.
        standing_amounts.append(next(iter(amounts)) if len(amounts) == 1 else None)
    if standing_amounts and standing_amounts[0] is not None and len(set(standing_amounts)) == 1:
        tags.append(f"[REP {standing_amounts[0]}]")
    return tags


def reward_signature(contract: dict) -> tuple:
    reputation = tuple(sorted(
        (r.get("faccion_loc_id"), r.get("cantidad"), r.get("ambito_loc_id"))
        for r in contract.get("reputacion", [])
    ))
    blueprints = tuple(sorted(
        (p.get("pool"), p.get("probabilidad"))
        for p in contract.get("planos", [])
    ))
    return reputation, blueprints


def candidate_description_keys(title_key: str) -> list[str]:
    candidates = []
    for replacement in ("_Desc", "_desc"):
        candidate = re.sub(r"(?i)_title(?=_|$)", replacement, title_key)
        if candidate != title_key and candidate not in candidates:
            candidates.append(candidate)
    return candidates


def reward_text(
    contract: dict,
    strings: dict[str, str],
    english_strings: dict[str, str],
    component_names: dict[str, str],
) -> str:
    lines = ["<EM4>RECOMPENSAS DEL CONTRATO</EM4>"]
    reputation = contract.get("reputacion", [])
    if reputation:
        parts = []
        seen_reputation = set()
        for reward in reputation:
            faction = reward.get("faccion") or reward.get("faccion_ingles") or "facción"
            amount = reward.get("cantidad")
            scope_key = (reward.get("ambito_loc_id") or "").lstrip("@")
            scope = strings.get(scope_key) or reward.get("ambito_ingles") or "Reputación"
            identity = (faction, scope_key, amount)
            if amount is not None and identity not in seen_reputation:
                parts.append(f"+{amount} {scope} con {faction}")
                seen_reputation.add(identity)
        if parts:
            lines.append("<EM4>Reputación</EM4>: " + "; ".join(parts) + ".")

    pool_lines = []
    for pool_index, pool in enumerate(contract.get("planos", []), start=1):
        names = []
        seen_options = set()
        for option in pool.get("opciones", []):
            item_id = option.get("objeto_id")
            if not item_id:
                continue
            option_id = option.get("id") or item_id
            if option_id in seen_options:
                continue
            seen_options.add(option_id)
            name = blueprint_item_name(option, english_strings, component_names)
            if name and name not in names:
                names.append(name)
        if names:
            chance = pool.get("probabilidad")
            chance_text = f" ({chance * 100:g} % de probabilidad)" if isinstance(chance, (int, float)) and chance < 1 else ""
            group_title = f"Grupo {pool_index}{chance_text}:"
            pool_lines.append(group_title + r"\n" + r"\n".join(f"- {name}" for name in names))
    if pool_lines:
        lines.append("<EM4>Planos posibles</EM4> (selección aleatoria):" + r"\n" + r"\n".join(pool_lines))
    return r"\n\n".join(lines)


def blueprint_item_name(
    option: dict,
    english_strings: dict[str, str],
    component_names: dict[str, str],
) -> str:
    """Resolve a blueprint reward to an English-only, unambiguous item name."""
    item_id = (option.get("objeto_id") or "").strip()
    explicit = (option.get("nombre_ingles") or "").strip()
    if explicit and explicit not in PLACEHOLDER_TOKENS:
        return explicit
    if item_id:
        localized = (
            english_strings.get(f"item_Name{item_id}")
            or english_strings.get(f"item_Name_{item_id}")
        )
        if localized:
            return localized.strip()
        component = component_names.get(item_id.lower())
        if component:
            return component.strip()
        return readable_item_name_english(item_id)
    return ""


def readable_item_name_english(item_id: str) -> str:
    """Create a deterministic English fallback without translating a BP name."""
    manufacturers = {
        "amrs": "AMRS", "apar": "APAR", "asad": "ASAD", "banu": "Banu",
        "behr": "Behring", "grin": "Greycat", "gmni": "Gemini", "thcn": "Tachyon",
    }
    types = {
        "lasercannon": "Laser Cannon", "ballisticgatling": "Ballistic Gatling",
        "ballisticscattergun": "Ballistic Scattergun", "massdriver": "Mass Driver",
        "distortionrepeater": "Distortion Repeater", "tachyoncannon": "Tachyon Cannon",
        "ballisticcannon": "Ballistic Cannon", "ballisticrepeater": "Ballistic Repeater",
        "energycannon": "Energy Cannon", "mining_laser": "Mining Laser",
        "fuel_nozzle": "Fuel Nozzle", "utility": "Utility",
    }
    parts = item_id.lower().split("_")
    manufacturer = manufacturers.get(parts[0], parts[0].upper())
    compact = "_".join(parts[1:])
    description = next((label for key, label in types.items() if key in compact), None)
    if description:
        size = re.search(r"(?:^|_)s(\d+)(?:_|$)", compact)
        return f"{manufacturer} {description}" + (f" S{size.group(1)}" if size else "")
    component_types = {
        "cool": "Cooler", "powr": "Power Plant", "shld": "Shield Generator",
        "radr": "Radar", "qdrv": "Quantum Drive", "fuel": "Fuel Component",
        "mining": "Mining Equipment", "salvage": "Salvage Equipment", "cargo": "Cargo Container",
    }
    if parts[0] in component_types:
        brand = parts[1].upper() if len(parts) > 1 else ""
        model_parts = [part for part in parts[2:] if part != "scitem"]
        model = []
        size = None
        for part in model_parts:
            if re.fullmatch(r"s\d+", part):
                size = part.upper()
            else:
                model.append(part.upper() if len(part) <= 4 else part.capitalize())
        label = " ".join([component_types[parts[0]], brand, *model]).strip()
        return label + (f" {size}" if size else "")
    words = [part.upper() if len(part) <= 4 else part.capitalize() for part in parts[1:]]
    return manufacturer + (" " + " ".join(words) if words else "")


def load_strings(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    values = {}
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if line and not line.lstrip().startswith((";", "#")) and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def load_component_names(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return {
        component["id"].lower(): component["nombre_ingles"]
        for component in data.get("componentes", [])
        if component.get("id") and component.get("nombre_ingles")
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    catalog_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "datos" / "misiones_reputacion_planos.json"
    ini_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "global.ini"
    english_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    components_path = Path(sys.argv[4]) if len(sys.argv) > 4 else root / "datos" / "componentes_nave.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    contracts = catalog["contratos"]
    english_strings = load_strings(english_path)
    component_names = load_component_names(components_path)

    groups: dict[str, list[dict]] = defaultdict(list)
    for contract in contracts:
        title = contract.get("titulo_loc_id")
        if title and title != "@LOC_UNINITIALIZED":
            groups[title.lstrip("@").strip()].append(contract)

    original_bytes = ini_path.read_bytes()
    has_bom = original_bytes.startswith(b"\xef\xbb\xbf")
    original = original_bytes.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in original else "\n"
    lines = original.splitlines(keepends=True)
    values: dict[str, str] = {}
    key_pattern = re.compile(r"^([^=,]+)(,P)?=(.*)$")
    for line in lines:
        match = key_pattern.match(line.rstrip("\r\n"))
        if match:
            values[match.group(1).strip()] = match.group(3)

    updates: dict[str, str] = {}
    managed_description_keys: set[str] = set()
    title_updates: dict[str, list[str]] = {}
    skipped_ambiguous = 0
    for title_key, variants in groups.items():
        tags = title_reward_tags(variants)
        if title_key in values:
            title_updates[title_key] = tags

    for title_key, variants in groups.items():
        description_key = next(
            (key for key in candidate_description_keys(title_key) if key in values),
            None,
        )
        if not description_key:
            continue
        managed_description_keys.add(description_key)
        signatures = {reward_signature(c) for c in variants}
        if len(signatures) != 1:
            skipped_ambiguous += 1
            continue
        updates[description_key] = reward_text(
            variants[0], values, english_strings, component_names
        )

    written = 0
    titles_written = 0
    bp_titles = 0
    rep_titles = 0
    result = []
    for line in lines:
        ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        body = line[:-len(ending)] if ending else line
        match = key_pattern.match(body)
        if match and match.group(1).strip() in title_updates:
            title_key = match.group(1).strip()
            key, suffix, value = match.group(1), match.group(2) or "", match.group(3)
            while TITLE_MARKER_RE.match(value):
                value = TITLE_MARKER_RE.sub("", value, count=1)
            tags = title_updates[title_key]
            prefix = " ".join(f"<EM4>{tag}</EM4>" for tag in tags)
            localized_value = (prefix + " " + value.rstrip()).lstrip()
            result.append(key + suffix + "=" + localized_value + ending)
            titles_written += int(bool(tags))
            bp_titles += int("[BP]" in tags)
            rep_titles += int(any(tag.startswith("[REP ") for tag in tags))
        elif match and match.group(1).strip() in managed_description_keys:
            key, suffix, value = match.group(1), match.group(2) or "", match.group(3)
            value = REWARD_BLOCK_RE.split(value, 1)[0].rstrip()
            description_key = match.group(1).strip()
            if description_key in updates:
                value += r"\n\n" + updates[description_key]
                written += 1
            result.append(key + suffix + "=" + value + ending)
        else:
            result.append(line)

    output_bytes = "".join(result).encode("utf-8")
    # global.ini in this repository is distributed as UTF-8 with a BOM.
    ini_path.write_bytes((b"\xef\xbb\xbf" if has_bom or ini_path.name.lower() == "global.ini" else b"") + output_bytes)
    print(f"Títulos etiquetados: {titles_written} ({bp_titles} con [BP], {rep_titles} con [REP n])")
    print(f"Descripciones actualizadas: {written}")
    print(f"Claves de misión ambiguas omitidas: {skipped_ambiguous}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
