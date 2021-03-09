import numpy as np
import pandas as pd
from funcoes_coloracao import colorir_grafo_greedy
# há conflito

ind_cachorros = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
qtd = ind_cachorros.shape[0]
matriz_adjacencia_cachorros = np.zeros(shape=(qtd, qtd), dtype=int)
dict_ind_cachorros = dict([(letra,indice) for indice,letra in enumerate(ind_cachorros)])
dict_adjacencia = {'A': ['C', 'D', 'E'],
                   'B': ['F'],
                   'E': ['D', 'F']}

for c1, lista_c2 in dict_adjacencia.items():
    # print(c1, lista_c2)
    i = dict_ind_cachorros[c1]
    lista_j = [dict_ind_cachorros[c2] for c2 in lista_c2]
    for j in lista_j:
        matriz_adjacencia_cachorros[i,j] = 1


matriz_adjacencia_cachorros += matriz_adjacencia_cachorros.T

matriz_adjacencia_cachorros = pd.DataFrame(matriz_adjacencia_cachorros, index = ind_cachorros, columns = ind_cachorros)

print(matriz_adjacencia_cachorros)
if __name__ == "__main__":
    num_simulacoes = 2000
    dict_cachorro = dict()

    for i,cachorro in enumerate(ind_cachorros):
        lista = []
        for _ in range(num_simulacoes):
            lista.append(colorir_grafo_greedy(matriz_adjacencia_cachorros.values, i))
        dict_cachorro[cachorro] = np.mean(lista)

    import pprint
    pprint.pprint(dict_cachorro)
