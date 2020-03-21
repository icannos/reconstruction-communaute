from network2tikz import plot
import numpy as np
import networkx as nx


def random_graph(N, pa, pb, p):
    """
    Construit un graphe selon le modèle 1
    :param N: Taille d'une communauté (le graphe possède alors 2*N sommets)
    :param pa: Proba de connexion à l'intérieur de la communauté A
    :param pb: Proba de connexion à l'intérieur de la communauté B
    :param p: Proba de connexion inter communauté
    :return: Un graphe
    """
    nodes = np.array([i for i in range(2*N)])
    classes = np.array([1 for _ in range(N)] + [-1 for _ in range(N)])
    # np.random.shuffle(classes)

    edges = []

    for i in range(2 * N):
        for j in range(i + 1, 2 * N):
            if classes[i] == classes[j] == 1:
                if np.random.choice([True, False], p=(pa, 1 - pa)):
                    edges.append((i, j))
            if classes[i] == classes[j] == -1:
                if np.random.choice([True, False], p=(pb, 1 - pb)):
                    edges.append((i, j))
            if classes[i] != classes[j]:
                if np.random.choice([True, False], p=(p, 1 - p)):
                    edges.append((i, j))

    return nodes, edges, classes


def dump_graph(file, N, pa, pb, p, colors=None):
    """
    Utilise netwokx2tikz pour exporter le graphe en latex

    :param file:
    :param N:
    :param pa:
    :param pb:
    :param p:
    :param colors:
    :return:
    """
    if colors is None:
        colors = {1: "blue", -1:"red"}

    nodes, edges, classes = random_graph(N, pa, pb, p)

    G = nx.Graph()
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, scale=5)

    style = {}
    style['node_label'] = list(classes)
    style['node_color'] = [colors[c] for c in classes]
    style['node_opacity'] = .5
    style['edge_curved'] = 0.1
    style['edge_width'] = 0.8
    style["layout"] = pos

    style['canvas'] = (8, 8)
    style['margin'] = 1

    print(nodes)

    plot((list(nodes), edges), file, **style)

dump_graph("tmp/large_inter_proba.tex", 7, 0.8, 0.8, 0.1)
dump_graph("tmp/large_small_smaller.tex", 7, 0.9, 0.3, 0.05)
dump_graph("tmp/large_largenoise.tex", 7, 0.9, 0.9, 0.5)
