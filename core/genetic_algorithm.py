import random

from deap import tools

from utils import Crossing, Fitness, LocalSearch, Tournament

from .parameters import (
	CROSSOVER_PROBABILITY,
	MUTATION_PROBABILITY,
	NUMBER_OF_CITIES,
	NUMBER_OF_GENERATIONS,
	POPULATION_SIZE,
	SHUFFLE_PROBABILITY,
)


class GeneticAlgorithm:
	def __init__(self) -> None:
		self.fitness = 0
		self.best_cost = 0
		self.best_route = []

	def initialize_population(self):
		import random

		population = []

		for _ in range(POPULATION_SIZE):
			individual = list(range(1, NUMBER_OF_CITIES + 1))
			random.shuffle(individual)
			population.append(individual)

		return population

	def simulate(self, population, distances):
		self.fitness = Fitness.calculate(population, distances)

		best_index = self.fitness.index(min(self.fitness))

		self.best_cost = self.fitness[best_index]
		self.best_route = population[best_index][:]

		for generation in range(NUMBER_OF_GENERATIONS):
			new_population = []

			while len(new_population) < POPULATION_SIZE:
				parents1 = Tournament.play(population, self.fitness)[:]
				parents2 = Tournament.play(population, self.fitness)[:]

				sons1 = []
				sons2 = []
				
				if random.random() < CROSSOVER_PROBABILITY:
					sons1, sons2 = Crossing.play(parent1=parents1, parent2=parents2)

				if random.random() < MUTATION_PROBABILITY:
					tools.mutShuffleIndexes(sons1, indpb=SHUFFLE_PROBABILITY)

				if random.random() < MUTATION_PROBABILITY:
					tools.mutShuffleIndexes(sons2, indpb=SHUFFLE_PROBABILITY)


				if random.random() < 0.1:
					sons1 = LocalSearch.two_opt(
						sons1, distances, max_passes=50
					)

				if random.random() < 0.1:
					sons2 = LocalSearch.two_opt(
						sons2, distances, max_passes=50
					)

				new_population.append(sons1)
				if len(new_population) < POPULATION_SIZE:
					new_population.append(sons2)


			population = population + new_population
			new_population = []

			self.fitness = Fitness.calculate(population, distances)
			
			best_index = self.fitness.index(min(self.fitness))
			new_population.append(population[best_index][:])

			# Keep a portion of the best distinct individuals.
			sorted_indices = sorted(
				range(len(population)),
				key=lambda i: self.fitness[i]
			)

			seen_routes = {tuple(new_population[0])}

			for index in sorted_indices:
				if len(new_population) >= int(POPULATION_SIZE * 0.2):
					break

				route = tuple(population[index])

				if route not in seen_routes:
					new_population.append(list(route))
					seen_routes.add(route)

			# Fill the remaining slots with offspring from the combined population.
			while len(new_population) < POPULATION_SIZE:
				survivor = Tournament.play(population, self.fitness)[:]
				new_population.append(survivor)

			population = new_population
			self.fitness = Fitness.calculate(population, distances)
			
			if min(self.fitness) < self.best_cost:
				best_index = self.fitness.index(min(self.fitness))

				self.best_cost = self.fitness[best_index]
				self.best_route = population[best_index][:]
			
			if generation % 1 == 0:
				best = min(self.fitness)
				average = sum(self.fitness) / len(self.fitness)
				diversity = len({tuple(individual) for individual in population})

				print(
					f"Generation {generation:4d} | "
					f"best: {best} | "
					f"historical best: {self.best_cost} | "
					f"average: {average:.1f} | "
					f"distinct routes: {diversity}/{len(population)}"
				)
				
		return self.best_cost, self.best_route