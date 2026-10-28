# Explicação do `genetic_algorithm.py`

O arquivo [`core/genetic_algorithm.py`](./core/genetic_algorithm.py) implementa o **algoritmo genético** usado para tentar encontrar uma rota de menor custo no problema do caixeiro-viajante, conhecido como **TSP** (*Travelling Salesman Problem*).

Neste projeto, o objetivo é encontrar uma rota que visite as 58 cidades do Brasil exatamente uma vez e retorne à cidade inicial, minimizando a distância total percorrida.

## Função principal no projeto

A classe `GeneticAlgorithm` coordena todo o processo de busca:

1. Criação da população inicial.
2. Avaliação das rotas.
3. Seleção dos melhores indivíduos.
4. Cruzamento entre rotas.
5. Mutação.
6. Aplicação de busca local.
7. Preservação das melhores soluções.
8. Repetição por várias gerações.
9. Retorno da melhor rota encontrada.

Ela funciona como o núcleo do projeto. Os outros módulos fornecem operações específicas, enquanto esse arquivo organiza a execução do algoritmo.

## 1. Inicialização da classe

```python
def __init__(self) -> None:
    self.fitness = 0
    self.best_cost = 0
    self.best_route = []
```

Esses atributos armazenam o estado do algoritmo:

- `fitness`: custos associados às rotas da população atual.
- `best_cost`: menor distância encontrada até o momento.
- `best_route`: rota correspondente ao menor custo encontrado.

O valor de `best_cost` é atualizado logo após a avaliação da população inicial.

## 2. Criação da população inicial

```python
def initialize_population(self):
```

Esse método cria a primeira população de soluções.

Para cada indivíduo:

```python
individual = list(range(1, NUMBER_OF_CITIES + 1))
random.shuffle(individual)
```

É criada uma lista contendo as cidades de `1` a `58`. Depois, essa lista é embaralhada aleatoriamente.

Um indivíduo representa uma possível rota, por exemplo:

```text
[12, 4, 33, 1, 58, 20, ...]
```

Cada rota contém todas as 58 cidades em uma ordem diferente.

A quantidade de indivíduos é definida por:

```python
POPULATION_SIZE = 200
```

Portanto, a população inicial possui 200 rotas aleatórias.

## 3. Avaliação da população

O método principal é:

```python
def simulate(self, population, distances):
```

Ele recebe:

- `population`: conjunto de rotas.
- `distances`: dicionário contendo as distâncias entre as cidades.

A avaliação é feita por:

```python
self.fitness = Fitness.calculate(population, distances)
```

Para cada rota, o projeto calcula o custo total do percurso. Uma rota é considerada melhor quando possui um valor menor de `fitness`.

Por exemplo, se os custos forem:

```text
[12500, 10300, 11800, 9800]
```

A melhor rota é a de custo `9800`.

Inicialmente, o algoritmo encontra a melhor rota da população inicial:

```python
best_index = self.fitness.index(min(self.fitness))
self.best_cost = self.fitness[best_index]
self.best_route = population[best_index][:]
```

## 4. Execução das gerações

O algoritmo executa várias gerações:

```python
for generation in range(NUMBER_OF_GENERATIONS):
```

No projeto:

```python
NUMBER_OF_GENERATIONS = 200
```

Cada geração tenta produzir uma população melhor que a anterior.

## 5. Seleção dos pais

Dentro de cada geração, duas rotas são escolhidas usando torneio:

```python
parents1 = Tournament.play(population, self.fitness)[:]
parents2 = Tournament.play(population, self.fitness)[:]
```

O método `Tournament.play` escolhe alguns indivíduos aleatoriamente e retorna o melhor deles.

Isso favorece rotas com menor custo, mas ainda mantém certa aleatoriedade para evitar que o algoritmo fique preso muito rapidamente em uma solução ruim.

O tamanho do torneio é definido por:

```python
TOURNAMENT_SIZE = 3
```

## 6. Cruzamento

Depois da seleção, os dois pais podem ser combinados:

```python
if random.random() < CROSSOVER_PROBABILITY:
    sons1, sons2 = Crossing.play(
        parent1=parents1,
        parent2=parents2
    )
```

A probabilidade de cruzamento está definida como:

```python
CROSSOVER_PROBABILITY = 1.0
```

Isso significa que o cruzamento ocorre sempre.

O cruzamento combina partes das duas rotas para gerar dois descendentes. Como uma rota do TSP não pode repetir cidades, o projeto utiliza o cruzamento ordenado da biblioteca `DEAP`.

Exemplo conceitual:

```text
Pai 1: [1, 2, 3, 4, 5]
Pai 2: [5, 4, 3, 2, 1]

Filho: [1, 4, 3, 2, 5]
```

O resultado precisa continuar sendo uma permutação válida das cidades.

## 7. Mutação

Cada descendente pode sofrer mutação:

```python
if random.random() < MUTATION_PROBABILITY:
    tools.mutShuffleIndexes(
        sons1,
        indpb=SHUFFLE_PROBABILITY
    )
```

A mutação embaralha algumas posições da rota.

