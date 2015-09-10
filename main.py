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
start_time = time.time()
#SEED = 1441804756
SEED = int(start_time)
NUM_PEERS = 100
PROBA = 0.1 # probability of having an edge between any 2 neighbours
ALPHA = 0.3 # weight given to self opinion
STRATEGY1 = 'random' # strategy chosen by first forceful peer
BUDGET1 = 50 # number of edges allowed for first forceful peer
STRATEGY2 = 'D^2' # strategy chosen by second forceful peer
BUDGET2 = 50 # number of edges allowed for second forceful peer
NEUTRAL_RANGE = 0.001 # opinion between +ve and -ve values of this range are considered neutral
SIMULATIONS = 500 # Number of repition of a match between 2 strategies

# seed the random generator
np.random.seed(SEED)  ;rd.seed(SEED)
# arrays to store the percentages of positive, negative, neutral nodes
pos_percent = np.zeros(SIMULATIONS)
neg_percent = np.zeros(SIMULATIONS)
neutral_percent = np.zeros(SIMULATIONS)
for i in range(SIMULATIONS):
	# Initialize an erdos renyi graph
	G = gm.create_graph(NUM_PEERS, PROBA)
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
#	R_inf = cp.R_inf(G,ALPHA)
	# Calculate final opinion vector by iterations
	R_itr = gm.R_itr(G,ALPHA)
	# Calculate the percentage of normal peers that followed either of the forceful peers
	tmp = cp.percentages(G,NEUTRAL_RANGE)
	#store each percent in its array
	pos_percent[i] = tmp[0]
	neg_percent[i] = tmp[1]
	neutral_percent[i] = tmp[2]
	# Print result each 100 simulation match
	if i%100 == 0:
		print '%f, %f,%f'%(np.sum(pos_percent)/(i+1), np.sum(neg_percent)/(i+1), np.sum(neutral_percent)/(i+1))
	# Asserting that R_inf calculated by equation and iteration are equal to decimal places
#	try:
#		np.testing.assert_array_almost_equal(R_inf,R_itr,4)
#	except AssertionError:
#		sys.exit('ConvergenceError: convergence of R_inf is not correct to 4 decimal places\nProgram will terminate')
print 'seed used:', SEED 
print 'After %d simulations\n%s strategy nodes: %f\n%s strategy nodes: %f\nNeutral Nodes: %f' %(SIMULATIONS,STRATEGY1,np.mean(pos_percent),STRATEGY2,np.mean(neg_percent),np.mean(neutral_percent))
print 'Time elapsed %f' % (time.time() - start_time)
#print '\n'.join(map(str, R_itr))
# Display the graph categorizing nodes by category and by opinion based on the neutral range
d.display_graph(G,NEUTRAL_RANGE)