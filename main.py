import random

from core import GeneticAlgorithm
from utils import MatrixParsing

distancias = MatrixParsing.parse()

random.seed(42)

genetic_algorthm = GeneticAlgorithm()
populacao = genetic_algorthm.initPopulation()

melhor_custo, melhor_rota = genetic_algorthm.simulate(populacao=populacao, distancias=distancias)


print("\nMelhor custo:", melhor_custo)
print("Melhor rota :", melhor_rota)