As configurações são:

```python
MUTATION_PROBABILITY = 0.2
SHUFFLE_PROBABILITY = 0.05
```

Isso significa:

- Existe 20% de chance de um descendente sofrer mutação.
- Cada posição possui 5% de chance de ser embaralhada durante a mutação.

A mutação adiciona diversidade à população e ajuda o algoritmo a explorar novas possibilidades.

## 8. Busca local com `2-opt`

Depois do cruzamento e da mutação, existe uma chance de aplicar uma melhoria local:

```python
if random.random() < 0.1:
    sons1 = LocalSearch.two_opt(
        sons1,
        distances,
        max_passes=50
    )
```

Essa operação tem 10% de chance de ser aplicada a cada descendente.

O algoritmo `2-opt` tenta melhorar uma rota invertendo trechos dela. Ele compara:

- O custo das conexões atuais.
- O custo depois de inverter uma parte da rota.

Se a inversão reduzir a distância total, ela é mantida.

Essa combinação entre algoritmo genético e busca local é conhecida como uma abordagem híbrida ou **algoritmo memético**. O algoritmo genético explora soluções novas, enquanto o `2-opt` melhora localmente as soluções encontradas.

## 9. Construção da nova população

Os descendentes são adicionados à nova população:

```python
new_population.append(sons1)

if len(new_population) < POPULATION_SIZE:
    new_population.append(sons2)
```

Esse processo continua até a nova população atingir 200 indivíduos.

Depois, a população antiga e os descendentes são combinados:

```python
population = population + new_population
```

Nesse momento, a população temporária possui indivíduos antigos e novos.

## 10. Elitismo e diversidade

O algoritmo calcula novamente o custo de todas as rotas combinadas:

```python
self.fitness = Fitness.calculate(population, distances)
```

A melhor rota é preservada diretamente:

```python
best_index = self.fitness.index(min(self.fitness))
new_population.append(population[best_index][:])
```

Isso é chamado de **elitismo**. A melhor solução não é perdida durante a reprodução.

Depois, o algoritmo ordena as rotas pelo custo:

```python
sorted_indices = sorted(
    range(len(population)),
    key=lambda i: self.fitness[i]
)
```

Ele mantém uma parte das melhores rotas distintas:

```python
if len(new_population) >= int(POPULATION_SIZE * 0.2):
    break
```

Como `POPULATION_SIZE` é 200, aproximadamente 20% da nova população é formada pelas melhores rotas diferentes.

Essa estratégia evita que a população fique composta apenas por cópias da mesma rota.

## 11. Preenchimento da população

Depois de preservar os melhores indivíduos, o restante da população é preenchido usando novamente seleção por torneio:

```python
while len(new_population) < POPULATION_SIZE:
    survivor = Tournament.play(
        population,
        self.fitness
    )[:]

    new_population.append(survivor)
```

Assim, as rotas mais promissoras têm maior chance de continuar existindo na próxima geração.

## 12. Atualização da melhor solução histórica

Após formar a nova população, o algoritmo verifica se surgiu uma rota melhor:

```python
if min(self.fitness) < self.best_cost:
    best_index = self.fitness.index(min(self.fitness))

    self.best_cost = self.fitness[best_index]
    self.best_route = population[best_index][:]
```

Se o menor custo da geração atual for menor que o melhor custo histórico, a rota é armazenada.

Essa variável histórica é importante porque uma geração posterior pode ter uma população pior que uma geração anterior. Nesse caso, o algoritmo ainda conserva a melhor solução já encontrada.

## 13. Exibição do progresso

A cada 20 gerações, o algoritmo imprime informações:

```python
if generation % 20 == 0:
```

Ele exibe:

- Número da geração.
- Melhor custo da geração.
- Melhor custo histórico.
- Custo médio da população.
- Quantidade de rotas distintas.

Exemplo:

```text
Generation   20 | best: 9500 | historical best: 9300 |
average: 11200.4 | distinct routes: 174/200
```

Isso permite acompanhar a evolução da solução e medir a diversidade da população.

## 14. Resultado final

Ao terminar as 200 gerações, o método retorna:

```python
return self.best_cost, self.best_route
```

Ou seja:

```text
melhor custo encontrado
melhor rota encontrada
```

Esses valores são utilizados pelo arquivo [`lerBrasil58.py`](./lerBrasil58.py), que apresenta o resultado ao usuário.

## Resumo

O arquivo [`core/genetic_algorithm.py`](./core/genetic_algorithm.py) é o controlador do processo de otimização. Ele não calcula diretamente todas as distâncias nem implementa sozinho cada operação genética. Em vez disso, coordena os módulos:

- `Fitness`: calcula o custo de cada rota.
- `Tournament`: seleciona os pais e sobreviventes.
- `Crossing`: realiza o cruzamento.
- `DEAP`: executa a mutação.
- `LocalSearch`: aplica a melhoria `2-opt`.
- `parameters.py`: fornece os parâmetros do algoritmo.

A função dele no projeto é transformar uma população inicial de rotas aleatórias em soluções progressivamente melhores para o TSP Brasil 58.
