import numpy as np
from funcoes_coloracao import colorir_grafo_greedy,graph_to_png,animar_matriz_media_cumulativa,gerar_dicionarios
# há conflito
matriz_adjacencia_peixes = np.array([[0, 1, 1, 1, 1, 1, 1],
                                     [1, 0, 0, 0, 0, 1, 1],
                                     [1, 0, 0, 0, 0, 1, 0],
                                     [1, 0, 0, 0, 0, 1, 1],
                                     [1, 0, 0, 0, 0, 0, 0],
                                     [1, 1, 1, 1, 0, 0, 0],
                                     [1, 1, 0, 1, 0, 0, 0]])

if __name__ == "__main__":
    import pandas as pd
    num_simulacoes = 200
    dict_peixe = dict()
    graph_to_png(matriz_adjacencia_peixes,
                 'exercicios/grafo_peixes.png')
    # for peixe in range(matriz_adjacencia_peixes.shape[0]):
    #     print(peixe)
    #     lista = []
    #     for _ in range(num_simulacoes):
    #         lista.append(max(colorir_grafo_greedy(matriz_adjacencia_peixes, peixe)))
    #     dict_peixe[peixe] = np.mean(lista)
    
    num_simulacoes = 100

    matriz_adjacencia = matriz_adjacencia_peixes

    labels = list(range(matriz_adjacencia.shape[0]))

    dict_max, dict_min, dict_media, dict_media_acumulativa = gerar_dicionarios(matriz_adjacencia, num_simulacoes, labels)
    
    # a variação ocorre apenas 
    matriz_media_acumulativa = pd.DataFrame(dict_media_acumulativa).transpose().values
    
    animar_matriz_media_cumulativa(matriz_media_acumulativa,'exercicios/gif_peixes.gif',40,labels)
