import numpy as np
import pandas as pd
from funcoes_coloracao import colorir_grafo_greedy, graph_to_png, animar_matriz_media_cumulativa, gerar_dicionarios,graph_to_mp4

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
    graph_to_png(matriz_adjacencia.values,
                 'exercicios/grafo_Brasil.png',
                 estados)
    graph_to_mp4(matriz_adjacencia.values, 'exercicios/grafo_Brasil',num_quadros=100,tempo_segundos=5, lista_labels=estados)
    num_simulacoes = 150

    matriz_simulacoes, matriz_media_acumulativa = gerar_dicionarios(
        matriz_adjacencia.values, num_simulacoes, estados)

    segundos = 5
    # animar_matriz_media_cumulativa(
    #     matriz_media_acumulativa[:, :200], 'exercicios/Brasil.gif', 40, estados, maximo, minimo)
    args = []

    args = [(matriz_media_acumulativa[i, :].reshape(1, -1),
             f'exercicios/gifs_por_estado/{estado}',
             segundos,
             [estado],
             matriz_simulacoes[i, :].reshape(1, -1)) for i, estado in enumerate(estados)]
    args.append((matriz_media_acumulativa,
                 'exercicios/Brasil',
                 segundos,
                 estados,
                 matriz_simulacoes))
    # animar_matriz_media_cumulativa(matriz_media_acumulativa, 
    #                                'exercicios/Brasil', 
    #                                 segundos, 
    #                                 estados, 
    #                                 matriz_simulacoes)
    # estado = 'TO'
    # i = np.where(estados == estado)
    # animar_matriz_media_cumulativa(matriz_media_acumulativa[i, :].reshape(1, -1),
    #                               f'exercicios/gifs_por_estado/{estado}',
    #                               segundos,
    #                               [estados[i]],
    #                               matriz_simulacoes[i, :].reshape(1, -1))
    for arg in args:
        a0,a1,a2,a3,a4 = arg
        animar_matriz_media_cumulativa(a0,a1,a2,a3,a4)
    # n_cores=mp.cpu_count()

    # pool=Pool(n_cores)
     
    # pool.starmap_async(animar_matriz_media_cumulativa, args[0:12])

    # pool.close()
    # pool.join()

    # pool=Pool(n_cores)
     
    # pool.starmap_async(animar_matriz_media_cumulativa, args[12:25])

    # pool.close()
    # pool.join()

    # pool=Pool(n_cores)
     
    # pool.starmap_async(animar_matriz_media_cumulativa, args[25:])

    # pool.close()
    # pool.join()

   