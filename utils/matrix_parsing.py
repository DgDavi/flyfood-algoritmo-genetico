from pathlib import Path

from core.parameters import NUMBER_OF_CITIES

class MatrixParsing:
    @staticmethod
    def parse(file_path="brazil58.tsp"):
        path = Path(__file__).resolve().parent.parent / file_path
        content = path.read_text(encoding="utf-8")
        marker = "EDGE_WEIGHT_SECTION"
        if marker not in content:
            raise ValueError(f"Arquivo {path.name} não contém {marker}.")

        weights = [
            int(value)
            for value in content.split(marker, 1)[1].split()
            if value.lstrip("+-").isdigit()
        ]
        expected = NUMBER_OF_CITIES * (NUMBER_OF_CITIES - 1) // 2
        if len(weights) != expected:
            raise ValueError(
                f"Arquivo {path.name} deveria conter {expected} distâncias, "
                f"mas contém {len(weights)}."
            )

        distances = {}
        weight_index = 0
        for i in range(1, NUMBER_OF_CITIES):
            for j in range(i + 1, NUMBER_OF_CITIES + 1):
                weight = weights[weight_index]
                weight_index += 1
                distances[(i, j)] = weight
                distances[(j, i)] = weight
        return distances
