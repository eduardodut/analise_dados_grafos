import numpy as np
from funcoes_coloracao import colorir_grafo_greedy, graph_to_png
# há conflito
matriz_adjacencia_peixes = np.array([[0, 1, 1, 1, 1, 1, 1],
                                     [1, 0, 0, 0, 0, 1, 1],
                                     [1, 0, 0, 0, 0, 1, 0],
                                     [1, 0, 0, 0, 0, 1, 1],
                                     [1, 0, 0, 0, 0, 0, 0],
                                     [1, 1, 1, 1, 0, 0, 0],
                                     [1, 1, 0, 1, 0, 0, 0]])

if __name__ == "__main__":
    num_simulacoes = 200
    dict_peixe = dict()
    graph_to_png(matriz_adjacencia_peixes,
                 'grafo_peixes.png')
    for peixe in range(matriz_adjacencia_peixes.shape[0]):
        print(peixe)
        lista = []
        for _ in range(num_simulacoes):
            lista.append(max(colorir_grafo_greedy(matriz_adjacencia_peixes, peixe)))
        dict_peixe[peixe] = np.mean(lista)

    import pprint
    pprint.pprint(dict_peixe)
