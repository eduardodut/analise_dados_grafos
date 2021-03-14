import numpy as np
CORES_UTILIZADAS = np.array(['k', 'b', 'r', 'c', 'm', 'g', 'y'])
# ‘b’	blue
# ‘g’	green
# ‘r’	red
# ‘c’	cyan
# ‘m’	magenta
# ‘y’	yellow
# ‘k’	black
# ‘w’	white


class Observador:
    def __init__(self):
        self.sequencia_vetor_cores = []
        self.num_passos = 0
        self.num_cores = 0
        pass

    def atualizar(self, vetor_atualizado):
        self.sequencia_vetor_cores.append(vetor_atualizado)
        self.num_cores = max(vetor_atualizado)


def colorir_grafo(matriz_adjacencia,
                  *nodes,
                  lista_cores=None,
                  vizinhos_aleatorios=True,
                  observador=None):
    import numpy as np
    import random
    random.seed()

    if lista_cores is None:
        lista_cores = np.zeros_like(
            range(matriz_adjacencia.shape[0]), dtype=int)

    if observador != None:
        observador.num_passos += 1

    vizinhos_por_no = []

    sequencia_nos = list(nodes)

    if vizinhos_aleatorios:
        random.shuffle(sequencia_nos)

    for node in sequencia_nos:

        vizinhos = np.argwhere(matriz_adjacencia[node, :] != 0).reshape(-1)

        vizinhos_por_no.append(vizinhos)
        cores_vizinhos = lista_cores[vizinhos]

        cores_vizinhos = cores_vizinhos[cores_vizinhos > 0]
        ultima_cor_utilizada = cores_vizinhos.max() if len(cores_vizinhos) > 0 else 0
        lista_cores_disponiveis = np.ones(ultima_cor_utilizada+2, dtype=bool)
        lista_cores_disponiveis[0] = False
        lista_cores_disponiveis[cores_vizinhos] = False

        for i, disponivel in enumerate(lista_cores_disponiveis):
            if disponivel:
                lista_cores[node] = i
                break
    if observador != None:
        observador.atualizar(np.array(lista_cores))

    vizinhos_por_no = np.unique(np.concatenate(vizinhos_por_no))
    vizinhos_sem_cor = np.array(
        [viz for viz in vizinhos_por_no if lista_cores[viz] == 0])

    # inicia a chamada da função de coloração para cada um dos vizinhos que ainda não possuem cores
    if len(vizinhos_sem_cor) > 0:

        # for i in indices_vizinhos_sem_cor:
        colorir_grafo(matriz_adjacencia,
                      *tuple(vizinhos_sem_cor),
                      lista_cores=lista_cores,
                      vizinhos_aleatorios=vizinhos_aleatorios,
                      observador=observador)
    return lista_cores


def _simular(matriz_adjacencia, funcao_coloracao, node):
    observador = Observador()
    lista_cores = funcao_coloracao(
        matriz_adjacencia, node, observador=observador)
    return observador


def simular(matriz_adjacencia, funcao_coloracao, simulacoes_por_no=1000):
    import multiprocessing as mp
    from multiprocessing import Pool
    n_cores = mp.cpu_count()

    pool = Pool(n_cores)
    args = []

    for p in range(matriz_adjacencia.shape[0]):
        for _ in range(simulacoes_por_no):
            args.append((matriz_adjacencia, funcao_coloracao, p))

    observadores = pool.starmap(_simular, args)

    pool.close()
    pool.join()
    return observadores


def get_max_min_cores(observadores):
    lista_qtd_cores = np.array(
        [observador.num_cores for observador in observadores])
    min_cores = max_cores = 0
    ind_min_cores = ind_max_cores = []

    lista_qtd_cores = np.unique(lista_qtd_cores)

    min_cores, max_cores = lista_qtd_cores[0], lista_qtd_cores[-1]

    lista_passos = np.array(
        [observador.num_passos for observador in observadores])

    min_passos = lista_passos.max()

    max_passos = lista_passos.min()

    indice_min_passos = indice_max_passos = 0

    for i, obs in enumerate(observadores):
        if obs.num_cores == min_cores:
            if obs.num_passos <= min_passos:
                min_passos = obs.num_passos
                indice_min_passos = i

        if obs.num_cores == max_cores:
            if obs.num_passos >= max_passos:
                max_passos = obs.num_passos
                indice_max_passos = i

    return observadores[indice_max_passos], observadores[indice_min_passos]


