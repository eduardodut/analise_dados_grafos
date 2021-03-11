
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

def graph_to_mp4(matriz_adjacencia, titulo,num_quadros=10,tempo_segundos=5, lista_labels=[]):
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
    pos = nx.circular_layout(grafo)
    cores_atribuidas = []
    i = 20
    
    for n in range(num_quadros):
        
        if (cores_atribuidas == [] )| ( n % i == 0):
            ponto_partida = random.choice(range(len(labels)))
            cores_atribuidas = colorir_grafo_greedy(matriz_adjacencia, ponto_partida)
        cores = random_colors(max(cores_atribuidas))

       
        nx.draw(grafo,
                pos,
                ax=ax,
                labels=dict_ind_label,
                node_color=cores_atribuidas,
                font_color='white',
                with_labels=True)
        camera.snap()

    animation = camera.animate()
    fps = num_quadros//tempo_segundos
    animation.save(titulo+".mp4", fps=fps)
    plt.close(fig) 


def graph_to_png(matriz_adjacencia, nome_arquivo, lista_labels=[], ponto_partida = -1):
    import random
    random.seed()
    import networkx as nx
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    grafo = nx.from_numpy_array(matriz_adjacencia)
    labels = list(range(matriz_adjacencia.shape[0]))
    if ponto_partida == -1:
        ponto_partida = random.choice(labels)
    cores_atribuidas = colorir_grafo_greedy(matriz_adjacencia, ponto_partida)
    cores = random_colors(max(cores_atribuidas))

    if len(lista_labels) == len(labels):
        labels = [lista_labels[l] for l in labels]
    
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
            font_color='white',
            with_labels=True)
    f.savefig(nome_arquivo)



# def animar_grafo(matriz_adjacencia,titulo,segundos,labels,matriz_simulacoes):
def animar_grafo(matriz,titulo,segundos,labels):
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
    
    ax.set_ylim(minimo* 0.8, maximo * 1.2)
    ax.set_xlim(0,num_quadros)
    
    camera = Camera(fig)

    cor = random.choices(list(get_named_colors_mapping().keys()),k=len(labels))
    max_sim = [] 
    min_sim = []
    for i in range(matriz.shape[1]):
        
        # plt.legend()
        s = matriz[:,i]
        max_sim.append(np.max(s))
        min_sim.append(np.min(s))
        eixo_x = list(range(i+1))
        # ax.axhline(np.max(s),c='green',ls="--")
        # ax.axhline(np.min(s), c='blue',ls="--")    
          
        for j,linha in enumerate(matriz[:,:i+1]):
            label = labels[j]
            
            ax.plot(eixo_x,linha, label=label,c=cor[j], linewidth=1)
        if matriz.shape[0] > 1:    
            ax.plot(eixo_x,max_sim,label='Valor máximo local',c='black',ls="--")
            ax.plot(eixo_x,min_sim, label='Valor mínimo local',c='black',ls="--")
        if maximo > minimo:
            ax.axhline(maximo, label='Valor máximo', c='red',ls=":")
            ax.axhline(minimo, label='Valor mínimo', c='red',ls=":")
        camera.snap()

    animation = camera.animate()
    animation.save(titulo+".mp4", fps=fps)
    plt.close(fig) 



def animar_matriz_simulacoes(matriz,titulo,segundos,labels,matriz_simulacoes):
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
    
    ax.set_ylim(minimo* 0.8, maximo * 1.2)
    ax.set_xlim(0,num_quadros)
    
    camera = Camera(fig)

    cor = random.choices(list(get_named_colors_mapping().keys()),k=len(labels))
    max_sim = [] 
    min_sim = []
    for i in range(matriz.shape[1]):
        
        # plt.legend()
        s = matriz[:,i]
        max_sim.append(np.max(s))
        min_sim.append(np.min(s))
        eixo_x = list(range(i+1))
        # ax.axhline(np.max(s),c='green',ls="--")
        # ax.axhline(np.min(s), c='blue',ls="--")    
          
        for j,linha in enumerate(matriz[:,:i+1]):
            label = labels[j]
            
            ax.plot(eixo_x,linha, label=label,c=cor[j], linewidth=1)
        if matriz.shape[0] > 1:    
            ax.plot(eixo_x,max_sim,label='Valor máximo local',c='black',ls="--")
            ax.plot(eixo_x,min_sim, label='Valor mínimo local',c='black',ls="--")
        if maximo > minimo:
            ax.axhline(maximo, label='Valor máximo', c='red',ls=":")
            ax.axhline(minimo, label='Valor mínimo', c='red',ls=":")
        camera.snap()

    animation = camera.animate()
    animation.save(titulo+".mp4", fps=fps)
    plt.close(fig) 

def simular(matriz_adjacencia, i, label,funcao_coloracao):
    num_cores = max(funcao_coloracao(matriz_adjacencia, i))
    return {label:num_cores}



def gerar_simulacoes(matriz_adjacencia,num_simulacoes, labels, funcao_coloracao):
    import numpy as np
    import multiprocessing as mp
    import pandas as pd
    from multiprocessing import Pool

    args = [(matriz_adjacencia,i,label,funcao_coloracao) for i,label in enumerate(labels)]
    
    n_cores = mp.cpu_count()
    
    pool = Pool(n_cores)
    resultados = dict()
    for i in range(num_simulacoes):
        resultados[i] = pool.starmap(simular, args)

    pool.close()
    pool.join()
    saida = []

    for resultado in resultados.values():
        dict_agregado = {}
        for r in resultado:
            dict_agregado = {**dict_agregado,**r}
        saida.append(dict_agregado)
    dict_resultados_final = dict([(label,[]) for label in labels])
    for s in saida:
        for label in labels:
            dict_resultados_final[label].append(s[label])

    # dict_media_acumulativa = dict([(label, [np.mean(lista[:i+1]) for i,_ in enumerate(lista)]) for label, lista in dict_resultados_final.items()])
    matriz_simulacoes = np.stack(list(dict_resultados_final.values()))
    # matriz_media_acumulativa = np.stack([])
    # matriz_media_acumulativa = np.stack(list(dict_media_acumulativa.values()))
 

    return matriz_simulacoes

def aplicar_funcao_matriz_simulacoes(matriz_simulacoes,funcao,**kargs):
    import numpy as np
    matriz_simulacoes = matriz_simulacoes.astype(float)
    saida = np.zeros_like(matriz_simulacoes)
    for j in range(matriz_simulacoes.shape[1]):
        saida[:,j] =funcao(matriz_simulacoes[:,:j+1],axis=1,**kargs)
    return saida

# matriz_adjacencia_peixes = np.array([[0, 1, 1, 1, 1, 1, 1],
#                                      [1, 0, 0, 0, 0, 1, 1],
#                                      [1, 0, 0, 0, 0, 1, 0],
#                                      [1, 0, 0, 0, 0, 1, 1],
#                                      [1, 0, 0, 0, 0, 0, 0],
#                                      [1, 1, 1, 1, 0, 0, 0],
#                                      [1, 1, 0, 1, 0, 0, 0]])
# j=1
# aplicar_funcao_matriz_simulacoes(matriz_adjacencia_peixes,np.sum)
# saida = aplicar_funcao_matriz_simulacoes(matriz_adjacencia_peixes,np.sum)

# print(saida)