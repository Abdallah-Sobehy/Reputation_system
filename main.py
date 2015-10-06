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
SEED = 1443194868
#SEED = int(start_time)
NUM_PEERS = 100
G_TYPE = 'random' # Graph type: random, geometric, scale_free (barabasi_albert)
# Gaph characterisitic parameter:
#for random graph: probability of having an edge between any 2 neighbours
#for Geometric graph: maximum euclidean distance for a edge to exist between 2 nodes
#for barabasi albert graph: number of nodes starting the graph and number of edges a new node entering the graph will have
G_CHAR = 0.1
ALPHA = 0.3 # weight given to self opinion
STRATEGY1 = 'random' # strategy chosen by first forceful peer ((+1))
BUDGET1 = 50 #number of edges allowed for first forceful peer 
STRATEGY2 = 'D' # strategy chosen by second forceful peer ((-1))
BUDGET2 = 50 # number of edges allowed for second forceful peers
NEUTRAL_RANGE = 0.001 # opinion between +ve and -ve values of this range are considered neutral
SIMULATIONS = 1 # Number of repition of a match between 2 strategies

# seed the random generator
np.random.seed(SEED)  ;rd.seed(SEED)
# arrays to store the followers percentages of forceful peers (positive or negative) and neutral nodes for each match
S1_followers = np.zeros(SIMULATIONS)
S2_followers = np.zeros(SIMULATIONS)
neutral = np.zeros(SIMULATIONS)
# List that stores [S1_wins, S2_wins, ties]
wins= [0,0,0]

# Loop Simulation times to generate graph and evaluate results.
# taking into consideration the possibility of having to redo a simulation in case of an edgeless node appears woth 1/D strategy
i = 0
while i < SIMULATIONS:
	# Initialize an erdos renyi graph
	G = gm.create_graph(G_TYPE,NUM_PEERS, G_CHAR)
	# Add 2 forceful peers with chosen strategy
	try:
		gm.add_forceful(G, STRATEGY1, BUDGET1, STRATEGY2, BUDGET2)
	except ZeroDivisionError:
		# decrease i to redo the simulation
		i -= 1
		continue
	# Calculate final opinion vector by equation, considering the presence of 
	# 2 forceful peers in the last 2 indices of the graph
#	R_inf = cp.R_inf(G,ALPHA)
	# Calculate final opinion vector by iterations
	R_itr = gm.R_itr(G,ALPHA)
	# Calculate the percentage of normal peers that followed either of the forceful peers
	tmp = cp.percentages(G,NEUTRAL_RANGE)
	# Update percentages arrays
	cp.update_percentages(tmp, S1_followers, S2_followers, neutral, i, wins)
	i += 1

wins[0] = (wins[0]/SIMULATIONS)*100 
wins[1] = (wins[1]/SIMULATIONS)*100
wins[2] = (wins[2]/SIMULATIONS)*100

	# Asserting that R_inf calculated by equation and iteration are equal to decimal places
#try:
#	np.testing.assert_array_almost_equal(R_inf,R_itr,4)
#except AssertionError:
#	sys.exit('ConvergenceError: convergence of R_inf is not correct to 4 decimal places\nProgram will terminate')

print 'seed used: %d\tGraph type: %s' %(SEED,G_TYPE)
print 'After %d simulations: %s strategy budget = %d, %s strategy budget = %d\n\t\t\t %s strategy \t %s strategy\t neutral' %(SIMULATIONS,STRATEGY1,BUDGET1,STRATEGY2,BUDGET2, STRATEGY1,STRATEGY2)
print 'Follwers percentage\t %.2f%% \t\t %.2f%% \t %.2f%%' %(np.mean(S1_followers)*100,np.mean(S2_followers)*100,np.mean(neutral)*100) 
print 'Winning percentage:\t %.2f%% \t\t %.2f%% \t %.2f%%' %(wins[0],wins[1], wins[2])
print 'Time elapsed %f' % (time.time() - start_time)
sys.stdout.write("\a")
#input("Press Enter to continue...")
#print '\n'.join(map(str, R_itr))
# Display the graph categorizing nodes by category and by opinion based on the neutral range
#sub_normal = G.subgraph(range(NUM_PEERS))
#d.display_graph(sub_normal,NEUTRAL_RANGE)
