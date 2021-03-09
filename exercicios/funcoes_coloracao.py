
def random_colors(n):
    import random
    saida = []
    for i in range(n):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        saida.append((r, g, b))

    return saida


def colorir_grafo_greedy(matriz_adjacencia, ponto_partida):
    import numpy as np
    import random
    lista_cores_utilizadas = np.zeros_like(range(matriz_adjacencia.shape[0]))

    def colorir(ponto_partida):

        vizinhos = np.where(matriz_adjacencia[ponto_partida, :] == 1)[0]
        cores_vizinhos = sorted(lista_cores_utilizadas[vizinhos])
        cor_selecionada = lista_cores_utilizadas[ponto_partida]
        for cor in range(1, max(cores_vizinhos)+1):
            if cor not in cores_vizinhos:
                cor_selecionada = cor
                break

        if cor_selecionada == 0:
            cor_selecionada = max(cores_vizinhos)+1

        lista_cores_utilizadas[ponto_partida] = cor_selecionada

        vizinhos = [viz for viz in vizinhos if lista_cores_utilizadas[viz] == 0]

        if len(vizinhos) > 0:
            random.shuffle(vizinhos)
            for viz in vizinhos:
                colorir(viz)

    colorir(ponto_partida)

    return lista_cores_utilizadas


def graph_to_png(matriz_adjacencia, nome_arquivo, lista_labels=[]):
    import random
    import networkx as nx
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    grafo = nx.from_numpy_array(matriz_adjacencia)
    labels = list(range(matriz_adjacencia.shape[0]))
    ponto_partida = random.choice(labels)
    cores_atribuidas = colorir_grafo_greedy(matriz_adjacencia, ponto_partida)
    cores = random_colors(max(cores_atribuidas))

    if len(lista_labels) == len(labels):
        labels = [lista_labels[l] for l in labels]
    # dict_cores = dict([(l, cores[cores_atribuidas[i]-1])
    #                    for i, l in enumerate(labels)])

    f = plt.figure()
    dict_ind_label = dict([(indice, letra)
                           for indice, letra in enumerate(labels)])
    # pos = nx.spring_layout(grafo)
    pos = nx.circular_layout(grafo)
    nx.draw(grafo,
            pos,
            ax=f.add_subplot(111),
            labels=dict_ind_label,
            node_color=cores_atribuidas,
            with_labels=True)
    f.savefig(nome_arquivo)

    print()
