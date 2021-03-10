import numpy as np
import pandas as pd
from funcoes_coloracao import colorir_grafo_greedy,graph_to_png,animar_matriz_media_cumulativa,gerar_dicionarios
import networkx as nx
import matplotlib
# há conflito

ind_cachorros = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
qtd = ind_cachorros.shape[0]
matriz_adjacencia_cachorros = np.zeros(shape=(qtd, qtd), dtype=int)
dict_cachorro_ind = dict([(letra, indice)
                          for indice, letra in enumerate(ind_cachorros)])
dict_ind_cachorro = dict([(indice, letra)
                          for indice, letra in enumerate(ind_cachorros)])
dict_adjacencia = {'A': ['C', 'D', 'E'],
                   'B': ['F'],
                   'E': ['D', 'F']}


for c1, lista_c2 in dict_adjacencia.items():
    # print(c1, lista_c2)
    i = dict_cachorro_ind[c1]
    lista_j = [dict_cachorro_ind[c2] for c2 in lista_c2]
    for j in lista_j:
        matriz_adjacencia_cachorros[i, j] = 1


matriz_adjacencia_cachorros += matriz_adjacencia_cachorros.T

matriz_adjacencia_cachorros = pd.DataFrame(
    matriz_adjacencia_cachorros, index=ind_cachorros, columns=ind_cachorros)


if __name__ == "__main__":
    import random
    random.seed()

    graph_to_png(matriz_adjacencia_cachorros.values,
                 'exercicios/grafo_cachorro.png',
                 lista_labels=ind_cachorros)

    num_simulacoes = 200

    matriz_adjacencia = matriz_adjacencia_cachorros.values
    
    matriz_simulacoes, matriz_media_acumulativa = gerar_dicionarios(matriz_adjacencia, num_simulacoes, ind_cachorros)

    maximo = np.max(list(dict_max.values()))
    
    minimo = np.min(list(dict_min.values()))

    matriz_media_acumulativa = pd.DataFrame(dict_media_acumulativa).transpose().values
    
    animar_matriz_media_cumulativa(matriz_media_acumulativa,'exercicios/cachorros.gif',5,ind_cachorros,maximo,minimo)