import random

from core import GeneticAlgorithm
from utils import MatrixParsing

distances = MatrixParsing.parse()

random.seed(42)

genetic_algorithm = GeneticAlgorithm()
population = genetic_algorithm.initialize_population()

best_cost, best_route = genetic_algorithm.simulate(
    population=population, distances=distances
)

print("\nBest cost:", best_cost)
print("Best route:", best_route)