import numpy as np
import pandas as pd
from funcoes_coloracao import *

estados = np.array(['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT',
                    'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'])
dict_vizinhanca = {'AC': ["AM", "RO"],
                   'AL': ['PE', "SE", "BA"],
                   'AM': ['AC', "RR", "RO", "MT", "PA"],
                   "AP": ["PA"],
                   "BA": ["SE", "AL", "PE", "PI", "TO", "GO", "MG", "ES"],
                   "CE": ["RN", "PB", "PE", "PI"],
                   "DF": ["GO"],
                   "ES": ["MG", "RJ", "BA"],
                   "GO": ["DF", "TO", "BA", "MG", "MS", "MT"],
                   "MA": ["PI", "TO", "PA"],
                   "MG": ["ES", "RJ", "SP", "GO", "BA", "MS", "DF"],
                   "MS": ["PR", "SP", "MG", "GO", "MT"],
                   "MT": ["RO", "AM", "PA", "TO", "GO", "MS"],
                   "PA": ["AP", "MA", "TO", "MT", "AM", "RR"],
                   "PB": ["CE", "RN", "PE"],
                   "PE": ["PB", "CE", "PI", "AL", "BA"],
                   "PI": ["CE", "PE", "BA", "TO", "MA"],
                   "PR": ["SP", "SC", "MS"],
                   "RJ": ["MG", "ES", "SP"],
                   "RN": ["PB", "CE"],
                   "RO": ["AC", "AM", "MT"],
                   "RR": ["AM", "PA"],
                   "RS": ["SC"],
                   "SC": ["PR", "RS"],
                   "SE": ["BA", "AL"],
                   "SP": ["MG", "RJ", "PR", "MS"],
                   "TO": ["MA", "PI", "BA", "GO", "MT", "PA"]}
matriz_adjacencia = []
args_pandas = {'index': estados, 'columns': estados}
def to_pandas(x): return pd.DataFrame(x, **args_pandas)


for chave, lista in dict_vizinhanca.items():
    linha = [int(sigla in lista) for sigla in estados]
    matriz_adjacencia.append(linha)

matriz_adjacencia = to_pandas(matriz_adjacencia)

# print(matriz_adjacencia)
dict_graus = dict([(chave, len(lista))
                   for chave, lista in dict_vizinhanca.items()])

d = np.diag(list(dict_graus.values()))
lista_qtd_vizinhos = list(dict_graus.values())
# print(lista_qtd_vizinhos == np.max(lista_qtd_vizinhos))
estado_com_menos_vizinhos = estados[lista_qtd_vizinhos == np.min(
    lista_qtd_vizinhos)]
estado_com_mais_vizinhos = estados[lista_qtd_vizinhos == np.max(
    lista_qtd_vizinhos)]
m_aux = matriz_adjacencia
p = 1

if __name__ == "__main__":
    import random
    random.seed()
    import multiprocessing as mp
    from multiprocessing import Pool
    import os
    nome_exercicio = 'Brasil'
    caminho = 'exercicios/'+nome_exercicio
    os.makedirs(caminho + '/resultado_por_estado',exist_ok=True)
    matriz_adjacencia = matriz_adjacencia.values
    labels = estados

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
                           )

    graph_to_gif(matriz_adjacencia, caminho+'/combinacoes_cores_grafo_'+nome_exercicio,
                 num_quadros=100, tempo_segundos=5, lista_labels=labels)

    segundos = 5

    matriz_simulacoes = get_matriz_simulacao(len(labels), observadores)[:,:200]

    dict_matrizes = {'min': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.min),
                     'max': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.max),
                     'media': aplicar_funcao_matriz_simulacoes(matriz_simulacoes, np.mean)}

    args = []
    for chave, matriz in dict_matrizes.items():
        for i, estado in enumerate(labels):
            arg = (matriz[i, :].reshape(1, -1),
                   caminho + f'/resultado_por_estado/{chave}_{estado}',
                   segundos,
                   [estado],
                   matriz_simulacoes[i, :].reshape(1, -1))
            args.append(arg)
        args.append((matriz,
                 caminho + f'/{chave}_'+nome_exercicio,
                 segundos,
                 labels,
                 matriz_simulacoes))
    
    n_cores=mp.cpu_count()
    splitted_args = np.split(np.array(args),len(args)//n_cores)
    for conjunto_args in splitted_args:

        pool=Pool(n_cores)

        pool.starmap_async(animar_matriz_simulacoes, conjunto_args.tolist())

        pool.close()
        pool.join()
