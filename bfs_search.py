from collections import deque

"""
    :param start: Posição inicial (tupla)
    :param target: Posição de destino (tupla)
    :param get_neighbors_func: Função que retorna os vizinhos válidos de uma posição
    :param restrict_to: Conjunto (set) de células permitidas para explorar. Se None, explora todas.
    :return: Lista representando o caminho (incluindo start e target), ou None se não achar caminho.
    """
def bfs_search(start, target, get_neighbors_func, restrict_to=None):
    fronteira = deque([[start]])
    explorados = set()
    explorados.add(start)

    while fronteira:
        caminho = fronteira.popleft()
        atual = caminho[-1]

        if atual == target:
            return caminho

        for viz in get_neighbors_func(atual):
            if viz not in explorados:
                # Só explora se não houver restrição ou se estiver na lista de restrições
                if restrict_to is None or viz in restrict_to:
                    novo_caminho = list(caminho)
                    novo_caminho.append(viz)
                    fronteira.append(novo_caminho)
                    explorados.add(viz)
    
    return None # nenhum caminho encontrado
