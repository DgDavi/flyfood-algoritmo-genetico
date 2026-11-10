import random
from time import perf_counter

from core import GeneticAlgorithm
from utils import MatrixParsing

start_time = perf_counter()

distances = MatrixParsing.parse()

random.seed(42)

genetic_algorithm = GeneticAlgorithm()
population = genetic_algorithm.initialize_population()

best_cost, best_route = genetic_algorithm.simulate(
    population=population, distances=distances
)

print("\nBest cost:", best_cost)
print("Best route:", best_route)
elapsed_time = perf_counter() - start_time
print(f"Execution time: {elapsed_time:.2f} seconds")
