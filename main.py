## @package main
# Simulates a network with peers and diffusion of information
from __future__ import division # to allow integer division to produce a floating point
import networkx as nx
import matplotlib.pyplot as plt
import graph_modification as gm
import random as rd
import numpy as np
import computation as cp
import time
import excp as ex
import sys
import display as d
#import pydot
#import graphviz

# Macros like variables

#SEED = 1441635615
SEED = int(time.time())
NUM_PEERS = 300
PROBA = 0.04 # probability of having an edge between any 2 neighbours
ALPHA = 0.3 # weight given to self opinion
STRATEGY1 = 'random' # strategy chosen by first forceful peer
BUDGET1 = 150 # number of edges allowed for first forceful peer
STRATEGY2 = '1/D' # strategy chosen by second forceful peer
BUDGET2 = 150 # number of edges allowed for second forceful peer
NEUTRAL_RANGE = 0.001 # opinion between +ve and -ve values of this range are considered neutral

# seed the random generator
print 'seed used:', SEED ; np.random.seed(SEED)  ;rd.seed(SEED)
# Initialize an erdos renyi graph
G = gm.create_graph(NUM_PEERS, PROBA)

# Add 2 forceful peers with chosen strategy
gm.add_forceful(G, STRATEGY1, BUDGET1, STRATEGY2, BUDGET2)

# Calculate final opinion vector by equation, considering the presence of 
# 2 forceful peers in the last 2 indices of the graph
R_inf = cp.R_inf(G,ALPHA)

# Calculate final opinion vector by iterations
R_itr = gm.R_itr(G,ALPHA)


# Calculate the percentage of normal peers that followed either of the forceful peers
pos_percent = neg_percent = neutral_perc = 0
for i in range(NUM_PEERS):
	if G.node[i]['opinion'] < - NEUTRAL_RANGE:
		neg_percent +=1
	elif G.node[i]['opinion'] > NEUTRAL_RANGE:
		pos_percent +=1
	elif G.node[i]['opinion'] >= - NEUTRAL_RANGE and G.node[i]['opinion'] <= NEUTRAL_RANGE:
		neutral_perc +=1
	else:
		try:
			raise ex.UncategorizedNodeError(i)
		except ex.UncategorizedNodeError as un:
				print 'warning a node [',i,'] out of the specifed categories according to opinion'
pos_percent /= NUM_PEERS
neg_percent /= NUM_PEERS
neutral_perc /= NUM_PEERS
print 'Positive nodes: %f\nNegative nodes: %f\nNeutral Nodes: %f' %(pos_percent,neg_percent,neutral_perc)


# Asserting that R_inf calculated by equation and iteration are equal to decimal places
try:
	np.testing.assert_array_almost_equal(R_inf,R_itr,4)
except AssertionError:
	sys.exit('ConvergenceError: convergence of R_inf is not correct to 4 decimal places\nProgram will terminate')

#print '\n'.join(map(str, R_itr))
# Display the graph categorizing nodes by category and by opinion based on the neutral range
#d.display_graph(G,NEUTRAL_RANGE)