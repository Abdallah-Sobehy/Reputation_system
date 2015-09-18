import networkx as nx
import matplotlib.pyplot as plt
import excp as ex
import time
import random as rd
import numpy as np
#import graphviz
#import pygraphviz
#import pydot

##
# draws the graph according to both category and opinion
#
def display_graph(G,neutral_range):
	# Seed for the graph creation to have the two graphs (category and opinion) with the same shape
	SEED = int(time.time()) ; np.random.seed(SEED) 
	color_map = color_graph_cat(G)
	fig1 = plt.figure('Categories',(8.5,8),dpi=80)
	#fig1.text(0, 0.95, 'forceful +1: dark blue\n forceful -1 dark red', style='italic',fontsize=14, fontweight='bold')
	thismanager = plt.get_current_fig_manager()
	thismanager.window.move(0, 0)
	nx.draw_graphviz(G,node_size = 80,node_color = color_map, edge_color = 'black', with_labels = False)
	
	# Reseed
	np.random.seed(SEED)
	color_map = color_graph_op(G,neutral_range)
	fig2 = plt.figure('Opinion',(8.5,8),dpi=80)
	fig2.text(0, 0.95, 'nodes are neutral in the range from -'+str(neutral_range)+ ' to ' + str(neutral_range), style='italic',fontsize=14)
	thismanager = plt.get_current_fig_manager()
	thismanager.window.move(700, 0)
	nx.draw_graphviz(G,node_size = 80,node_color = color_map, edge_color = 'black', with_labels = False)
	plt.show()
	return;

##
# colors graph to distinguish between different categories of nodes
# categories: +1, -1, attached to +1 only, attached to -1 only, attached to both, not attached to any of them
#
def color_graph_cat(G):
	n = nx.number_of_nodes(G)
	color_map = []
	for i in G:
		# color for forceful peer +1
		if G.node[i]['opinion'] == 1:
			color_map.append('blue')
		# color for forceful peer -1
		elif G.node[i]['opinion'] == -1:
			color_map.append('crimson')
		# if neighbor of -1 forceful peer
		elif n-1 in G.neighbors(i) and n-2 not in G.neighbors(i):
			color_map.append('lightsalmon')
		# if neighbor of +1 forceful peer
		elif n-2 in G.neighbors(i) and n-1 not in G.neighbors(i):
			color_map.append('lightskyblue')
		# if neighbor of both forceful peers
		elif n-1 in G.neighbors(i) and n-2 in G.neighbors(i):
			color_map.append('w')
		# if not connected to any of the forceful peer
		elif n-2 not in G.neighbors(i) and n-1 not in G.neighbors(i): # If neighbor of none of the forceful peers
			color_map.append('grey')
		# a test if a category of nodes has not been covered
		else :
			try:
				color_map.append('limegreen')
				raise ex.UncategorizedNodeError(i)
			except ex.UncategorizedNodeError as un:
				print 'warning a node [',i,'] out of the specifed categories\n will be colored in lime green '


	return color_map;

##
# colors graph to distinguish between nodes according to their opinion
# categories: +1, -1, less than neutral range, neutral, more than neutral range
# @param G graph to be drawn
# @param neutral_range a number that any node with an opinion between its negative and positive value is considered neutral
#
def color_graph_op(G,neutral_range):
	n = nx.number_of_nodes(G)
	color_map = []
	for i in G:
		# color for forceful peer +1
		if G.node[i]['opinion'] == 1:
			color_map.append('blue')
		# color for forceful peer -1
		elif G.node[i]['opinion'] == -1:
			color_map.append('crimson')
		# color for normal peer with negative opinion
		elif G.node[i]['opinion'] < - neutral_range: 
			color_map.append('lightsalmon')
		# color for normal peer with positive value
		elif G.node[i]['opinion'] > neutral_range:
			color_map.append('lightskyblue')
		# color for neutral normal peer
		elif G.node[i]['opinion'] >= - neutral_range and G.node[i]['opinion'] <= neutral_range:
			color_map.append('grey')
		# a test if a category of nodes has not been covered
		else :
			try:
				color_map.append('limegreen')
				raise ex.UncategorizedNodeError(i)
			except ex.UncategorizedNodeError as un:
				print 'warning a node [',i,'] out of the specifed categories according to opinion\n will be colored in lime green '
	return color_map;