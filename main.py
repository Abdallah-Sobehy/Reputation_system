## @package main
# Simulates a network with peers and diffusion of information
import networkx as nx
import matplotlib.pyplot as plt
import graph_modification as gm
import random as rd

# Macros like variables
NUM_PEERS = 5
PROBA = 0.3 # probability of having an edge between any 2 neighbours

# Initialize an erdos renyi graph
initial_graph = nx.erdos_renyi_graph(NUM_PEERS,PROBA,)
# Adding the property of having multiple edges between nodes
G = nx.MultiGraph(initial_graph)
li = list(G.nodes_iter())

gm.assign_normal(G)
print li[1]


nx.draw(G)
plt.show()