from pathlib import Path

from loggibud.v1.data_conversion import to_tsplib
from loggibud.v1.types import CVRPInstance


def convert_file(instance_file: str):
    """Read a data file and converts into a TSPLIB format"""
    loggibud_instance = CVRPInstance.from_file(instance_file)
    tsplib_file_name = f"tsplib_data/{loggibud_instance.name}.vrp"

    if Path(tsplib_file_name).exists():
        print(f"File {loggibud_instance.name} already exists. Skipping")
        return

    print(f"Converting file {loggibud_instance.name}")
    tsplib_instance = to_tsplib(loggibud_instance)
    with open(tsplib_file_name, "w") as f:
        tsplib_instance.write(f)


if __name__ == "__main__":
    path = Path("./data/cvrp-instances-1.0/")

    for instance_file in path.rglob("*.json"):
        convert_file(instance_file)


# Rio: 1000, 600
# DF: 900, 500
# PA: 600, 400
# Deixar simétrico, diag inferior
# Plotar coordenadas
# Adicionar seção de demanda
# De depot
# capacity
