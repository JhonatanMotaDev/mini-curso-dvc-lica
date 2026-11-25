"""Gera o CSV sintético do exemplo: v1 (base) e v2 (5 linhas alteradas)."""
import csv
import random
import sys
from pathlib import Path

OUTPUT = Path("data/medicoes.csv")
ROWS = 100
CHANGED_IDS = (10, 20, 30, 40, 50)  # linhas alteradas na V2
NEW_VALUE = 999.99


def build_rows() -> list[list]:
    rng = random.Random(42)  # semente fixa -> saída determinística
    return [[i, f"sensor_{i % 5 + 1}", round(rng.uniform(10, 100), 2)] for i in range(1, ROWS + 1)]


def main(version: str) -> None:
    if version not in ("v1", "v2"):
        raise SystemExit("Uso: python scripts/generate_csv.py v1|v2")
    rows = build_rows()
    if version == "v2":
        for row in rows:
            if row[0] in CHANGED_IDS:
                row[2] = NEW_VALUE
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["id", "sensor", "valor"])
        writer.writerows(rows)
    print(f"{version.upper()}: {len(rows)} linhas -> {OUTPUT}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) == 2 else "")
