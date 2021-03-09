import numpy as np
from funcoes_coloracao import colorir_grafo_greedy
# há conflito
matriz_adjacencia_peixes = np.array([[0, 1, 1, 1, 1, 1, 1],
                                     [1, 0, 0, 0, 0, 1, 1],
                                     [1, 0, 0, 0, 0, 1, 0],
                                     [1, 0, 0, 0, 0, 1, 1],
                                     [1, 0, 0, 0, 0, 0, 0],
                                     [1, 1, 1, 1, 0, 0, 0],
                                     [1, 1, 0, 1, 0, 0, 0]])

if __name__ == "__main__":
    num_simulacoes =  200   
    dict_peixe = dict()
    for peixe in range(matriz_adjacencia_peixes.shape[0]):
        print(peixe)
        lista = []
        for _ in range(num_simulacoes):
            lista.append(colorir_grafo_greedy(matriz_adjacencia_peixes, peixe))
        dict_peixe[peixe] = np.mean(lista)

    import pprint
    pprint.pprint(dict_peixe)