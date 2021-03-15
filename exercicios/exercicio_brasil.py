import numpy as np
import pandas as pd
from funcoes_coloracao import *

estados = np.array(['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT',
                    'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'])
array_coords = np.array([[76,  265],  # 'AC'
                         [622, 268],  # 'AL'
                         [150, 159],  # 'AM'
                         [363,  65],  # 'AP'
                         [524, 302],  # 'BA'
                         [565, 180],  # 'CE'
                         [419, 360],  # 'DF'
                         [539, 423],  # 'ES'
                         [383, 382],  # 'GO'
                         [473, 189],  # 'MA'
                         [480, 413],  # 'MG'
                         [317, 442],  # 'MS'
                         [305, 315],  # 'MT'
                         [343, 184],  # 'PA'
                         [631, 220],  # 'PB'
                         [626, 243],  # 'PE'
                         [507, 225],  # 'PI'
                         [362, 513],  # 'PR'
                         [500, 481],  # 'RJ'
                         [626, 194],  # 'RN'
                         [183, 279],  # 'RO'
                         [203,  61],  # 'RR'
                         [340, 602],  # 'RS'
                         [386, 556],  # 'SC'
                         [602, 290],  # 'SE'
                         [406, 471],  # 'SP'
                         [416, 267]])  # 'TO'

max_x = array_coords[:, 0].max()//2
max_y = array_coords[:, 1].max()//2

array_coords_exp = np.ones(shape=(array_coords.shape[0], array_coords.shape[1]+1), dtype=int)
array_coords_exp[:, :-1] = array_coords

matriz_translacao_1 = np.array([[1, 0, -max_x],
                                [0, 1, -max_y],
                                [0, 0, 1]])

matriz_reflexao = np.array([[1, 0, 0],
                            [0, -1, 0],
                            [0, 0, 1]])

matriz_translacao_2 = np.array([[1, 0, max_x],
                                [0, 1, max_y],
                                [0, 0, 1]])

array_coords = matriz_translacao_2 @ matriz_reflexao @ matriz_translacao_1 @ array_coords_exp.T

dict_coords = dict([(ind, t[:-1]) for ind, t in enumerate(array_coords.T)])

dict_vizinhanca = {'AC': ["AM", "RO"],
                   'AL': ['PE', "SE", "BA"],
                   'AM': ['AC', "RR", "RO", "MT", "PA"],
                   "AP": ["PA"],
                   "BA": ["SE", "AL", "PE", "PI", "TO", "GO", "MG", "ES"],
                   "CE": ["RN", "PB", "PE", "PI"],
                   "DF": ["GO", "MG"],
                   "ES": ["MG", "RJ", "BA"],
                   "GO": ["DF", "TO", "BA", "MG", "MS", "MT"],
                   "MA": ["PI", "TO", "PA"],
                   "MG": ["ES", "RJ", "SP", "GO", "DF", "BA", "MS", "DF"],
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
dict_graus = dict([(chave, len(lista)) for chave, lista in dict_vizinhanca.items()])

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
    os.makedirs(caminho + '/resultado_por_estado', exist_ok=True)
    matriz_adjacencia = matriz_adjacencia.values
    labels = estados
    # dict_coords={}
    observadores = simular(
        matriz_adjacencia, colorir_grafo, simulacoes_por_no=1000)
    obs_max_cores, obs_min_cores = get_max_min_cores(observadores)

    if obs_max_cores.num_cores == obs_min_cores.num_cores:
        sequencia_coloracao_para_gif(matriz_adjacencia,
                                     obs_min_cores,
                                     caminho+'/animacao_coloracao_' + nome_exercicio,
                                     lista_labels=labels,
                                     quadros_por_etapa=2,
                                     segundos=5,
                                     pos=dict_coords)
        coloracao_para_png(matriz_adjacencia,
                           obs_min_cores.sequencia_vetor_cores[-1],
                           caminho+'/grafo_'+nome_exercicio,
                           labels,
                           pos=dict_coords)
    else:
        sequencia_coloracao_para_gif(matriz_adjacencia,
                                     obs_min_cores,
                                     caminho +
                                     f'/animacao_coloracao_{nome_exercicio}_min_cores',
                                     lista_labels=labels,
                                     quadros_por_etapa=2,
                                     segundos=5,
                                     pos=dict_coords)
        coloracao_para_png(matriz_adjacencia,
                           obs_min_cores.sequencia_vetor_cores[-1],
                           caminho+'/grafo_min_cores_'+nome_exercicio,
                           labels,
                           pos=dict_coords)

        sequencia_coloracao_para_gif(matriz_adjacencia,
                                     obs_max_cores,
                                     caminho +
                                     f'/animacao_coloracao_{nome_exercicio}_max_cores',
                                     lista_labels=labels,
                                     quadros_por_etapa=2,
                                     segundos=5,
                                     pos=dict_coords)
        coloracao_para_png(matriz_adjacencia,
                           obs_max_cores.sequencia_vetor_cores[-1],
                           caminho+'/grafo_max_cores_'+nome_exercicio,
                           labels,
                           pos=dict_coords
                           )

    graph_to_gif(matriz_adjacencia, caminho+'/combinacoes_cores_grafo_'+nome_exercicio,
                 num_quadros=100, tempo_segundos=5, lista_labels=labels,
                 pos=dict_coords)

    segundos = 5

    matriz_simulacoes = get_matriz_simulacao(
        len(labels), observadores)[:, :200]

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

    n_cores = mp.cpu_count()
    splitted_args = np.split(np.array(args), len(args)//n_cores)
    for conjunto_args in splitted_args:

        pool = Pool(n_cores)

        pool.starmap_async(animar_matriz_simulacoes, conjunto_args.tolist())

        pool.close()
        pool.join()
