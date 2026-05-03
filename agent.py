import random
from enums import PerceptEnum, DirectionEnum

class WumpusAgent:
    def __init__(self, env, search_strategy, on_step=None):
        """
        Inicia o agente no Mundo do Wumpus.
        
        :param env: A instância do ambiente (WumpusWorldEnv).
        :param search_strategy: Função de busca que será usada para pathfinding.
                                Deve ter a assinatura: func(start, target, get_neighbors, restrict_to)
        :param on_step: Callback (função) opcional chamada a cada ação importante para atualizar a UI.
        """
        self.agent_pos_actual = (0,0)
        self.has_gold = False
        
        self.safe_cells = set()
        self.safe_cells.add((0,0))
        
        self.visited = set()
        self.no_abyss = set([(0,0)])
        self.no_wumpus = set([(0,0)])

        self.env = env
        self.search_strategy = search_strategy
        self.on_step = on_step

    def _get_vizinhos(self, pos):
        x, y = pos
        vizinhos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [v for v in vizinhos if self.env._is_valid_position(v)]

    def _find_path(self, start, target, restrict_to=None):
        # Delega a busca para a estratégia injetada
        return self.search_strategy(start, target, self._get_vizinhos, restrict_to)

    def move_to(self, next_pos):
        x, y = self.agent_pos_actual
        nx, ny = next_pos
        if nx == x - 1:
            self.env.move_agent(DirectionEnum.UP)
        elif nx == x + 1:
            self.env.move_agent(DirectionEnum.DOWN)
        elif ny == y - 1:
            self.env.move_agent(DirectionEnum.LEFT)
        elif ny == y + 1:
            self.env.move_agent(DirectionEnum.RIGHT)
        self.agent_pos_actual = self.env.agent_pos
        
        if self.on_step:
            self.on_step(self)

    def resolve_problem(self):
        print("Iniciando exploração do Mundo do Wumpus...")
        if self.on_step:
            self.on_step(self) # Mostra o estado inicial
            
        while not self.has_gold and self.env.agent_alive:
            curr = self.agent_pos_actual
            self.visited.add(curr)
            percepts = self.env.get_percepts()
            
            percept_names = [p.value for p in percepts]
            print(f"Agente em {curr} | Percepções: {percept_names}")
            
            if PerceptEnum.SCREAM in percepts:
                print("Ouvimos um grito! O Wumpus morreu.")
                
            if PerceptEnum.GLITTER in percepts:
                print("Ouro encontrado! Pegando...")
                self.env.grab_gold()
                self.has_gold = True
                
                if self.on_step:
                    self.on_step(self) # Atualiza a tela após pegar o ouro
                
                print("Retornando para a origem...")
                caminho = self._find_path(self.agent_pos_actual, (0,0), restrict_to=self.safe_cells)
                if caminho:
                    for pos in caminho[1:]:
                        self.move_to(pos)
                        print(f"Agente moveu para {self.agent_pos_actual}")
                
                if self.env.climb_out():
                    print(f"Agente saiu da caverna com sucesso! Score final: {self.env.score}")
                return True
                
            # Atirar a flecha ao sentir mau cheiro
            if PerceptEnum.STENCH in percepts and self.env._arrow_available():
                suspect_vizinhos = [v for v in self._get_vizinhos(curr) if v not in self.visited and v not in self.safe_cells]
                if suspect_vizinhos:
                    alvo = random.choice(suspect_vizinhos)
                    direction = None
                    if alvo[0] == curr[0] - 1:
                        direction = DirectionEnum.UP
                    elif alvo[0] == curr[0] + 1:
                        direction = DirectionEnum.DOWN
                    elif alvo[1] == curr[1] - 1:
                        direction = DirectionEnum.LEFT
                    elif alvo[1] == curr[1] + 1:
                        direction = DirectionEnum.RIGHT
                        
                    if direction:
                        print(f"Sentiu mau cheiro! Atirando flecha na direção {direction.value}...")
                        self.env.shoot_arrow(direction)
                        
                        if self.on_step:
                            self.on_step(self) # Atualiza a tela após atirar a flecha
                        
                        # Pegar as percepções imediatamente após atirar
                        novas_percepcoes = self.env.get_percepts()
                        if PerceptEnum.SCREAM in novas_percepcoes:
                            print(f"Ouviu o grito ao atirar em {alvo}! Wumpus morto. Local marcado como seguro.")
                        else:
                            print(f"Sem grito. O Wumpus não estava em {alvo}. Local marcado como seguro.")
                        
                        # Atualizar para considerar o local seguro como o usuário pediu
                        self.no_wumpus.add(alvo)
                        self.no_abyss.add(alvo)
                        self.safe_cells.add(alvo)
                        
                        # Atualizar a variável percepts da rodada atual
                        percepts = novas_percepcoes
                
            # Inferência Lógica Básica:
            # Se não há brisa, os vizinhos não têm poço
            if PerceptEnum.BREEZE not in percepts:
                for viz in self._get_vizinhos(curr):
                    self.no_abyss.add(viz)
            
            # Se não há mau cheiro, os vizinhos não têm wumpus
            if PerceptEnum.STENCH not in percepts:
                for viz in self._get_vizinhos(curr):
                    self.no_wumpus.add(viz)
                    
            # Atualiza lista de células 100% seguras
            for r in range(self.env.lines):
                for c in range(self.env.cols):
                    if (r,c) in self.no_abyss and (r,c) in self.no_wumpus:
                        self.safe_cells.add((r,c))
                        
            # Células seguras que ainda não foram visitadas
            unvisited_safe = self.safe_cells - self.visited
            
            if unvisited_safe:
                # Procurar o caminho mais curto para uma célula segura não visitada
                menor_caminho = None
                for target in unvisited_safe:
                    caminho = self._find_path(curr, target, restrict_to=self.safe_cells)
                    if caminho:
                        if menor_caminho is None or len(caminho) < len(menor_caminho):
                            menor_caminho = caminho
                            
                if menor_caminho and len(menor_caminho) > 1:
                    next_pos = menor_caminho[1] # Dar apenas o próximo passo no menor caminho
                    self.move_to(next_pos)
                else:
                    print("Sem caminho seguro possível para células conhecidas.")
                    break
            else:
                print("Não há mais células 100% seguras. Arriscando em uma célula desconhecida para não parar!")
                unvisited_neighbors = [v for v in self._get_vizinhos(curr) if v not in self.visited]
                
                if unvisited_neighbors:
                    next_pos = random.choice(unvisited_neighbors)
                    print(f"Arriscando passo para vizinho {next_pos}")
                    self.move_to(next_pos)
                else:
                    # Tenta ir para qualquer célula não visitada do mapa (arriscado)
                    all_unvisited = [(r,c) for r in range(self.env.lines) for c in range(self.env.cols) if (r,c) not in self.visited]
                    if all_unvisited:
                        menor_caminho = None
                        for target in all_unvisited:
                            caminho = self._find_path(curr, target) # Sem restrição de segurança
                            if caminho:
                                if menor_caminho is None or len(caminho) < len(menor_caminho):
                                    menor_caminho = caminho
                        
                        if menor_caminho and len(menor_caminho) > 1:
                            next_pos = menor_caminho[1]
                            print(f"Navegando em risco em direção a {menor_caminho[-1]}")
                            self.move_to(next_pos)
                        else:
                            print("Nenhuma célula restante acessível.")
                            break
                    else:
                        print("Todas as células foram visitadas e o ouro não foi pego.")
                        break
                
        if not self.env.agent_alive:
            print(f"O agente morreu de forma trágica em {self.agent_pos_actual}! Score final: {self.env.score}")
            if self.on_step:
                self.on_step(self)
            return False
            
        print(f"Fim da execução. Score final: {self.env.score}")
        return False
