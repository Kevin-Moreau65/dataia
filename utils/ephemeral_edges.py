import pandas as pd
ephemeral_edges = pd.read_csv("./ephemeral edges.csv")
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