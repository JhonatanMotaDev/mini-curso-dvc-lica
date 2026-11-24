import sys
from datetime import date, datetime
from pathlib import Path


class PowerConsumptionSnapshotter:
    """
    Classe responsável por gerenciar e gerar snapshots filtrados por data 
    a partir do dataset de consumo de energia residencial.
    """

    VERSIONS = {
        "v1": (date(2006, 12, 16), date(2007, 12, 15)),
        "v2": (date(2006, 12, 16), date(2010, 11, 26)),
    }

    def __init__(self, source_path: Path, output_path: Path):
        """
        Inicializa a classe definindo os caminhos de origem e destino dos arquivos.
        """
        self.source_path = source_path
        self.output_path = output_path

    def _validate_version(self, version: str) -> tuple[date, date]:
        """
        Valida se a versão informada é suportada e retorna 
        o intervalo de datas correspondente (data inicial e final).
        """
        if version not in self.VERSIONS:
            raise ValueError("Use v1 ou v2.")
        return self.VERSIONS[version]

    def _ensure_source_exists(self) -> None:
        """
        Verifica se o arquivo de dados original existe no caminho especificado.
        Lança FileNotFoundError caso o arquivo não seja encontrado.
        """
        if not self.source_path.exists():
            raise FileNotFoundError(f"Dataset original não encontrado: {self.source_path}")

    def _print_summary(self, version: str, start_date: date, end_date: date, total: int) -> None:
        """
        Exibe no console um resumo detalhado com as estatísticas do snapshot gerado.
        """
        print(f"Versão gerada: {version.upper()}")
        print(f"Período: {start_date} a {end_date}")
        print(f"Registros: {total:,}")
        print(f"Arquivo: {self.output_path}")
        print(f"Tamanho: {self.output_path.stat().st_size / (1024 * 1024):.2f} MB")

    def create_snapshot(self, version: str) -> None:
        """
        Executa o processo de leitura, filtragem por data e gravação do snapshot 
        com base na versão escolhida.
        """
        start_date, end_date = self._validate_version(version)
        self._ensure_source_exists()

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        total = 0

        with self.source_path.open("r", encoding="utf-8-sig", newline="") as source:
            with self.output_path.open("w", encoding="utf-8", newline="") as output:
                for line_number, line in enumerate(source):
                    if line_number == 0:
                        output.write(line)
                        continue

                    date_text = line.split(";", 1)[0]
                    current_date = datetime.strptime(date_text, "%d/%m/%Y").date()

                    if start_date <= current_date <= end_date:
                        output.write(line)
                        total += 1

        self._print_summary(version, start_date, end_date, total)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python scripts/create_snapshot.py v1|v2")

    SOURCE = Path("data/source/household_power_consumption.txt")
    OUTPUT = Path("data/snapshots/household_power_consumption.txt")

    snapshotter = PowerConsumptionSnapshotter(SOURCE, OUTPUT)
    snapshotter.create_snapshot(sys.argv[1].lower())