def get_matriz_simulacao(num_nos, observadores):
    matriz = np.array(np.array([observador.num_cores
                                for observador in observadores])).reshape(num_nos, -1)
    return matriz


def draw_grafo(matriz, plt_figure, dict_labels, cores, pos={}):
    import networkx as nx
    grafo = nx.from_numpy_array(matriz)
    if pos == {}:
        pos = nx.spring_layout(grafo, seed=1)
    nx.draw(grafo,
            pos,
            ax=plt_figure.add_subplot(111),
            labels=dict_labels,
            node_color=cores,
            font_color='white',
            with_labels=True)


def graph_to_gif(matriz_adjacencia, titulo, num_quadros=10, tempo_segundos=5, lista_labels=[],
                   pos={}):
    import random
    random.seed()
    import networkx as nx
    from matplotlib import pyplot as plt
    from matplotlib.colors import get_named_colors_mapping
    from celluloid import Camera
    import matplotlib.pyplot as plt

    grafo = nx.from_numpy_array(matriz_adjacencia)
    labels = list(range(matriz_adjacencia.shape[0]))

    if len(lista_labels) == len(labels):
        labels = [lista_labels[l] for l in labels]

    dict_ind_label = dict([(indice, letra)
                           for indice, letra in enumerate(labels)])

    fig, ax = plt.subplots()

    camera = Camera(fig)
    # pos = nx.circular_layout(grafo)
    # pos = nx.shell_layout(grafo)
    if pos == {}:
        pos = nx.spring_layout(grafo, seed=1)
    cores_atribuidas = []
    i = 20

    for n in range(num_quadros):

        if (cores_atribuidas == []) | (n % i == 0):
            node = random.choice(range(len(labels)))
            cores_atribuidas = colorir_grafo(matriz_adjacencia, node)
        cores = CORES_UTILIZADAS[cores_atribuidas]
        nx.draw(grafo,
                pos,
                ax=ax,
                labels=dict_ind_label,
                node_color=cores,
                font_color='white',
                with_labels=True)
        camera.snap()

    animation = camera.animate()
    fps = num_quadros//tempo_segundos
    animation.save(titulo+".gif", fps=fps)
    plt.close(fig)


def sequencia_coloracao_para_gif(matriz_adjacencia,
                                 observador, titulo, 
                                 lista_labels=[], 
                                 quadros_por_etapa: int = 2,
                                 segundos=5,
                                 pos={}):
    import networkx as nx
    from matplotlib import pyplot as plt
    from matplotlib.colors import get_named_colors_mapping
    from celluloid import Camera
    import matplotlib.pyplot as plt

    grafo = nx.from_numpy_array(matriz_adjacencia)
    labels = list(range(matriz_adjacencia.shape[0]))
    if len(lista_labels) == len(labels):
        labels = [lista_labels[l] for l in labels]

    dict_ind_label = dict([(indice, letra)
                           for indice, letra in enumerate(labels)])

    fig, ax = plt.subplots()

    camera = Camera(fig)
    # pos = nx.circular_layout(grafo)
    if pos == {}:
        pos = nx.spring_layout(grafo, seed=1)
    # pos = nx.planar_layout(grafo)

    fps = (quadros_por_etapa * len(observador.sequencia_vetor_cores)) // segundos
    cores_quadro_inicial = np.zeros(len(labels), dtype=int).reshape(1, -1)
    sequencia = np.vstack(
        [cores_quadro_inicial, observador.sequencia_vetor_cores])
    for lista_cores in sequencia:
        for _ in range(quadros_por_etapa):
            nx.draw(grafo,
                    pos,
                    ax=ax,
                    labels=dict_ind_label,
                    node_color=CORES_UTILIZADAS[lista_cores],
                    cmap=plt.get_cmap('Set2'),
                    font_color='white',
                    with_labels=True)
            camera.snap()

    animation = camera.animate()
    animation.save(titulo+".gif", fps=max(fps, 1))
    plt.close(fig)


def coloracao_para_png(matriz_adjacencia, cores, nome_arquivo, lista_labels=[],   pos={}):
    import random
    random.seed()
    import networkx as nx
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = list(range(matriz_adjacencia.shape[0]))

    cores = CORES_UTILIZADAS[cores]

    if len(lista_labels) == len(labels):
        labels = [lista_labels[l] for l in labels]

    f = plt.figure()
    dict_ind_label = dict([(indice, letra)
                           for indice, letra in enumerate(labels)])
    # img = plt.imread("rain.jpg")
    draw_grafo(matriz_adjacencia, f, dict_ind_label, cores, pos)

    f.savefig(nome_arquivo)


