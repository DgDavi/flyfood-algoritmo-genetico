import random

from deap import tools

from utils import Crossing, Fitness, LocalSearch, Tournament

from .parameters import (
	PROBABILIDADE_DE_CRUZAMENTO,
	PROBABILIDADE_DE_EMBARALHAR,
	PROBABILIDADE_DE_MUTACAO,
	QUANTIDADE_DE_CIDADES,
	QUANTIDADE_DE_GERACOES_EXECUTADAS,
	TAMANHO_DA_POPULACAO,
)


class GeneticAlgorithm:
	def __init__(self) -> None:
		self.aptidao = 0
		self.melhor_custo = 0
		self.melhor_rota = []

	def initPopulation(self):
		import random

		lista = []

		for _ in range(TAMANHO_DA_POPULACAO):
			individuo = list(range(1, QUANTIDADE_DE_CIDADES+1))
			random.shuffle(individuo)
			lista.append(individuo)

		return lista

	def simulate(self, populacao, distancias):
		self.aptidao = Fitness.calculate(populacao, distancias)

		indice_melhor = self.aptidao.index(min(self.aptidao))

		self.melhor_custo = self.aptidao[indice_melhor]
		self.melhor_rota = populacao[indice_melhor][:]

		for geracao in range(QUANTIDADE_DE_GERACOES_EXECUTADAS):
			novaPop = []

			while len(novaPop) < TAMANHO_DA_POPULACAO:
				pai1 = Tournament.play(populacao, self.aptidao)[:]
				pai2 = Tournament.play(populacao, self.aptidao)[:]

				if random.random() < PROBABILIDADE_DE_CRUZAMENTO:
					pai1, pai2 = Crossing.play(pai1=pai1, pai2=pai2)

				if random.random() < PROBABILIDADE_DE_MUTACAO:
					tools.mutShuffleIndexes(pai1, indpb=PROBABILIDADE_DE_EMBARALHAR)                      

				if random.random() < PROBABILIDADE_DE_MUTACAO:
					tools.mutShuffleIndexes(pai2, indpb=PROBABILIDADE_DE_EMBARALHAR)


				if random.random() < 0.1:
					pai1 = LocalSearch.two_opt(
						pai1, distancias, max_passagens=50
					)

				if random.random() < 0.1:
					pai2 = LocalSearch.two_opt(
						pai2, distancias, max_passagens=50
					)

				novaPop.append(pai1)
				if len(novaPop) < TAMANHO_DA_POPULACAO:
					novaPop.append(pai2)


			populacao = populacao + novaPop
			novaPop = []

			self.aptidao = Fitness.calculate(populacao, distancias)
			
			indice_melhor = self.aptidao.index(min(self.aptidao))
			novaPop.append(populacao[indice_melhor][:])

			# Mantém uma parte dos melhores indivíduos distintos.
			ordenados = sorted(
				range(len(populacao)),
				key=lambda i: self.aptidao[i]
			)

			rotas_vistas = {tuple(novaPop[0])}

			for indice in ordenados:
				if len(novaPop) >= int(TAMANHO_DA_POPULACAO * 0.2):
					break

				rota = tuple(populacao[indice])

				if rota not in rotas_vistas:
					novaPop.append(list(rota))
					rotas_vistas.add(rota)

			# Preenche o restante com descendentes da população combinada.
			while len(novaPop) < TAMANHO_DA_POPULACAO:
				sobrevivente = Tournament.play(populacao, self.aptidao)[:]
				novaPop.append(sobrevivente)

			populacao = novaPop
			self.aptidao = Fitness.calculate(populacao, distancias)
			
			if min(self.aptidao) < self.melhor_custo:
				indice_melhor = self.aptidao.index(min(self.aptidao))

				self.melhor_custo = self.aptidao[indice_melhor]
				self.melhor_rota = populacao[indice_melhor][:]
			
			if geracao % 20 == 0:
				melhor = min(self.aptidao)
				media = sum(self.aptidao) / len(self.aptidao)
				diversidade = len({tuple(ind) for ind in populacao})

				print(
					f"Geração {geracao:4d} | "
					f"melhor: {melhor} | "
					f"histórico: {self.melhor_custo} | "
					f"média: {media:.1f} | "
					f"rotas distintas: {diversidade}/{len(populacao)}"
				)
				
		return self.melhor_custo, self.melhor_rota