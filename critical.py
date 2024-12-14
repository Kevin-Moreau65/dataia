import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import copy
stations = pd.read_csv("./data/position gps des stations de métro.csv")
correspondances = pd.read_csv("./data/plan du métro.csv")
weight_edges = pd.read_csv("./data/weight_edge.csv")
correspondance_unique = []
#Filtre pour avoir des correspondances uniques
for _, correspondance in correspondances.iterrows():
    if (correspondance['de Station'] != correspondance['vers Station']):
        correspondance_unique.append(correspondance)
passagers = pd.read_csv("./data/passagers.csv")
G = nx.Graph()
#Ajoute les edges
for row in correspondance_unique:
    G.add_edge(row['de Station'], row['vers Station'], weight=0)
for _,edge in weight_edges.iterrows():
    G.add_edge(edge["Source"], edge["Destination"], label=str(edge["Poids"]))
    G.add_weighted_edges_from([(edge["Source"], edge["Destination"],G.get_edge_data(edge["Source"], edge["Destination"])["weight"] + (edge["Poids"] / 3500))])
ephemeral_edges = []
for node in G.nodes():
    edges = copy.deepcopy(G.edges(node))
    if (len(edges) > 1):
        for edge in edges:
            print(edge)
            G.remove_edge(u=edge[0], v=edge[1])
            try:
                shortest_path = nx.shortest_path(G, edge[0], edge[1])
                print("more path !")
                ephemeral_edges.append({"De": edge[0], "Vers": edge[1]})
            except:
                print("1 path")
                G.add_edge(edge[0], edge[1])
file_csv = pd.DataFrame(
    ephemeral_edges,
    columns=["De", "Vers"]
)
file_csv.to_csv("ephemeral edges.csv", index=False)