import numpy as np
import pandas as pd
from funcoes_coloracao import colorir_grafo_greedy, graph_to_png, animar_matriz_simulacoes, gerar_simulacoes, graph_to_mp4,aplicar_funcao_matriz_simulacoes
# há conflito

ind_containers = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
qtd = ind_containers.shape[0]
matriz_adjacencia_containers = np.zeros(shape=(qtd, qtd), dtype=int)
dict_ind_containers = dict([(letra, indice)
                            for indice, letra in enumerate(ind_containers)])
dict_adjacencia = {'A': ['B', 'C', 'G', 'F', 'D'],
                   'B': ["A", "C", "G"],
                   'C': ["A", "B", "G"],
                   "G": ["A", "B", "C"],
                   'E': ['D', 'F']}

for c1, lista_c2 in dict_adjacencia.items():
    i = dict_ind_containers[c1]
    lista_j = [dict_ind_containers[c2] for c2 in lista_c2]
    for j in lista_j:
        matriz_adjacencia_containers[i, j] = 1
        matriz_adjacencia_containers[j, i] = 1

matriz_adjacencia_containers = pd.DataFrame(
    matriz_adjacencia_containers, index=ind_containers, columns=ind_containers)

if __name__ == "__main__":
    import random
    import os
    os.makedirs('exercicios/Containers',exist_ok=True)
    random.seed()
    num_simulacoes = 20
    graph_to_png(matriz_adjacencia_containers.values,
                 'exercicios/Containers/grafo_containers.png',
                 lista_labels=ind_containers)

    num_simulacoes = 200
    matriz_adjacencia = matriz_adjacencia_containers.values
    graph_to_mp4(matriz_adjacencia, 'exercicios/Containers/animacao_grafo_containers',num_quadros=100,tempo_segundos=5, lista_labels=ind_containers)
    

    segundos=5
    matriz_simulacoes = gerar_simulacoes(matriz_adjacencia, num_simulacoes, ind_containers,colorir_grafo_greedy)
    
    dict_matrizes = {'min': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.min),
                     'max': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.max),
                     'media': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.mean)}
    
    for chave, matriz in dict_matrizes.items():
        animar_matriz_simulacoes(matriz,f'exercicios/Containers/{chave}_containers',segundos,ind_containers,matriz_simulacoes)
