from typing import TYPE_CHECKING

from .parameters import (
    CROSSOVER_PROBABILITY,
    MUTATION_PROBABILITY,
    NUMBER_OF_CITIES,
    NUMBER_OF_GENERATIONS,
    POPULATION_SIZE,
    SHUFFLE_PROBABILITY,
    TOURNAMENT_SIZE,
)

if TYPE_CHECKING:
    from .genetic_algorithm import GeneticAlgorithm


def __getattr__(name):
    if name == "GeneticAlgorithm":
        from .genetic_algorithm import GeneticAlgorithm

        return GeneticAlgorithm

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "CROSSOVER_PROBABILITY",
    "MUTATION_PROBABILITY",
    "NUMBER_OF_CITIES",
    "NUMBER_OF_GENERATIONS",
    "POPULATION_SIZE",
    "SHUFFLE_PROBABILITY",
    "TOURNAMENT_SIZE",
    "GeneticAlgorithm",
]