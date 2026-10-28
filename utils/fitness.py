from utils import CostPath


class Fitness:
    @staticmethod
    def calculate(population, distances):
        fitness_values = []
       
        for individual in population:
            fitness_values.append(CostPath.calculate(individual, distances))
       
        return fitness_values