import numpy as np
import pandas as pd
from funcoes_coloracao import *
import networkx as nx
import matplotlib
# há conflito

labels = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
qtd = labels.shape[0]
matriz_adjacencia_cachorros = np.zeros(shape=(qtd, qtd), dtype=int)
dict_cachorro_ind = dict([(letra, indice)
                          for indice, letra in enumerate(labels)])
dict_ind_cachorro = dict([(indice, letra)
                          for indice, letra in enumerate(labels)])
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
    matriz_adjacencia_cachorros, index=labels, columns=labels)


if __name__ == "__main__":
    import random
    import os
    nome_exercicio = 'Cachorros'
    caminho = 'exercicios/'+nome_exercicio

    os.makedirs(caminho, exist_ok=True)
    matriz_adjacencia = matriz_adjacencia_cachorros.values

    observadores = simular(matriz_adjacencia, colorir_grafo, simulacoes_por_no = 1000)
    obs_max_cores, obs_min_cores = get_max_min_cores(observadores)
     
     
    if obs_max_cores.num_cores == obs_min_cores.num_cores:
        sequencia_coloracao_para_gif(matriz_adjacencia, 
                                    obs_min_cores, 
                                    caminho+'/animacao_coloracao_'+ nome_exercicio, 
                                    lista_labels=labels, 
                                    quadros_por_etapa = 2, 
                                    segundos=5)
        coloracao_para_png(matriz_adjacencia,
                           obs_max_cores.sequencia_vetor_cores[-1],
                           caminho+'/grafo_'+nome_exercicio,
                           labels
                           )
    else:  
        sequencia_coloracao_para_gif(matriz_adjacencia, 
                                    obs_min_cores, 
                                    caminho+f'/animacao_coloracao_{nome_exercicio}_min_cores', 
                                    lista_labels=labels, 
                                    quadros_por_etapa = 2, 
                                    segundos=5)
        coloracao_para_png(matriz_adjacencia,
                           obs_min_cores.sequencia_vetor_cores[-1],
                           caminho+'/grafo_min_cores_'+nome_exercicio,
                           labels
                           )

        sequencia_coloracao_para_gif(matriz_adjacencia, 
                                    obs_max_cores, 
                                     caminho+f'/animacao_coloracao_{nome_exercicio}_max_cores', 
                                    lista_labels=labels, 
                                    quadros_por_etapa = 2, 
                                    segundos=5)
        coloracao_para_png(matriz_adjacencia,
                           obs_max_cores.sequencia_vetor_cores[-1],
                           caminho+'/grafo_max_cores_'+nome_exercicio,
                           labels
                           )

    graph_to_gif(matriz_adjacencia, caminho+'/combinacoes_cores_grafo_'+nome_exercicio,
                 num_quadros=100, tempo_segundos=5, lista_labels=labels)
    segundos = 5

    matriz_simulacoes = get_matriz_simulacao(len(labels), observadores)[:,:200]

    dict_matrizes = {'min': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.min),
                     'max': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.max),
                     'media': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.mean)}

    for chave, matriz in dict_matrizes.items():
        animar_matriz_simulacoes(
            matriz, caminho+f'/{chave}_{nome_exercicio}', segundos, labels, matriz_simulacoes)