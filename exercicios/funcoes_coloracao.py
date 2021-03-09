
def colorir_grafo_greedy(matriz_adjacencia, ponto_partida):
    import numpy as np
    import random
    lista_cores_utilizadas = np.zeros_like(range(matriz_adjacencia.shape[0]))
    def colorir(ponto_partida):
        
        vizinhos = np.where(matriz_adjacencia[ponto_partida,:] == 1)[0]
        cores_vizinhos = sorted(lista_cores_utilizadas[vizinhos])
        cor_selecionada = 0
        for cor in range(1,max(cores_vizinhos)+1):
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