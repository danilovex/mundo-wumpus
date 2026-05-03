import random
from enums import DirectionEnum, PerceptEnum

class WumpusWorldEnv:
    def __init__(self):
        self.score = 0

        self.lines = 8
        self.cols = 8
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.lines)] #create matriz 4x4 with 0 value
        
        self.agent_pos = (0,0)
        self.agent_alive = True
        
        self.arrow_pos = []

        self._insert_elements_on_world()

    def _insert_elements_on_world(self):
        self.wumpus_pos = (random.randint(0, self.lines-1), random.randint(0, self.cols-1))
        while self.wumpus_pos == (0, 0): # Wumpus não pode nascer na casa inicial
            self.wumpus_pos = (random.randint(0, self.lines-1), random.randint(0, self.cols-1))
            
        self.wumpus_alive = True
        self.abyss_pos = (random.randint(0, self.lines-1), random.randint(0, self.cols-1))    #random position for abyss
        self.gold_pos = self._get_position_gold()  #random position for gold

    def _get_position_gold(self): #get position of the gold should be different to abyss
        gold_pos = (random.randint(0, self.lines-1), random.randint(0, self.cols-1))
        while gold_pos == self.abyss_pos:
            gold_pos = (random.randint(0, self.lines-1), random.randint(0, self.cols-1))
        return gold_pos

    def _arrow_available(self):
        return len(self.arrow_pos) < 2

    def _is_valid_position(self, pos):
        return pos[0] >= 0 and pos[0] < self.lines and pos[1] >= 0 and pos[1] < self.cols

    def get_percepts(self):
        percepts = []
        neighbors_pos = self._get_neighbors()
        if self.wumpus_pos in neighbors_pos and self.wumpus_alive:
            percepts.append(PerceptEnum.STENCH) #Mau cheiro
        if self.abyss_pos in neighbors_pos:
            percepts.append(PerceptEnum.BREEZE) #Brisa
        if self.agent_pos == self.gold_pos:
            percepts.append(PerceptEnum.GLITTER) #Brilho
        if self.wumpus_pos in self.arrow_pos and self.wumpus_alive:
            self.wumpus_alive = False
            percepts.append(PerceptEnum.SCREAM)
        if not self._is_valid_position(self.agent_pos):
            percepts.append(PerceptEnum.BUMP)
        return percepts

    def _get_neighbors(self):
        pos = self.agent_pos
        neighbors = []
        if pos[0] > 0:
            neighbors.append((pos[0]-1, pos[1]))
        if pos[0] < self.lines-1:
            neighbors.append((pos[0]+1, pos[1]))
        if pos[1] > 0:
            neighbors.append((pos[0], pos[1]-1))
        if pos[1] < self.cols-1:
            neighbors.append((pos[0], pos[1]+1))
        return neighbors

    def move_agent(self, action):
        self.score -= 1
        pos = self.agent_pos
        if action == DirectionEnum.UP:
            self.agent_pos = (pos[0]-1, pos[1])
        elif action == DirectionEnum.DOWN:
            self.agent_pos = (pos[0]+1, pos[1])
        elif action == DirectionEnum.LEFT:
            self.agent_pos = (pos[0], pos[1]-1)
        elif action == DirectionEnum.RIGHT:
            self.agent_pos = (pos[0], pos[1]+1)

        # Verifica morte após o movimento
        if self.agent_pos == self.abyss_pos or (self.agent_pos == self.wumpus_pos and self.wumpus_alive):
            self.agent_alive = False
            self.score -= 1000 # Penalidade por morrer

    def shoot_arrow(self, direction):
        if self._arrow_available():
            self.score -= 10
            pos = self.agent_pos
            if direction == DirectionEnum.UP:
                self.arrow_pos.append((pos[0]-1, pos[1]))
            elif direction == DirectionEnum.DOWN:
                self.arrow_pos.append((pos[0]+1, pos[1]))
            elif direction == DirectionEnum.LEFT:
                self.arrow_pos.append((pos[0], pos[1]-1))
            elif direction == DirectionEnum.RIGHT:
                self.arrow_pos.append((pos[0], pos[1]+1))
            return True
        return False

    def grab_gold(self):
        self.score += 1000
        self.has_gold = True

    def climb_out(self):
        if self.agent_pos == (0,0) and self.has_gold:
            self.score += 1000
            return True
        else:
            return False
