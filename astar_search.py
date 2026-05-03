from heapq import heappush, heappop

# Calcula quantos passos mínimos existem entre dois pontos numa grade (sem andar na diagonal)
# Ex: de (0,0) até (2,3) = 2 passos para baixo + 3 para o lado = 5 passos no mínimo
def distancia_manhattan(ponto_a, ponto_b):
    return abs(ponto_a[0] - ponto_b[0]) + abs(ponto_a[1] - ponto_b[1])

def astar_search(posicao_inicial, posicao_alvo, obter_vizinhos, celulas_permitidas=None):
    """
    Busca A* (A-Star): encontra o caminho mais curto de um ponto a outro.
    
    Diferente do BFS, o A* usa uma "bússola" (distância_manhattan) para priorizar
    os caminhos que já estão mais perto do destino — explorando menos células.
    
    :param posicao_inicial: Onde o agente está agora (tupla, ex: (0, 0))
    :param posicao_alvo: Onde o agente quer chegar (tupla, ex: (3, 3))
    :param obter_vizinhos: Função que diz quais células estão ao lado de uma posição
    :param celulas_permitidas: Se informado, o agente só pode passar por essas células
    :return: Lista de posições do caminho encontrado, ou None se não houver caminho
    """

    # Fila de candidatos ordenada por prioridade (menor custo_total sai primeiro)
    # Cada item da fila é uma tupla: (custo_total, passos_dados, desempate, posicao, caminho)
    fila_de_candidatos = []

    # Calcula a estimativa inicial: 0 passos dados + distância até o alvo
    estimativa_inicial = distancia_manhattan(posicao_inicial, posicao_alvo)
    heappush(fila_de_candidatos, (estimativa_inicial, 0, 0, posicao_inicial, [posicao_inicial]))

    # Guarda quantos passos reais foram dados para chegar em cada célula já visitada
    # Serve para ignorar caminhos piores que já encontramos antes
    menor_passos_para_celula = {posicao_inicial: 0}

    # Contador usado apenas para desempatar quando dois caminhos têm o mesmo custo
    desempate = 1

    while fila_de_candidatos:
        # Retira o candidato com menor custo_total da fila
        custo_total, passos_dados, _, posicao_atual, caminho_ate_aqui = heappop(fila_de_candidatos)

        # Chegamos ao destino! Retorna o caminho completo percorrido
        if posicao_atual == posicao_alvo:
            return caminho_ate_aqui

        # Se já encontramos um caminho mais curto para essa célula antes, ignora esse
        if passos_dados > menor_passos_para_celula.get(posicao_atual, float('inf')):
            continue

        # Avalia cada célula vizinha da posição atual
        for vizinho in obter_vizinhos(posicao_atual):

            # Só considera o vizinho se não houver restrição ou se ele for uma célula permitida
            if celulas_permitidas is None or vizinho in celulas_permitidas:

                # Custo real para chegar nesse vizinho = passos dados até aqui + 1
                passos_para_vizinho = passos_dados + 1

                # Só vale a pena explorar esse vizinho se esse é o caminho mais curto até ele
                if passos_para_vizinho < menor_passos_para_celula.get(vizinho, float('inf')):
                    menor_passos_para_celula[vizinho] = passos_para_vizinho

                    # Custo total = passos reais já dados + estimativa de passos que ainda faltam
                    custo_total_vizinho = passos_para_vizinho + distancia_manhattan(vizinho, posicao_alvo)

                    # Adiciona o vizinho à fila com o caminho atualizado
                    caminho_atualizado = list(caminho_ate_aqui)
                    caminho_atualizado.append(vizinho)
                    heappush(fila_de_candidatos, (custo_total_vizinho, passos_para_vizinho, desempate, vizinho, caminho_atualizado))
                    desempate += 1

    # Nenhum caminho foi encontrado até o destino
    return None
