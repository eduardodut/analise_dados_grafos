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
    dict_peixe = dict()
    graph_to_png(matriz_adjacencia_peixes,
                 'exercicios/grafo_peixes.png',ponto_partida=6)
    
    num_simulacoes = 200


    matriz_adjacencia = matriz_adjacencia_peixes

    labels = list(range(matriz_adjacencia.shape[0]))

    matriz_simulacoes, matriz_media_acumulativa = gerar_dicionarios(matriz_adjacencia, num_simulacoes, labels)
    
    
    animar_matriz_media_cumulativa(matriz_media_acumulativa,'exercicios/peixes.gif',5,labels,matriz_simulacoes)
