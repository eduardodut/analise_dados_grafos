import numpy as np
from funcoes_coloracao import *
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
    import numpy as np
    import os
    nome_exercicio = 'Peixes'
    caminho = 'exercicios/'+nome_exercicio

    os.makedirs(caminho, exist_ok=True)
    matriz_adjacencia = matriz_adjacencia_peixes
    labels = ['A','B','C','D','E','F','G']

    observadores = simular(matriz_adjacencia, colorir_grafo, simulacoes_por_no = 1000)
    obs_max_cores, obs_min_cores = get_max_min_cores(observadores)
    max_cores = max(obs_max_cores.sequencia_vetor_cores[-1])
    min_cores = max(obs_min_cores.sequencia_vetor_cores[-1])
    if max_cores == min_cores:
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
