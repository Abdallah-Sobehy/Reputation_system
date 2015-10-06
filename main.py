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


# Macros like variables
start_time = time.time()
#SEED = 1442232808
SEED = int(start_time)
NUM_PEERS = 100
G_TYPE = 'barabasi_albert' # Graph type: random, geometric, scale_free (barabasi_albert)
# Gaph characterisitic parameter:
#for random graph: probability of having an edge between any 2 neighbours
#for Geometric graph: maximum euclidean distance for a edge to exist between 2 nodes
#for barabasi albert graph: number of nodes starting the graph and number of edges a new node entering the graph will have
G_CHAR = 5
ALPHA = 0.3 # weight given to self opinion
STRATEGY1 = 'D' # strategy chosen by first forceful peer ((+1))
BUDGET1 = 50 #number of edges allowed for first forceful peer 
STRATEGY2 = 'D^2' # strategy chosen by second forceful peer ((-1))
BUDGET2 = 50 # number of edges allowed for second forceful peers
NEUTRAL_RANGE = 0.001 # opinion between +ve and -ve values of this range are considered neutral
SIMULATIONS = 50 # Number of repition of a match between 2 strategies

# seed the random generator
np.random.seed(SEED)  ;rd.seed(SEED)
# arrays to store the percentages of positive, negative, neutral nodes
pos_percent = np.zeros(SIMULATIONS)
neg_percent = np.zeros(SIMULATIONS)
neutral_percent = np.zeros(SIMULATIONS)
# Strategy 1 winning percentage
S1_win_percent = 0
# Strategy 1 winning percentage
S2_win_percent = 0
# percentage of ties between strageies 1 and 2
tie_percent = 0
# Loop Simulation times to generate graph and evaluate results.
for i in range(SIMULATIONS):
	# Initialize an erdos renyi graph
	G = gm.create_graph(G_TYPE,NUM_PEERS, G_CHAR)
	# Add 2 forceful peers with chosen strategy
	try:
		gm.add_forceful(G, STRATEGY1, BUDGET1, STRATEGY2, BUDGET2)
	except ZeroDivisionError:
		print 'ZeroDivisionError: when calculating neighbors for 1/D strategy\nSimulation match ignored'
		# Consider the results of the previous match the igore the rest of the loop
		if i != 0:
			pos_percent[i] = tmp[0]
			neg_percent[i] = tmp[1]
			neutral_percent[i] = tmp[2]
		else : sys.exit('Can not use previous match result (first iteration), program will terminate')
		continue
	# Calculate final opinion vector by equation, considering the presence of 
	# 2 forceful peers in the last 2 indices of the graph
	R_inf = cp.R_inf(G,ALPHA)
	# Calculate final opinion vector by iterations
	R_itr = gm.R_itr(G,ALPHA)
	# Calculate the percentage of normal peers that followed either of the forceful peers
	tmp = cp.percentages(G,NEUTRAL_RANGE)
	#store each percent in its array
	pos_percent[i] = tmp[0]
	neg_percent[i] = tmp[1]
	neutral_percent[i] = tmp[2]
	# Update win percentges
	if pos_percent[i] > neg_percent[i]:
		S1_win_percent += 1
	elif neg_percent[i] > pos_percent[i]:
		S2_win_percent += 1
	else : tie_percent += 1
S1_win_percent = (S1_win_percent/SIMULATIONS)*100 
S2_win_percent = (S2_win_percent/SIMULATIONS)*100
tie_percent = (tie_percent/SIMULATIONS)*100

# Asserting that R_inf calculated by equation and iteration are equal to decimal places
try:
	np.testing.assert_array_almost_equal(R_inf,R_itr,4)
except AssertionError:
	sys.exit('ConvergenceError: convergence of R_inf is not correct to 4 decimal places\nProgram will terminate')

print 'seed used:', SEED
print 'After %d simulations: %s strategy budget = %d, %s strategy budget = %d\n\t\t\t %s strategy \t %s strategy\t neutral' %(SIMULATIONS,STRATEGY1,BUDGET1,STRATEGY2,BUDGET2, STRATEGY1,STRATEGY2)
print 'Follwers percentage\t %.2f%% \t\t %.2f%% \t %.2f%%' %(np.mean(pos_percent)*100,np.mean(neg_percent)*100,np.mean(neutral_percent)*100) 
print 'Winning percentage:\t %.2f%% \t\t %.2f%% \t %.2f%%' %(S1_win_percent,S2_win_percent, tie_percent)
print 'Time elapsed %f' % (time.time() - start_time)
sys.stdout.write("\a")
#print '\n'.join(map(str, R_itr))
# Display the graph categorizing nodes by category and by opinion based on the neutral range
#sub_normal = G.subgraph(range(NUM_PEERS))
#d.display_graph(sub_normal,NEUTRAL_RANGE)
