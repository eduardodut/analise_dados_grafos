import numpy as np
from funcoes_coloracao import colorir_grafo_greedy, graph_to_png, animar_matriz_simulacoes, gerar_simulacoes, graph_to_mp4,aplicar_funcao_matriz_simulacoes
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
    import os
    os.makedirs('exercicios/Peixes',exist_ok=True)
    matriz_adjacencia = matriz_adjacencia_peixes
    labels = list(range(matriz_adjacencia.shape[0]))
    graph_to_png(matriz_adjacencia,
                 'exercicios/Peixes/grafo_peixes.png',ponto_partida=6)
    graph_to_mp4(matriz_adjacencia, 'exercicios/Peixes/animacao_grafo_peixes',num_quadros=100,tempo_segundos=5, lista_labels=labels)
    
    num_simulacoes = 200


    segundos=5
    matriz_simulacoes = gerar_simulacoes(matriz_adjacencia, num_simulacoes, labels,colorir_grafo_greedy)
    
    dict_matrizes = {'min': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.min),
                     'max': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.max),
                     'media': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.mean)}
    
    for chave, matriz in dict_matrizes.items():
        animar_matriz_simulacoes(matriz,f'exercicios/Peixes/{chave}_peixes',segundos,labels,matriz_simulacoes)