def animar_grafo(matriz, titulo, segundos, labels):
    from matplotlib import pyplot as plt
    from matplotlib.colors import get_named_colors_mapping
    from celluloid import Camera
    import numpy as np
    import random
    num_quadros = matriz.shape[1]
    fps = num_quadros // segundos
    # plt.figure(figsize=(16,10))
    fig, ax = plt.subplots()
    maximo = np.max(matriz_simulacoes)
    minimo = np.min(matriz_simulacoes)

    ax.set_ylim(minimo * 0.8, maximo * 1.2)
    ax.set_xlim(0, num_quadros)

    camera = Camera(fig)

    cor = random.choices(
        list(get_named_colors_mapping().keys()), k=len(labels))
    max_sim = []
    min_sim = []
    for i in range(matriz.shape[1]):

        # plt.legend()
        s = matriz[:, i]
        max_sim.append(np.max(s))
        min_sim.append(np.min(s))
        eixo_x = list(range(i+1))
        # ax.axhline(np.max(s),c='green',ls="--")
        # ax.axhline(np.min(s), c='blue',ls="--")

        for j, linha in enumerate(matriz[:, :i+1]):
            label = labels[j]

            ax.plot(eixo_x, linha, label=label, c=cor[j], linewidth=1)
        if matriz.shape[0] > 1:
            ax.plot(eixo_x, max_sim, label='Valor máximo local',
                    c='black', ls="--")
            ax.plot(eixo_x, min_sim, label='Valor mínimo local',
                    c='black', ls="--")
        if maximo > minimo:
            ax.axhline(maximo, label='Valor máximo', c='red', ls=":")
            ax.axhline(minimo, label='Valor mínimo', c='red', ls=":")
        camera.snap()

    animation = camera.animate()
    animation.save(titulo+".gif", fps=fps)
    plt.close(fig)


def animar_matriz_simulacoes(matriz, titulo, segundos, labels, matriz_simulacoes):
    from matplotlib import pyplot as plt
    from matplotlib.colors import get_named_colors_mapping
    from celluloid import Camera
    import numpy as np
    import random
    num_quadros = matriz.shape[1]
    fps = num_quadros // segundos
    # plt.figure(figsize=(16,10))
    fig, ax = plt.subplots()
    maximo = np.max(matriz_simulacoes)
    minimo = np.min(matriz_simulacoes)

    ax.set_ylim(minimo * 0.8, maximo * 1.2)
    ax.set_xlim(0, num_quadros)

    camera = Camera(fig)

    cor = random.choices(
        list(get_named_colors_mapping().keys()), k=len(labels))
    max_sim = []
    min_sim = []
    for i in range(matriz.shape[1]):

        # plt.legend()
        s = matriz[:, i]
        max_sim.append(np.max(s))
        min_sim.append(np.min(s))
        eixo_x = list(range(i+1))
        # ax.axhline(np.max(s),c='green',ls="--")
        # ax.axhline(np.min(s), c='blue',ls="--")

        for j, linha in enumerate(matriz[:, :i+1]):
            label = labels[j]

            ax.plot(eixo_x, linha, label=label, c=cor[j], linewidth=1)
        if matriz.shape[0] > 1:
            ax.plot(eixo_x, max_sim, label='Valor máximo local',
                    c='black', ls="--")
            ax.plot(eixo_x, min_sim, label='Valor mínimo local',
                    c='black', ls="--")
        if maximo > minimo:
            ax.axhline(maximo, label='Valor máximo', c='red', ls=":")
            ax.axhline(minimo, label='Valor mínimo', c='red', ls=":")
        camera.snap()

    animation = camera.animate()
    animation.save(titulo+".gif", fps=fps)
    plt.close(fig)


def aplicar_funcao_matriz_simulacoes(matriz_simulacoes, funcao, **kargs):
    import numpy as np
    matriz_simulacoes = matriz_simulacoes.astype(float)
    saida = np.zeros_like(matriz_simulacoes)
    for j in range(matriz_simulacoes.shape[1]):
        saida[:, j] = funcao(matriz_simulacoes[:, :j+1], axis=1, **kargs)
    return saida
