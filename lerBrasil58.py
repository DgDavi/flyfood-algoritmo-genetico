import random
from deap import tools

objArq = open("edgesbrasil58.tsp")

distancias = {}

for i in range(1, 58):
	linha = objArq.readline() 
	
	lista = linha.split() 

	for j in range(i+1, 59):
		if len(lista) > 0:
			peso = int(lista.pop(0)) 
		else:
			print(f"Erro! linha {i} do arquivo não possui elementos suficientes")
			exit()

		distancias[(i,j)] = peso
		distancias[(j,i)] = peso

objArq.close()

def custoCaminho(permutacao, dicDistancias):
	soma = 0
	for i in range(len(permutacao)-1):
		a = permutacao[i]
		b = permutacao[i+1]
		if (a,b) in dicDistancias:
			soma += dicDistancias[(a,b)]
		else:
			print(f"Erro! ({a},{b}) não existe no dicionario!")
			exit()

	soma += dicDistancias[(permutacao[-1],permutacao[0])]
	return soma

def inicializaPopulacao(tamanho, qtdeCidades):
	import random

	lista = []
	for i in range(tamanho):
		individuo = list(range(1, qtdeCidades+1))
		random.shuffle(individuo)
		lista.append(individuo)
	return lista

def calculaAptidao(populacao, dicDistancias):
	listaAptidao = []
	for elem in populacao:
		listaAptidao.append(custoCaminho(elem, dicDistancias))
	return listaAptidao

QUANTIDADE_DE_CIDADES = 58
TAMANHO_DA_POPULACAO = 200
QUANTIDADE_DE_GERACOES_EXECUTADAS = 1000
PROBABILIDADE_DE_MUTACAO = 0.5
PROBABILIDADE_DE_EMBARALHAR = 0.05
PROBABILIDADE_DE_CRUZAMENTO = 0.4
TORNEIO = 3

def cruzamentoOX(pai1, pai2):
    filho1 = [cidade - 1 for cidade in pai1]
    filho2 = [cidade - 1 for cidade in pai2]

    tools.cxOrdered(filho1, filho2)
	
    filho1 = [cidade + 1 for cidade in filho1]
    filho2 = [cidade + 1 for cidade in filho2]

    return filho1, filho2

def torneio(populacao, aptidoes, k=TORNEIO) :
	candidatos = random.sample(range(len(populacao)), k)
	melhor = min(candidatos, key=lambda idx: aptidoes[idx])
	return populacao[melhor]

random.seed(42)

populacao = inicializaPopulacao(TAMANHO_DA_POPULACAO, QUANTIDADE_DE_CIDADES)

aptidao = calculaAptidao(populacao,  distancias)
melhorCusto = min(aptidao)
melhorRota = populacao[aptidao.index(min(aptidao))][:]

for geracao in range(QUANTIDADE_DE_GERACOES_EXECUTADAS):
	novaPop = []

	while len(novaPop) < TAMANHO_DA_POPULACAO:
		pai1 = torneio(populacao, aptidao)[:]
		pai2 = torneio(populacao, aptidao)[:]

		if random.random() < PROBABILIDADE_DE_CRUZAMENTO:
			pai1, pai2 = cruzamentoOX(pai1=pai1, pai2=pai2)

		if random.random() < PROBABILIDADE_DE_MUTACAO:
			tools.mutShuffleIndexes(pai1, indpb=PROBABILIDADE_DE_EMBARALHAR)                      

		if random.random() < PROBABILIDADE_DE_MUTACAO:
			tools.mutShuffleIndexes(pai2, indpb=PROBABILIDADE_DE_EMBARALHAR)

		novaPop.append(pai1)
		if len(novaPop) < TAMANHO_DA_POPULACAO:
			novaPop.append(pai2)


	populacao = populacao + novaPop
	novaPop = []

	aptidao = calculaAptidao(populacao, distancias) 
	
	novaPop.append(populacao[aptidao.index(min(aptidao))][:])

	while len(novaPop) < TAMANHO_DA_POPULACAO:
		sobrevivente = torneio(populacao, aptidao)[:]
		novaPop.append(sobrevivente)

	populacao = novaPop
	aptidao = calculaAptidao(populacao, distancias) 
	
	if min(aptidao)< melhorCusto:
		melhorCusto = min(aptidao)
		melhorRota = populacao[aptidao.index(melhorCusto)][:]

	if geracao % 20 == 0:
		print(f"Geração {geracao:3d} | melhor: {min(aptidao)} | média: {sum(aptidao)/len(aptidao):.1f}")

print("\nMelhor custo:", melhorCusto)
print("Melhor rota :", melhorRota)