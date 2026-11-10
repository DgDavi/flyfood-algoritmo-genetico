# Flyfood / TSP Brasil 58

Este repositório implementa uma solução para o problema do caixeiro-viajante (TSP) usando um algoritmo genético híbrido para encontrar uma rota com menor custo para 58 cidades brasileiras.

O projeto foi estruturado em módulos para separar a lógica de otimização, avaliação da rota, seleção, cruzamento, mutação e busca local.

## Objetivo

Resolver o TSP para as cidades representadas no arquivo `edgesbrasil58.tsp`, buscando uma permutação de cidades que minimize a distância total percorrida, respeitando a condição de visitar cada cidade exatamente uma vez e retornar à origem.

## Estrutura do projeto

```text
.
├── README.md
├── lerBrasil58.py
├── brazil58.tsp
├── edgesbrasil58.tsp
├── flyfood.tsp
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── genetic_algorithm.py
│   └── parameters.py
└── utils/
    ├── __init__.py
    ├── cost_path.py
    ├── crossing.py
    ├── fitness.py
    ├── matrix_parsing.py
    ├── progress.py
    ├── tournament.py
    └── two_opt.py
```

## Componentes principais

### `lerBrasil58.py`
Script principal que executa o algoritmo. Ele:

1. carrega a matriz de distâncias,
2. inicializa a população,
3. executa as gerações do algoritmo genético,
4. imprime a melhor rota e o menor custo encontrado,
5. exibe o tempo total de execução.

### `core/parameters.py`
Contém as configurações do problema e do algoritmo, como:

- `NUMBER_OF_CITIES = 58`
- `POPULATION_SIZE = 200`
- `NUMBER_OF_GENERATIONS = 80`
- `MUTATION_PROBABILITY = 0.2`
- `CROSSOVER_PROBABILITY = 1.0`
- `TOURNAMENT_SIZE = 3`

### `core/genetic_algorithm.py`
Classe central do projeto. Ela coordena:

- criação da população inicial,
- avaliação de cada rota,
- seleção de pais por torneio,
- cruzamento ordenado,
- mutação por inversão,
- busca local com `2-opt`,
- preservação das melhores rotas,
- execução ao longo de várias gerações.

### `utils/matrix_parsing.py`
Lê o arquivo de distâncias e monta um dicionário em formato `(i, j) -> peso`, permitindo acesso bidirecional entre cidades.

O projeto usa `edgesbrasil58.tsp` por padrão:

```python
file_object = open("edgesbrasil58.tsp")
```

Há também os arquivos alternativos `brazil58.tsp` e `flyfood.tsp`, que podem ser utilizados ao ajustar o ponto de leitura do arquivo.

## Como o algoritmo funciona

O fluxo principal é:

1. gerar uma população inicial com rotas aleatórias;
2. calcular o custo de cada rota;
3. selecionar os melhores indivíduos para reprodução;
4. gerar novos filhos por cruzamento;
5. aplicar mutação e busca local;
6. manter somente as melhores rotas na população;
7. repetir até atingir o número de gerações configurado.

### Seleção
A seleção é feita por torneio (`Tournament.play`), que escolhe alguns indivíduos aleatoriamente e retorna o melhor custo entre eles.

### Cruzamento
O cruzamento usa `tools.cxOrdered` da biblioteca DEAP para gerar filhos válidos sem repetir cidades.

### Mutação
A mutação é implementada por `tools.mutInversion`, invertendo um trecho da rota para introduzir diversidade.

### Busca local
A busca local `2-opt` tenta melhorar a rota invertendo segmentos em busca de redução na distância total.

## Dependências

O projeto usa as bibliotecas abaixo, listadas em `requirements.txt`:

- `deap==1.4.4`
- `numpy==2.5.4`
- `more-itertools==0.3.2`
- `platformdirs==4.13.7`
- `pyparsing==3.12`

Observação: o arquivo `requirements.txt` parece estar salvo em codificação UTF-16. Em alguns ambientes, isso pode causar erro ao instalar com `pip`. Se necessário, converta antes:

```bash
iconv -f utf-16 -t utf-8 requirements.txt > requirements_utf8.txt
python -m pip install -r requirements_utf8.txt
```

## Como executar

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install deap==1.4.4 numpy==2.5.4
```

Se preferir, use o arquivo de dependências convertido:

```bash
iconv -f utf-16 -t utf-8 requirements.txt > requirements_utf8.txt
python -m pip install -r requirements_utf8.txt
```

Em seguida, execute:

```bash
python lerBrasil58.py
```

A saída esperada inclui:

- melhor custo encontrado;
- melhor rota encontrada;
- tempo total de execução.

## Dicas

- Para trocar o conjunto de cidades, ajuste o nome do arquivo lido em `utils/matrix_parsing.py`.
- Para alterar o comportamento do algoritmo, edite os parâmetros em `core/parameters.py`.
- O código é adequado para experimentação e tuning de parâmetros do algoritmo genético.

## Observações

Este projeto é um exemplo de combinação entre:

- algoritmo genético para exploração global,
- heurística `2-opt` para refinamento local,
- estrutura modular em Python para facilitar manutenção e testes.

Ele é útil como base para estudos de otimização combinatória, TSP e metaheurísticas.
