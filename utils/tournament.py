import random

from core.parameters import TOURNAMENT_SIZE


class Tournament:

    @staticmethod
    def play(population, fitness_values, k=TOURNAMENT_SIZE):

        if len(population) != len(fitness_values):
            raise ValueError("Population and fitness values must have the same size.")

        if not 1 <= k <= len(population):
            raise ValueError("TOURNAMENT_SIZE must be between 1 and the population size.")
        
        candidates = random.sample(range(len(population)), k)

        best = min(candidates, key=lambda idx: fitness_values[idx])
        
        return population[best]