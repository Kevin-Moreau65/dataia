import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
from IPython.display import HTML
from utils.path import find_all_paths,evaluate_paths,distribute_flow_among_paths
from utils.ephemeral_edges import get_random_ephemeral_edges
from random import randrange
correspondances = pd.read_csv("plan du métro.csv")
correspondance_unique = []
#Filtre pour avoir des correspondances uniques
for _, correspondance in correspondances.iterrows():
    if (correspondance['de Station'] != correspondance['vers Station']):
            correspondance_unique.append(correspondance)
#Initialise le graph et les edges
def find(arr, de, vers):
    list = []
    for x in arr:
        if x["de"] == de and x["vers"] == vers:
            list.append(x)
    return list
G = nx.Graph()
ephemeral_edges = pd.read_csv("./interstations supprimées.csv")
def get_random_ephemeral_edges(prob=50):
    """
    Get all edges thaht can be cut without isolating a node
    """
    edges_return = []
    for _,edge in ephemeral_edges.iterrows():
        rand = randrange(100)
        if (rand <= prob):
            edges_return.append(edge)
    return edges_return
edge_to_delete = get_random_ephemeral_edges(100)
for row in correspondance_unique:
    result1 = find(edge_to_delete, row['de Station'], row['vers Station'])
    result2 = find(edge_to_delete, row['vers Station'], row['de Station'])
    if (len(result1) == 0 and len(result2) == 0):
        G.add_edge(row['de Station'], row['vers Station'], weight=1, capacity=99999999)
#Itère sur les passagers afin d'y ajouter le poids des passagers
passagers = pd.read_csv("passagers.csv")
for _, passager in passagers.head(20).iterrows():
    all_paths = find_all_paths(G, passager["de"], passager["vers"])

    # Étape 2 : Évaluer les chemins
    paths_with_costs = evaluate_paths(G, all_paths)

    # Étape 3 : Répartir les flux
    distributed_flows = distribute_flow_among_paths(paths_with_costs, passager["nombre"])
    for flow in distributed_flows:
        for index, bond in enumerate(flow["path"]):
            next = index + 1
            if (next + 1 >= len(flow["path"])):
                break
        G.add_edge(bond, flow["path"][next],weight=(G.get_edge_data(bond, flow["path"][next])["weight"] + flow["passengers"]), label=str(G.get_edge_data(bond, flow["path"][next])["weight"] + flow["passengers"]))
#Hack: Diviser par 30 les poids afin d'avoir des edges pas trop épais...
import copy
no_fake_edges = copy.deepcopy(G.edges(data=True))
no_fake_graph = copy.deepcopy(G)
for edge in G.edges(data=True):
    G.add_edge(edge[0], edge[1], weight=edge[2]["weight"] / 30, label=str(edge[2]["weight"]))
#Sauvegarder le graph
net = Network(
    select_menu = True, # Show part 1 in the plot (optional)
    notebook=False,
    cdn_resources='in_line'
)
net.show_buttons()
net.from_nx(G) # Create directly from nx graph
net.save_graph("networkx-pyvis.html")
import time
import os
# généré dataset
# Récupérer les arêtes du graphe
edges = list(G.edges())
# Créer un DataFrame à partir des arêtes
current_timestamp = time.time()
path = f"./DATASET/{current_timestamp}"
os.mkdir(path)
df_edges = pd.DataFrame(edges, columns=["De Station", "Vers Station"])
# Exporter le DataFrame en CSV
output_path = path  # Chemin du fichier de sortie
df_edges.to_csv(path+"/start.csv", index=False, encoding="utf-8")
# Exporter le DataFrame de sortie en CSV
dataset_sortie = pd.DataFrame([{"De Station": item[0],"Vers Station": item[1],
                                "poids": item[2]['weight']
                               } for item in no_fake_edges])
dataset_sortie.to_csv(path+"/result.csv", index=False)

print(f"Les fichier CSV ont été exporté avec succès vers : {output_path}")
import seaborn as sns
import matplotlib.pyplot as plt
weight_edge = pd.DataFrame(
    [(source, target, weight) for (source, target), weight in nx.get_edge_attributes(no_fake_graph,'weight').items()],
    columns=["Source", "Destination", "Poids"]
)
weight_edge["Path"] = weight_edge["Source"].astype(str) + " - " + weight_edge["Destination"].astype(str)
# Créer le barplot
plt.figure(figsize=(12, 6))
sns.barplot(
    data=weight_edge.sort_values("Poids",ascending= False).head(10),
    x="Path",  # Colonne des chemins
    y="Poids",   # Colonne des poids
    hue="Path",  # Ajouter la distinction des destinations
    palette="viridis"
)

# Ajouter des détails au graphique
plt.title("Poids des arêtes par lignes", fontsize=16)
plt.xlabel("Path", fontsize=14)
plt.ylabel("Poids", fontsize=14)
plt.xticks(rotation=45, fontsize=8)
#plt.legend(title="Path", fontsize=10)

plt.show()
#Visualiser le graph
HTML(filename="networkx-pyvis.html")