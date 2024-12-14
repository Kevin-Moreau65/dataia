import pandas as pd
from random import randrange
ephemeral_edges = pd.read_csv("./ephemeral edges.csv")
def get_random_ephemeral_edges(prob=50):
    edges_return = []
    for edge in ephemeral_edges.iterrows():
        rand = randrange(100)
        if (rand <= prob):
            edges_return.append(edge)
    return edges_return
print(get_random_ephemeral_edges(100))