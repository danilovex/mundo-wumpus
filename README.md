# Mundo do Wumpus - Agente Inteligente

## Descrição
Este projeto implementa uma solução baseada em Inteligência Artificial para o clássico problema do **Mundo do Wumpus**. O objetivo é desenvolver um agente autônomo capaz de explorar uma caverna (representada por uma matriz bidimensional, ex: 8x8), identificar a localização de perigos (abismos e o monstro Wumpus) através de percepções sensoriais como brisa e mau cheiro, atirar flechas quando necessário, coletar o ouro e retornar com segurança à origem.

Este projeto foi desenvolvido como parte de uma disciplina do curso de **Mestrado da UNIFESP** (Universidade Federal de São Paulo).

## Arquitetura e Algoritmos
O agente utiliza Inferência Lógica para construir uma base de conhecimento sobre células 100% seguras. Para a navegação até essas células e o retorno à origem, o projeto compara dois algoritmos clássicos de *Pathfinding*:
- **Busca em Largura (BFS):** Exploração sistemática e exaustiva para encontrar o menor caminho.
- **Busca A* (A-Star):** Busca heurística guiada pela Distância de Manhattan, priorizando explorar caminhos que levam de forma mais direta ao destino.

A arquitetura foi pensada segundo os princípios do **Clean Code**, separando ambiente, lógica de agente e estratégias de busca (via Injeção de Dependência) em módulos distintos.

## Tecnologias Utilizadas
- **Linguagem:** Python (3.7+)
- **Bibliotecas:** Apenas pacotes nativos do Python (`collections`, `heapq`, `random`, `enum`, `copy`, `time`, `argparse`, `tkinter`), sem necessidade de dependências externas.

## Como Executar e Usar

A aplicação não requer a instalação de pacotes externos (`pip install`). Basta ter o Python configurado na sua máquina.

1. Clone o repositório ou extraia os arquivos do projeto.
2. Navegue até a pasta do projeto via terminal.
3. Para iniciar a simulação rápida via terminal (comparativo), execute o arquivo principal:

```bash
python main.py
```
O script irá gerar um mapa aleatório, executar as tomadas de decisão utilizando primeiro o algoritmo **BFS** e depois o **A*** no mesmo cenário exato. Ao final, imprimirá no console um comparativo detalhado com a pontuação (Score) e o Tempo de Execução de cada um.

### Simulação Gráfica (Tkinter)
Para **assistir** ao agente explorando a caverna passo a passo em tempo real com uma Interface Gráfica, execute:

```bash
python gui.py
```
* **Opções adicionais da interface:**
  Você pode customizar a velocidade (segundos por passo) e qual algoritmo usar:
  ```bash
  python gui.py --search bfs --speed 1.0
  ```
  *(Opções de search: `bfs` ou `astar`)*

## Estrutura de Arquivos
- `gui.py` - Ponto de entrada da Interface Gráfica (Simulação passo a passo).
- `main.py` - Ponto de entrada via terminal; configura e executa as simulações comparativas.
- `agent.py` - Contém a classe `WumpusAgent` (o cérebro e a memória do robô explorador).
- `wumpus_world_env.py` - Implementa o `WumpusWorldEnv` (regras físicas, morte, sorteio do mapa e retornos sensoriais do jogo).
- `bfs_search.py` - Lógica isolada da Busca em Largura.
- `astar_search.py` - Lógica isolada da Busca A*.
- `enums.py` - Definições de Percepções e Direções de movimento.
