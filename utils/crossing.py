from deap import tools


class Crossing:
    @staticmethod
    def play(parent1, parent2):
        child1 = [city - 1 for city in parent1]
        child2 = [city - 1 for city in parent2]

        tools.cxOrdered(child1, child2)
        
        child1 = [city + 1 for city in child1]
        child2 = [city + 1 for city in child2]

        return child1, child2