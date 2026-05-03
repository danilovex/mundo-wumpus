import tkinter as tk
import threading
import time
import argparse
from wumpus_world_env import WumpusWorldEnv
from agent import WumpusAgent
from astar_search import astar_search
from bfs_search import bfs_search

class WumpusGUI:
    def __init__(self, master, env):
        self.master = master
        self.master.title("Mundo do Wumpus - Simulação Gráfica")
        self.env = env
        
        self.cell_size = 30
        self.width = env.cols * self.cell_size
        self.height = env.lines * self.cell_size
        
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="white")
        self.canvas.pack(padx=20, pady=20)
        
        # Botões de controle
        self.frame_botoes = tk.Frame(master)
        self.frame_botoes.pack(pady=10)
        
        self.status_label = tk.Label(self.frame_botoes, text="Aguardando início...", font=("Arial", 12))
        self.status_label.pack(side=tk.LEFT, padx=20)

    def desenhar_estado(self, agent=None):
        self.canvas.delete("all")
        
        # Desenha a grade e os elementos estáticos
        for r in range(self.env.lines):
            for c in range(self.env.cols):
                x0 = c * self.cell_size
                y0 = r * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                
                cor_fundo = "white"
                texto = ""
                cor_texto = "black"
                
                # Elementos no cenário
                if (r, c) == self.env.abyss_pos:
                    cor_fundo = "black"
                elif (r, c) == self.env.gold_pos and (not agent or not agent.has_gold):
                    cor_fundo = "gold"
                elif (r, c) == self.env.wumpus_pos:
                    if self.env.wumpus_alive:
                        cor_fundo = "red"
                        texto = "W"
                    else:
                        cor_fundo = "pink" # Wumpus morto
                        texto = "X"
                
                # Desenha a célula
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=cor_fundo, outline="lightgray")
                
                # Desenha o texto (Wumpus)
                if texto:
                    self.canvas.create_text(x0 + self.cell_size/2, y0 + self.cell_size/2, 
                                            text=texto, fill="white", font=("Arial", 12, "bold"))
                                            
                # Se a célula foi visitada, pinta o chão de cinza clarinho (se não tiver nada em cima)
                if agent and (r, c) in agent.visited and cor_fundo == "white":
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#e6e6e6", outline="lightgray")

        # Desenha as flechas atiradas
        for ar, ac in self.env.arrow_pos:
            x_center = ac * self.cell_size + self.cell_size/2
            y_center = ar * self.cell_size + self.cell_size/2
            self.canvas.create_oval(x_center-2, y_center-2, x_center+2, y_center+2, fill="orange")

        # Desenha o Agente
        ag_pos = self.env.agent_pos
        if agent:
            ag_pos = agent.agent_pos_actual
            
        ax_center = ag_pos[1] * self.cell_size + self.cell_size/2
        ay_center = ag_pos[0] * self.cell_size + self.cell_size/2
        
        # Agente é um círculo azul (ou preto se morrer)
        raio = self.cell_size * 0.35
        cor_agente = "blue" if self.env.agent_alive else "black"
        self.canvas.create_oval(ax_center-raio, ay_center-raio, ax_center+raio, ay_center+raio, fill=cor_agente)
        
        # Desenha um X sobre o agente se ele morrer
        if not self.env.agent_alive:
            self.canvas.create_line(ax_center-raio, ay_center-raio, ax_center+raio, ay_center+raio, fill="white", width=2)
            self.canvas.create_line(ax_center-raio, ay_center+raio, ax_center+raio, ay_center-raio, fill="white", width=2)
            
        self.master.update()

def rodar_simulacao(gui, env, search_strategy, velocidade):
    # Callback chamado a cada passo do agente
    def atualizar_tela(agent):
        gui.status_label.config(text=f"Agente em {agent.agent_pos_actual} | Score: {env.score}")
        gui.desenhar_estado(agent)
        time.sleep(velocidade)

    # Inicia o agente passando a função de atualizar tela
    agent = WumpusAgent(env=env, search_strategy=search_strategy, on_step=atualizar_tela)
    
    gui.status_label.config(text="Explorando a caverna...")
    
    # Inicia o laço pesado do agente
    agent.resolve_problem()
    
    gui.status_label.config(text=f"Fim da Execução! Score: {env.score}")

def main():
    parser = argparse.ArgumentParser(description="Mundo do Wumpus - GUI")
    parser.add_argument("--search", type=str, choices=["bfs", "astar"], default="astar", help="Algoritmo de busca")
    parser.add_argument("--speed", type=float, default=0.5, help="Tempo em segundos entre cada passo")
    args = parser.parse_args()

    search_strategy = astar_search if args.search == "astar" else bfs_search

    # Cria a janela do Tkinter
    root = tk.Tk()
    
    # Prepara o ambiente
    print("Gerando Mundo do Wumpus...")
    env = WumpusWorldEnv()
    
    # Cria a interface passando a janela e o ambiente inicial
    gui = WumpusGUI(root, env)
    gui.desenhar_estado() # Desenha o estado inicial
    
    # Roda a inteligência do agente em uma Thread separada para não congelar a janela
    thread = threading.Thread(target=rodar_simulacao, args=(gui, env, search_strategy, args.speed))
    thread.daemon = True # Faz a thread morrer quando a janela for fechada
    thread.start()
    
    # Inicia o loop de renderização da janela
    root.mainloop()

if __name__ == "__main__":
    main()
