## @package main
# Simulates a network with peers and diffusion of information
import networkx as nx
import matplotlib.pyplot as plt

# Macros like variables
NUM_PEERS = 10
PROBA = 0.3 # probability of having an edge between any 2 neighbours

# Initialize an erdos renyi graph
initial_graph = nx.erdos_renyi_graph(NUM_PEERS,PROBA)
# Adding the property of having multiple edges between nodes
G = nx.MultiGraph(initial_graph)
G.add_edge(0,1, weight=3)
G.add_edge(0,1, weight=115)

#print list(G.edges_iter(data=True))

nx.draw(G)
plt.show()