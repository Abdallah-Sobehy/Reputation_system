## @package main
# Simulates a network with peers and diffusion of information
import networkx as nx
import matplotlib as mpl 
import matplotlib.pyplot as plt
import graph_modification as gm
import random as rd
import numpy as np
import computation as cp
import time;
#import pydot
#import graphviz
# Macros like variables

SEED = 1441353050
#SEED = int(time.time())
NUM_PEERS = 100
PROBA = 0.06 # probability of having an edge between any 2 neighbours
THRESHOLD = 0.00001
ALPHA = 0.3 # weight given to self opinion
STRATEGY1 = 'D' # strategy chosen by first forceful peer
BUDGET1 = 20 # number of edges allowed for first forceful peer
STRATEGY2 = 'random' # strategy chosen by second forceful peer
BUDGET2 = 20 # number of edges allowed for second forceful peer

# seed the random generator
print 'seed used:', SEED
np.random.seed(SEED)
rd.seed(SEED)
# Initialize an erdos renyi graph
initial_graph = nx.erdos_renyi_graph(NUM_PEERS,PROBA)
# Adding the property of having multiple edges between nodes
G = nx.MultiGraph(initial_graph)
# Assign normal peers with type and opinion
gm.assign_normal(G)

# Add 2 forceful peers with chosen strategy
gm.add_forceful(G, STRATEGY1, BUDGET1, STRATEGY2, BUDGET2)

# Calculate final opinion vector by equation, considering the presence of 
# 2 forceful peers in the last 2 indices of the graph
print cp.R_inf(G,ALPHA)[0:9]

# Calculate final opinion vector by loops
# maximum difference variable to indicate the change in opinion after local update
max_diff = 1
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
print '\n'.join(map(str, li[0:9]))
# assert equality of R_inf calculated by both equation and iterations
R_itr = []
for n in range(NUM_PEERS):
	R_itr += [[ G.node[n]['opinion']] ]
# Asserting that R_inf calculated by equation and iteration are equal to 5 decimal places in standard format
np.testing.assert_array_almost_equal(cp.R_inf(G,ALPHA),R_itr,5,'R_inf is different by equation and iteration')

color_map = gm.color_graph(G)
nx.draw(G,node_size = 250,node_color = color_map, edge_color = 'black', with_labels = True)
plt.show()