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
SEED = 14460415
#SEED = int(start_time)
NUM_PEERS = 13
G_TYPE = 'random' # Graph type: random, geometric, scale_free (barabasi_albert)
# Gaph characterisitic parameter:
#for random graph: probability of having an edge between any 2 neighbours
#for Geometric graph: maximum euclidean distance for a edge to exist between 2 nodes
#for barabasi albert graph: number of nodes starting the graph and number of edges a new node entering the graph will have
G_CHAR = 0.25
ALPHA = 0.3 # weight given to self opinion
STRATEGY1 = 'smart' # strategy chosen by first forceful peer ((+1))
BUDGET1 = 8 #number of edges allowed for first forceful peer 
STRATEGY2 ='random' # strategy chosen by second forceful peer ((-1))
BUDGET2 = 8 # number of edges allowed for second forceful peers
NEUTRAL_RANGE = 0.001 # opinion between +ve and -ve values of this range are considered neutral
SIMULATIONS = 1 # Number of repition of a match between 2 strategies
repeated_sim = 0 # Repeated simulations in case of 1/D strategy
# seed the random generator
np.random.seed(SEED)  ;rd.seed(SEED)
# arrays to store the followers percentages of forceful peers (positive or negative) and neutral nodes for each match
S1_followers = np.zeros(SIMULATIONS)
S2_followers = np.zeros(SIMULATIONS)
neutral = np.zeros(SIMULATIONS)
# List that stores [S1_wins, S2_wins, ties]
wins= [0,0,0]
# for analytical reasons, store the winning percentage for each simulation for strategy 1
S1_wins_list = []
# Loop Simulation times to generate graph and evaluate results.
# taking into consideration the possibility of having to redo a simulation in case of an edgeless node appears woth 1/D strategy
i = 0
while i < SIMULATIONS:
	# Initialize the graph with normal peers
	G = gm.create_graph(G_TYPE,NUM_PEERS, G_CHAR)
	# Exception is thrown if there is an isolated node (ZeroDivision) or if the graph is not connected
	# In both cases the simulation is repeated
	try:
		if not nx.is_connected(G): raise Exception('Graph is not connected')
		#gm.add_forceful(G, STRATEGY1, BUDGET1, STRATEGY2, BUDGET2)
	except Exception as exp:
		# Ignore this simulation and do another one
		print type(exp)
		repeated_sim += 1
		continue
	#Add one forceul peer to the graph
	gm.add_one_forceful(G, STRATEGY2, BUDGET2)

	## Linear programming method to beat an existing peer with minimum budget
	gm.add_smart(G,ALPHA,BUDGET1, NEUTRAL_RANGE)
	# Calculate final opinion vector by equation, considering the presence of 
	# 2 forceful peers in the last 2 indices of the graph
	#R_inf = cp.R_inf(G,ALPHA)
	# Calculate final opinion vector by iterations
	R_itr = gm.R_itr(G,ALPHA)
	# Calculate the percentage of normal peers that followed either of the forceful peers
	tmp = cp.percentages(G,NEUTRAL_RANGE)
	# Update S1_wins_list for analytical reason
	if (tmp[0]>0.5): S1_wins_list.append(1)
	else: S1_wins_list.append(0)
	# Update percentages arrays
	cp.update_percentages(tmp, S1_followers, S2_followers, neutral, i, wins)
	i += 1
	# Asserting that R_inf calculated by equation and iteration are equal to decimal places
	#try:
	#	np.testing.assert_array_almost_equal(R_inf,R_itr,4)
	#except AssertionError:
	#	sys.exit('ConvergenceError: convergence of R_inf is not correct to 4 decimal places\nProgram will terminate')


wins[0] = (wins[0]/SIMULATIONS)*100 
wins[1] = (wins[1]/SIMULATIONS)*100
wins[2] = (wins[2]/SIMULATIONS)*100

print 'seed used: %d\tGraph type: %s' %(SEED,G_TYPE)
print 'After %d simulations: %s strategy budget = %d, %s strategy budget = %d\n\t\t\t %s strategy \t %s strategy\t neutral' %(SIMULATIONS,STRATEGY1,BUDGET1,STRATEGY2,BUDGET2, STRATEGY1,STRATEGY2)
print 'Follwers percentage\t %.2f%% \t\t %.2f%% \t %.2f%%' %(np.mean(S1_followers)*100,np.mean(S2_followers)*100,np.mean(neutral)*100) 
print 'Winning percentage:\t %.2f%% \t\t %.2f%% \t %.2f%%' %(wins[0],wins[1], wins[2])
print 'Time elapsed %f' % (time.time() - start_time)

#print 'Repeated simulations: ', repeated_sim
#print 'The number of simulations needed to obtain 0.5% confidence interval: ',str(cp.get_sim_num(np.mean(S1_followers),S1_followers))
#print 'The precision after ', str(SIMULATIONS), 'simulations is:', str(cp.get_precision(np.mean(S1_followers),S1_followers,SIMULATIONS))
sys.stdout.write("\a")
#input("Press Enter to continue...")
#print '\n'.join(map(str, R_itr))
# Display the graph including forceful peers (NUM_PEERS+2) or not (NUM_PEERS)categorizing nodes by category and by opinion based on the neutral range
d.display_graph(G,NEUTRAL_RANGE,NUM_PEERS,SEED)
