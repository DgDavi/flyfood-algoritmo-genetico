import random

from deap import tools

from utils import Crossing, Fitness, LocalSearch, Progress, Tournament

from .parameters import (
	CROSSOVER_PROBABILITY,
	MUTATION_PROBABILITY,
	NUMBER_OF_CITIES,
	NUMBER_OF_GENERATIONS,
	POPULATION_SIZE,
)


class GeneticAlgorithm:
	def __init__(self) -> None:
		self.fitness: list[int] = []
		self.best_cost = float("inf")
		self.best_route: list[int] | None = None

	def initialize_population(self):
		import random

		population = []

		for _ in range(POPULATION_SIZE):
			individual = list(range(1, NUMBER_OF_CITIES + 1))
			random.shuffle(individual)
			population.append(individual)

		return population

	def simulate(self, population, distances):
		self.evaluate_population(population=population, distances=distances)
		self.update_best(population=population)

		for generation in range(NUMBER_OF_GENERATIONS):

			offspring = self.reproduce(
				population=population,
            	distances=distances,
            	generation=generation
			)

			combined_population = population + offspring

			combined_fitness = Fitness.calculate(
            	combined_population, distances
			)

			population = self.create_new_population(
            	population=combined_population,
            	fitness=combined_fitness
        	)

			self.evaluate_population(population, distances)
			self.update_best(population)

			Progress.print_progress(
				fitness=self.fitness,
				best_cost=self.best_cost,
				generation=generation,
				population=population,
			)

		return self.best_cost, self.best_route

	def evaluate_population(self, population, distances):
		self.fitness = Fitness.calculate(population, distances)

	def update_best(self, population):
		best_index = self.fitness.index(min(self.fitness))

		if self.best_route is None or self.fitness[best_index] < self.best_cost:
			self.best_cost = self.fitness[best_index]
			self.best_route = population[best_index][:]

	def reproduce(self, population, distances, generation):
		offspring = []

		local_search_probability = 0.5 + 0.15 * (generation / NUMBER_OF_GENERATIONS)

		while len(offspring) < POPULATION_SIZE:
			parent1, parent2 = self.select_parents(population)[:]

			son1, son2 = self.crossover(parent1=parent1, parent2=parent2)

			son1 = self.mutate(son1)
			son2 = self.mutate(son2)

			son1 = self.apply_local_search(
            	son1, distances, local_search_probability
			)

			son2 = self.apply_local_search(
				son2, distances, local_search_probability
        	)

			offspring.append(son1)

			if len(offspring) < POPULATION_SIZE:
				offspring.append(son2)

		return offspring

	def select_parents(self, population):
		parent1 = Tournament.play(population, self.fitness)[:]
		parent2 = Tournament.play(population, self.fitness)[:]

		return parent1, parent2

	def crossover(self, parent1, parent2):
		son1 = parent1[:]
		son2 = parent2[:]

		if random.random() < CROSSOVER_PROBABILITY:
			son1, son2 = Crossing.play(
				parent1=parent1,
            	parent2=parent2
        	)

		return son1, son2

	def mutate(self, individual):
		if random.random() < MUTATION_PROBABILITY:
			individual, = tools.mutInversion(individual=individual)

		return individual

	def apply_local_search(self, individual, distances, probability):
		if random.random() < probability:
			individual = LocalSearch.two_opt(
				individual, distances, max_passes=50
			)

		return individual

	def create_new_population(self, population, fitness):
		new_population = []

		# Keep a portion of the best distinct individuals.
		sorted_indices = sorted(
			range(len(population)),
			key=lambda i: fitness[i]
		)

		best_index = sorted_indices[0]
		new_population.append(population[best_index][:])

		seen_routes = {tuple(new_population[0])}

		elite_size = int(POPULATION_SIZE * 0.2)

		for index in sorted_indices:
			if len(new_population) >= elite_size:
				break

			route = tuple(population[index])

			if route not in seen_routes:
				new_population.append(list(route))
				seen_routes.add(route)

		# Fill the remaining slots with offspring from the combined population.
		while len(new_population) < POPULATION_SIZE:
			survivor = Tournament.play(population, fitness)[:]
			new_population.append(survivor)

		return new_population