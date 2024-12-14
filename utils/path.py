import networkx as nx
def find_all_paths(graph, origin, destination, max_hops=10):
    """
    Trouve tous les chemins simples entre deux nœuds.
    graph: Graphe NetworkX.
    origin: Station d'origine.
    destination: Station de destination.
    max_hops: Limite sur la longueur des chemins pour éviter une explosion combinatoire.
    """
    return list(nx.all_simple_paths(graph, source=origin, target=destination, cutoff=max_hops))
def evaluate_paths(graph, paths):
    """
    Évalue chaque chemin et calcule son coût total.
    graph: Graphe NetworkX.
    paths: Liste de chemins (listes de nœuds).
    """
    path_costs = []
    for path in paths:
        cost = sum(graph[u][v]["weight"] for u, v in zip(path[:-1], path[1:]))
        path_costs.append((path, cost))
    return path_costs
def distribute_flow_among_paths(paths_with_costs, total_passengers):
    """
    Répartit les passagers sur plusieurs chemins en fonction de leurs coûts.
    paths_with_costs: Liste de tuples (chemin, coût).
    total_passengers: Nombre total de passagers à répartir.
    """
    # Inverser les coûts pour obtenir des poids proportionnels
    inverted_costs = [1 / cost for _, cost in paths_with_costs]
    total_inverse_cost = sum(inverted_costs)

    # Calcul des proportions
    proportions = [inv_cost / total_inverse_cost for inv_cost in inverted_costs]

    # Répartition des passagers
    distributed_flows = [
        {"path": path, "passengers": round(total_passengers * proportion)}
        for (path, _), proportion in zip(paths_with_costs, proportions)
    ]
    return distributed_flows