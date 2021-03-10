
def random_colors(n):
    import random
    random.seed()
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
    random.seed()
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
    random.seed()
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


def animar_matriz_media_cumulativa(matriz,titulo,fps,labels):
    from matplotlib import pyplot as plt
    from matplotlib.colors import get_named_colors_mapping
    from celluloid import Camera
    import numpy as np
    import random
    
    # plt.figure(figsize=(16,10))
    fig, ax = plt.subplots()
    
    minimo = np.min(matriz) 
    maximo = np.max(matriz)
    
    ax.set_ylim(minimo* 0.8, maximo * 1.2)
    ax.set_xlim(0, matriz.shape[1])
    
    camera = Camera(fig)

    cor = random.choices(list(get_named_colors_mapping().keys()),k=len(labels))
    for i in range(matriz.shape[1]):
        if maximo > minimo:
            ax.axhline(maximo, label='Valor máximo', c='gray',ls=":")
            ax.axhline(minimo, label='Valor mínimo', c='gray',ls=":")
        # plt.legend()
        for j,linha in enumerate(matriz):
            label = labels[j]
            
            ax.plot(list(range(i+1)),linha[:i+1], label=label,c=cor[j])
            # plt.legend(loc='upper left')
        camera.snap()

    animation = camera.animate()
    animation.save(titulo, writer='PillowWriter', fps=fps)


def gerar_dicionarios(matriz_adjacencia,num_simulacoes, labels):
    import numpy as np
    dict_no = dict([(label,[]) for label in labels])
    for _ in range(num_simulacoes):
        for i,label in enumerate(labels):
            num_cores = max(colorir_grafo_greedy(matriz_adjacencia, i))
            dict_no[label].append(num_cores)
    
    dict_max = dict([(label, np.max(lista)) for label, lista in dict_no.items()])
    dict_min = dict([(label, np.min(lista)) for label, lista in dict_no.items()])
    dict_media = dict([(label, np.mean(lista)) for label, lista in dict_no.items()])
    dict_media_acumulativa = dict([(label, [np.mean(lista[:i+1]) for i,_ in enumerate(lista)]) for label, lista in dict_no.items()])
    return dict_max, dict_min, dict_media, dict_media_acumulativa



