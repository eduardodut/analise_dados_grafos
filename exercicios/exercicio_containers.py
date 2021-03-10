import numpy as np
import pandas as pd
from funcoes_coloracao import colorir_grafo_greedy,graph_to_png,animar_matriz_media_cumulativa,gerar_dicionarios
# há conflito

ind_containers = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
qtd = ind_containers.shape[0]
matriz_adjacencia_containers = np.zeros(shape=(qtd, qtd), dtype=int)
dict_ind_containers = dict([(letra, indice)
                            for indice, letra in enumerate(ind_containers)])
dict_adjacencia = {'A': ['B', 'C', 'G', 'F', 'D'],
                   'E': ['D', 'F']}

for c1, lista_c2 in dict_adjacencia.items():
    # print(c1, lista_c2)
    i = dict_ind_containers[c1]
    lista_j = [dict_ind_containers[c2] for c2 in lista_c2]
    for j in lista_j:
        matriz_adjacencia_containers[i, j] = 1

matriz_adjacencia_containers += matriz_adjacencia_containers.T
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

    # for i, container in enumerate(ind_containers):
    #     lista = []
    #     for _ in range(num_simulacoes):
    #         lista.append(max(colorir_grafo_greedy(
    #             matriz_adjacencia_containers.values, i)))
    #     dict_container[container] = np.mean(lista)

    # import pprint
    # pprint.pprint(dict_container)
    num_simulacoes =  200
    
    matriz_adjacencia = matriz_adjacencia_containers.values

    dict_max, dict_min, dict_media, dict_media_acumulativa = gerar_dicionarios(matriz_adjacencia, num_simulacoes, ind_containers)
    
    matriz_media_acumulativa = pd.DataFrame(dict_media_acumulativa).transpose().values
    
    animar_matriz_media_cumulativa(matriz_media_acumulativa[:,:200],'exercicios/gif_containers.gif',40,ind_containers)

    # animar_matriz_media_cumulativa(matriz_media_acumulativa[0,:200].reshape(1,-1),'exercicios/gif_AC.gif',40,['AC'])