## @package main
# Simulates a network with peers and diffusion of information
import networkx as nx
import matplotlib.pyplot as plt
import graph_modification as gm
import random as rd

# Macros like variables
NUM_PEERS = 3
PROBA = 0.3 # probability of having an edge between any 2 neighbours
THRESHOLD = 0.001
ALPHA = 0.3 # weight given to self opinion

# Initialize an erdos renyi graph
initial_graph = nx.erdos_renyi_graph(NUM_PEERS,PROBA)
# Adding the property of having multiple edges between nodes
G = nx.MultiGraph(initial_graph)
# Assign normal peers with type and opinion
gm.assign_normal(G)
# maximum difference variable to indicate the change in opinion after local update
max_diff = 1
li = list(G.nodes_iter(data=True))
print li
# Loop to call Local update function until max difference is less than the threshold
# @var num_loops nuber of loops needed until conversion
num_loops = 0
while (max_diff > THRESHOLD):
	# copying an instance of the graph
	G_copy = nx.MultiGraph(G)
	gm.local_update(G,ALPHA)
	max_diff = gm.max_opinion_difference(G, G_copy)
	num_loops += 1
print 'The maximum difference = ', max_diff
print 'number of loops until conversion = ', num_loops



li = list(G.nodes_iter(data=True))
print li
nx.draw(G, with_labels = True)
plt.show()