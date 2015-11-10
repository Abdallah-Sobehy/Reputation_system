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
# @param G graph to be displayed
# @param neutral_range opinion between + and - of this value are considered neutral
# @param num_nodes number of nodes to be displayed: expected to be either all or without forceful peers
# @param SEED can be used to regenerate the same layout.
#
def display_graph(G,neutral_range,num_nodes,SEED):
	# Seed for the graph creation to have the two graphs (category and opinion) with the same shape
	np.random.seed(SEED)
	total_nodes = nx.number_of_nodes(G) 
	color_map = color_graph_cat(G)
	# Getting positions for normal peers in the case of geometric graph, setting the positions of forceful ones 
	if G.graph['type'] == 'geometric':
		node_pos = nx.get_node_attributes(G,'pos')
		if G.node[total_nodes-2]['opinion'] == 1:
			node_pos[total_nodes-2] = [-1.25,-1]
		if G.node[total_nodes-1]['opinion'] == -1:
			node_pos[total_nodes-1] = [1.25, 1]
	else : node_pos = None
	# Figure 1 shows nodes according to their connection with forceful peers
	# fig1 = plt.figure('Categories ' +G.node[total_nodes-2]['type']+ ' VS '+G.node[total_nodes-1]['type'],(8.5,8),dpi=80)
	# fig1.text(0, 0.97, 'Light blue: connected to '+ G.node[total_nodes-2]['type']+' ,Light red: connected to '+ G.node[total_nodes-1]['type'], style='italic',fontsize=14)
	# fig1.text(0, 0.94, 'White: connected to both,  Grey: Not connected to a forceful peer ', style='italic',fontsize=14)
	# thismanager = plt.get_current_fig_manager()
	# thismanager.window.move(0, 0)
	# nx.draw(G.subgraph(xrange(num_nodes)),node_pos,node_size = 50,node_color = color_map, edge_color = 'black', with_labels = False)
	
	# Reseed to get the eact similar graph as figure 1
	np.random.seed(SEED)
	color_map = color_graph_op(G,neutral_range)
	# Figure 2 shows nodes according to their opinions
	fig2 = plt.figure('Opinion '+G.node[total_nodes-2]['type']+ ' VS '+G.node[total_nodes-1]['type'] ,(8.5,8),dpi=80)
	fig2.text(0, 0.97, 'neutral range: '+str(neutral_range)+ '-' + str(neutral_range), style='italic',fontsize=14)
	fig2.text(0, 0.94, 'Light blue: following '+ G.node[total_nodes-2]['type']+' ,Light red: following '+ G.node[total_nodes-1]['type'], style='italic',fontsize=14)
	fig2.text(0, 0.91, 'Grey: neutral nodes', style='italic',fontsize=14)
	thismanager = plt.get_current_fig_manager()
	thismanager.window.move(700, 0)
	node_pos=nx.spring_layout(G)
	if G.node[total_nodes-2]['opinion'] == 1:
		node_pos[total_nodes-2] = [-1.25,-1]
	if G.node[total_nodes-1]['opinion'] == -1:
		node_pos[total_nodes-1] = [1.25, 1]
	node_labels = {n:(n,round(G.node[n]['opinion'],3)) for n in G.nodes_iter()}
	# nx.draw_networkx(G.subgraph(xrange(num_nodes)),node_pos,node_size = 50,node_color = color_map, edge_color = 'black', with_labels = False)
	nx.draw_networkx(G,node_pos,node_size = 700,node_color = color_map, edge_color = 'black', labels = node_labels, with_labels = True, font_size = 10,linewidths=0)
	edge_labels = dict (( (i,j),G[i][j]['weight']) for (i,j) in G.edges())
	nx.draw_networkx_edge_labels(G, node_pos, edge_labels=edge_labels)
	plt.axis('on')
	plt.show()
	return;

##
# colors graph to distinguish between different categories of nodes
# categories: +1, -1, attached to +1 only, attached to -1 only, attached to both, not attached to any of them
# @param G graph from which the nodes colors will be chsen accordingly
#
def color_graph_cat(G):
	n = nx.number_of_nodes(G)
	color_map = []
	for i in xrange(n):
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
	for i in xrange(n):
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