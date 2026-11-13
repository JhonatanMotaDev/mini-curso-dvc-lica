
import sys
from datetime import date, datetime
from pathlib import Path

SOURCE = Path("data/source/household_power_consumption.txt")
OUTPUT = Path("data/snapshots/household_power_consumption.txt")

VERSIONS = {
    "v1": (date(2006, 12, 16), date(2007, 12, 15)),
    "v2": (date(2006, 12, 16), date(2010, 11, 26)),
}


def create_snapshot(version):
    if version not in VERSIONS:
        raise ValueError("Use v1 ou v2.")

    start_date, end_date = VERSIONS[version]

    if not SOURCE.exists():
        raise FileNotFoundError(f"Dataset original não encontrado: {SOURCE}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    total = 0

    with SOURCE.open("r", encoding="utf-8-sig", newline="") as source:
        with OUTPUT.open("w", encoding="utf-8", newline="") as output:
            for line_number, line in enumerate(source):
                if line_number == 0:
                    output.write(line)
                    continue

                date_text = line.split(";", 1)[0]
                current_date = datetime.strptime(
                    date_text, "%d/%m/%Y"
                ).date()

                if start_date <= current_date <= end_date:
                    output.write(line)
                    total += 1

    print(f"Versão gerada: {version.upper()}")
    print(f"Período: {start_date} a {end_date}")
    print(f"Registros: {total:,}")
    print(f"Arquivo: {OUTPUT}")
    print(f"Tamanho: {OUTPUT.stat().st_size / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python scripts/create_snapshot.py v1|v2")

    create_snapshot(sys.argv[1].lower())
