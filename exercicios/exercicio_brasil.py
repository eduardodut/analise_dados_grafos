import numpy as np
import pandas as pd
from funcoes_coloracao import colorir_grafo_greedy,graph_to_png,animar_matriz_media_cumulativa,gerar_dicionarios

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

if __name__ == "__main__":
    import random
    random.seed()
    graph_to_png(matriz_adjacencia.values,
                 'exercicios/grafo_Brasil.png',
                  estados)
    num_simulacoes =  200

    dict_max, dict_min, dict_media, dict_media_acumulativa = gerar_dicionarios(matriz_adjacencia.values, num_simulacoes, estados)
    
    matriz_media_acumulativa = pd.DataFrame(dict_media_acumulativa).transpose().values
    
    animar_matriz_media_cumulativa(matriz_media_acumulativa[:,:200],'exercicios/gif_Brasil.gif',40,estados)

    animar_matriz_media_cumulativa(matriz_media_acumulativa[0,:200].reshape(1,-1),'exercicios/gif_AC.gif',40,['AC'])