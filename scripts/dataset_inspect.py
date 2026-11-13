import csv
import sys
from pathlib import Path
from datetime import datetime

path = Path(sys.argv[1])

if not path.exists():
    raise FileNotFoundError(path)

print(f"Arquivo: {path}")
print(f"Tamanho: {path.stat().st_size / (1024**2):.2f} MB")

total = 0
missing = 0
malformed = 0
dates = []

with path.open(
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.reader(file, delimiter=";")
    header = next(reader)

    print(f"\nColunas ({len(header)}):")
    print(header)

    for row in reader:
        if not row:
            continue

        if len(row) != len(header):
            malformed += 1
            continue

        total += 1
        missing += row.count("?")

        try:
            dates.append(
                datetime.strptime(
                    row[0], "%d/%m/%Y"
                ).date()
            )
        except ValueError:
            malformed += 1

print(f"\nRegistros: {total:,}")
print(f"Valores ausentes: {missing:,}")
print(f"Linhas inválidas: {malformed}")

if dates:
    print(f"Data inicial: {min(dates)}")
    print(f"Data final: {max(dates)}")