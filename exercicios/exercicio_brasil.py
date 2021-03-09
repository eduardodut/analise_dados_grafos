import numpy as np
import pandas as pd
import random
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
args_pandas = {'index':estados, 'columns':estados}
to_pandas = lambda x: pd.DataFrame(x,**args_pandas)

for chave,lista in dict_vizinhanca.items():
    linha = [int(sigla in lista) for sigla in estados]
    matriz_adjacencia.append(linha)

matriz_adjacencia = to_pandas(matriz_adjacencia)

# print(matriz_adjacencia)
dict_graus = dict([(chave,len(lista)) for chave,lista in dict_vizinhanca.items()])

d = np.diag(list(dict_graus.values()))
lista_qtd_vizinhos = list(dict_graus.values())
# print(lista_qtd_vizinhos == np.max(lista_qtd_vizinhos))
estado_com_menos_vizinhos = estados[lista_qtd_vizinhos == np.min(lista_qtd_vizinhos)]
estado_com_mais_vizinhos = estados[lista_qtd_vizinhos == np.max(lista_qtd_vizinhos)]
m_aux = matriz_adjacencia
p = 1
# while not all([m_aux.loc['BA',estado] > 0 for estado in estado_com_menos_vizinhos]):
#     p+=1
#     m_aux = to_pandas(np.linalg.matrix_power(matriz_adjacencia,p))
# print(lista_cores)
 

# print(dict_cores_estado)

# def colorir(estado):
#     vizinhos = getVizinhos(estado)
#     cores_vizinhos = [dict_cores_estado[es] for es in vizinhos if dict_cores_estado[es] > 0]
#     cor_selecionada = 0
#     for cor in lista_cores:
#         if cor not in cores_vizinhos:
#             cor_selecionada = cor
#             break
#     dict_cores_estado[estado] = cor_selecionada
    
#     vizinhos = [viz for viz in vizinhos if dict_cores_estado[viz] == 0]
    
#     if len(vizinhos) > 0:
#         random.shuffle(vizinhos)
#         for viz in vizinhos:
#             colorir(viz)
    
# dict_colorir_estado = {}  
# for i in range(1):
#     for estado in estados:
#         dict_cores_estado = dict(zip(estados,[0 for _ in range(len(estados))]))
#         colorir(estado)
#         dict_colorir_estado[estado] = max(dict_cores_estado.values())
# print(dict_colorir_estado)
# print(y)
# print(m_aux)
def colorir_grafo(matriz_adjacencia, ponto_partida):
    lista_cores = []
    nos = matriz_adjacencia.index.values
    dict_cores_no = dict(zip(nos,[0 for _ in range(len(nos))]))
    def colorir(ponto_partida):
        
        def getVizinhos(node):
            adjacencia = matriz_adjacencia.loc[node] 
            return adjacencia[adjacencia>0].index.values
        vizinhos = getVizinhos(ponto_partida)
        cores_vizinhos = [dict_cores_no[viz] for viz in vizinhos if dict_cores_no[viz] > 0]
        cor_selecionada = 0
        for cor in lista_cores:
            if cor not in cores_vizinhos:
                cor_selecionada = cor
                break
        if cor_selecionada == 0:
            if len(lista_cores) > 0:
                lista_cores.append(max(lista_cores)+1)
            else:
                lista_cores.append(1)
            cor_selecionada = lista_cores[-1]
        
        dict_cores_no[ponto_partida] = cor_selecionada
    
        vizinhos = [viz for viz in vizinhos if dict_cores_no[viz] == 0]
        
        if len(vizinhos) > 0:
            random.shuffle(vizinhos)
            for viz in vizinhos:
                colorir(viz)
    colorir(ponto_partida)
    return lista_cores[-1]
dict_no = dict()
for estado in estados:
    lista = []
    print(estado)
    for i in range(13):
        lista.append(colorir_grafo(matriz_adjacencia, estado))
    dict_no[estado] = np.mean(lista)

import pprint
pprint.pprint(dict_no)