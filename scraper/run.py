# -*- coding: utf-8 -*-
"""
Entry point for the scraper.

Usage:
    python -m scraper.run --target pokemon   # scrape evolutions + learnsets
    python -m scraper.run --target moves     # scrape move data
    python -m scraper.run --target namemap   # build dex num -> Chinese name map only
"""

import argparse
import json
import os

from .name_map import build_name_map
from .parse_pokemon import parse_evolution, parse_learnset
from .parse_move import parse_move

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../resources")


def _write(filename: str, data) -> None:
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {path}")


def run_namemap():
    print("Building name map...")
    name_map = build_name_map()
    print(f"Found {len(name_map)} entries")
    _write("name_map.json", name_map)
    return name_map


def run_pokemon(name_map: dict[int, str]):
    evolutions = {}
    learnsets = {}

    for num in sorted(name_map.keys()):
        cn_name = name_map[num]
        print(f"[{num:03d}] {cn_name}")

        try:
            evolutions[num] = parse_evolution(cn_name)
        except Exception as e:
            print(f"  evolution error: {e}")
            evolutions[num] = []

        try:
            learnsets[num] = parse_learnset(cn_name, gen=3)
        except Exception as e:
            print(f"  learnset error: {e}")
            learnsets[num] = {}

    _write("evolutions.json", evolutions)
    _write("learnsets.json", learnsets)


def run_moves(name_map: dict[int, str]):
    # Collect unique move names from all learnsets
    learnsets_path = os.path.join(OUTPUT_DIR, "learnsets.json")
    if not os.path.exists(learnsets_path):
        print("learnsets.json not found — run --target pokemon first")
        return

    with open(learnsets_path, encoding="utf-8") as f:
        learnsets = json.load(f)

    move_names: set[str] = set()
    for pkm_learnset in learnsets.values():
        for entry in pkm_learnset.get("level_up", []):
            move_names.add(entry["move"])
        for entry in pkm_learnset.get("tm_hm", []):
            move_names.add(entry["move"])
        for entry in pkm_learnset.get("egg", []):
            move_names.add(entry["move"])
        for entry in pkm_learnset.get("tutor", []):
            move_names.add(entry["move"])

    moves = {}
    for name in sorted(move_names):
        print(f"Move: {name}")
        try:
            moves[name] = parse_move(name)
        except Exception as e:
            print(f"  error: {e}")
            moves[name] = {"name_cn": name}

    _write("moves.json", moves)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        choices=["namemap", "pokemon", "moves", "all"],
        default="all"
    )
    args = parser.parse_args()

    if args.target in ("namemap", "pokemon", "all"):
        name_map_path = os.path.join(OUTPUT_DIR, "name_map.json")
        if os.path.exists(name_map_path):
            with open(name_map_path, encoding="utf-8") as f:
                name_map = {int(k): v for k, v in json.load(f).items()}
            print(f"Loaded name map ({len(name_map)} entries)")
        else:
            name_map = run_namemap()

    if args.target in ("namemap",):
        return

    if args.target in ("pokemon", "all"):
        run_pokemon(name_map)

    if args.target in ("moves", "all"):
        run_moves(name_map)


if __name__ == "__main__":
    main()
