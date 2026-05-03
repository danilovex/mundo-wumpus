import time
import copy
from wumpus_world_env import WumpusWorldEnv
from agent import WumpusAgent
from bfs_search import bfs_search
from astar_search import astar_search

def run_agent(name, search_strategy, env):
    print(f"\n{'='*50}")
    print(f"Executando algoritmo: {name}")
    print(f"{'='*50}")
    
    agent = WumpusAgent(env=env, search_strategy=search_strategy)
    
    start_time = time.time()
    agent.resolve_problem()
    end_time = time.time()
    
    execution_time = end_time - start_time
    score = env.score
    
    return score, execution_time

def main():
    print("Gerando Mundo do Wumpus (Layout Base)...")
    # Cria o ambiente base
    base_env = WumpusWorldEnv()
    
    # Cria cópias idênticas para garantir um teste justo
    env_bfs = copy.deepcopy(base_env)
    env_astar = copy.deepcopy(base_env)
    
    # Executa BFS
    score_bfs, time_bfs = run_agent("BFS (Busca em Largura)", bfs_search, env_bfs)
    
    # Executa A*
    score_astar, time_astar = run_agent("A* (A-Star)", astar_search, env_astar)
    
    # Mostra Comparação Final
    print(f"\n{'='*50}")
    print("COMPARAÇÃO DE RESULTADOS")
    print(f"{'='*50}")
    print(f"{'Algoritmo':<20} | {'Score':<10} | {'Tempo (s)':<15}")
    print("-" * 50)
    print(f"{'BFS':<20} | {score_bfs:<10} | {time_bfs:.6f}")
    print(f"{'A*':<20} | {score_astar:<10} | {time_astar:.6f}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()

