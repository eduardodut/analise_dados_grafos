import numpy as np
import pandas as pd
from funcoes_coloracao import colorir_grafo_greedy, graph_to_png, animar_matriz_media_cumulativa, gerar_dicionarios,graph_to_mp4
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

print(matriz_adjacencia_containers)
if __name__ == "__main__":
    import random
    random.seed()
    num_simulacoes = 20
    dict_container = dict()
    graph_to_png(matriz_adjacencia_containers.values,
                 'exercicios/grafo_containers.png',
                 lista_labels=ind_containers)

    num_simulacoes = 200
    matriz_adjacencia = matriz_adjacencia_containers.values
    graph_to_mp4(matriz_adjacencia, 'exercicios/grafo_containers',num_quadros=100,tempo_segundos=5, lista_labels=ind_containers)
    matriz_simulacoes, matriz_media_acumulativa = gerar_dicionarios(
        matriz_adjacencia, num_simulacoes, ind_containers)
    
    animar_matriz_media_cumulativa(
        matriz_media_acumulativa, 'exercicios/containers.gif', 5, ind_containers, matriz_simulacoes)

    # animar_matriz_media_cumulativa(matriz_media_acumulativa[0,:200].reshape(1,-1),'exercicios/AC.gif',40,['AC'])
