from typing import TYPE_CHECKING

from .parameters import (
    PROBABILIDADE_DE_CRUZAMENTO,
    PROBABILIDADE_DE_EMBARALHAR,
    PROBABILIDADE_DE_MUTACAO,
    QUANTIDADE_DE_CIDADES,
    QUANTIDADE_DE_GERACOES_EXECUTADAS,
    TAMANHO_DA_POPULACAO,
    TORNEIO,
)

if TYPE_CHECKING:
    from .genetic_algorithm import GeneticAlgorithm


def __getattr__(name):
    if name == "GeneticAlgorithm":
        from .genetic_algorithm import GeneticAlgorithm

        return GeneticAlgorithm

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "PROBABILIDADE_DE_CRUZAMENTO",
    "PROBABILIDADE_DE_EMBARALHAR",
    "PROBABILIDADE_DE_MUTACAO",
    "QUANTIDADE_DE_CIDADES",
    "QUANTIDADE_DE_GERACOES_EXECUTADAS",
    "TAMANHO_DA_POPULACAO",
    "TORNEIO",
    "GeneticAlgorithm",
]