import numpy as np
import pandas as pd
from funcoes_coloracao import colorir_grafo_greedy, graph_to_png, animar_matriz_simulacoes, gerar_simulacoes, graph_to_mp4,aplicar_funcao_matriz_simulacoes
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
    import os
    os.makedirs('exercicios/Cachorros',exist_ok=True)
    random.seed()

    graph_to_png(matriz_adjacencia_cachorros.values,
                 'exercicios/Cachorros/grafo_cachorro.png',
                 lista_labels=ind_cachorros)

    num_simulacoes = 200
    
    matriz_adjacencia = matriz_adjacencia_cachorros.values
    
    graph_to_mp4(matriz_adjacencia, 'exercicios/Cachorros/animacao_grafo_cachorros',num_quadros=100,tempo_segundos=5, lista_labels=ind_cachorros)

    

    segundos=5
    matriz_simulacoes = gerar_simulacoes(matriz_adjacencia, num_simulacoes, ind_cachorros,colorir_grafo_greedy)
    
    dict_matrizes = {'min': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.min),
                     'max': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.max),
                     'media': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.mean)}
    
    for chave, matriz in dict_matrizes.items():
        animar_matriz_simulacoes(matriz,f'exercicios/Cachorros/{chave}_cachorros',segundos,ind_cachorros,matriz_simulacoes)