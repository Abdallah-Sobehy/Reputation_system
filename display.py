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
	node_size = 100
	# Getting positions for normal peers in the case of geometric graph, setting the positions of forceful ones 
	if G.graph['type'] == 'geometric':
		node_pos = nx.get_node_attributes(G,'pos')
		if G.node[total_nodes-2]['opinion'] == 1:
			print 'roger'
			node_pos[total_nodes-2] = [-0.5,0.2]
		if G.node[total_nodes-1]['opinion'] == -1:
			node_pos[total_nodes-1] = [1.25, 1]
	else : node_pos = nx.spring_layout(G)
	# Reseed to get the eact similar graph as figure 1
	np.random.seed(SEED)
	color_map = color_graph_op(G,neutral_range)
	# Figure 2 shows nodes according to their opinions
	fig2 = plt.figure('Opinion '+G.node[total_nodes-2]['type']+ ' VS '+G.node[total_nodes-1]['type'] ,(8.5,8),dpi=80)
	thismanager = plt.get_current_fig_manager()
	# thismanager.window.move(700, 0)

	if G.node[total_nodes-2]['opinion'] == 1 and G.graph['type'] != 'geometric':
		node_pos[total_nodes-2] = [-1.25,-1]
	if G.node[total_nodes-1]['opinion'] == -1 and G.graph['type'] != 'geometric':
		node_pos[total_nodes-1] = [1.25, 1]
	node_labels = {n:(n,round(G.node[n]['opinion'],3)) for n in G.nodes_iter()}
	# The following 5 draw_networkx_nodes functions are used to for legend drawing purpose (will be overwritten by draw_networkx function)
	nx.draw_networkx_nodes(G,pos=node_pos,node_size = 80,nodelist=[total_nodes-1], node_color='crimson', label=G.node[total_nodes-1]['type']+ ' forceful peer')
	nx.draw_networkx_nodes(G,pos=node_pos,node_size = 80,nodelist=[total_nodes-2], node_color='blue', label=G.node[total_nodes-2]['type']+ ' forceful peer')
	nx.draw_networkx_nodes(G,pos=node_pos,node_size = 80,nodelist=[0], node_color='lightskyblue', label='following ' + G.node[total_nodes-2]['type'] )
	nx.draw_networkx_nodes(G,pos=node_pos,node_size = 80,nodelist=[1], node_color='lightsalmon', label='following ' + G.node[total_nodes-1]['type'])
	nx.draw_networkx_nodes(G,pos=node_pos,node_size = 80, nodelist=[2], node_color='grey', label='Neurtal' )
	plt.legend(numpoints = 1, loc = (0, 0.88))
	nx.draw_networkx(G,node_pos,node_size = node_size,node_color = color_map, with_labels = False,label='following '+G.node[total_nodes-1]['type'])

	edge_labels = dict (( (i,j),G[i][j]['weight']) for (i,j) in G.edges())
	# nx.draw_networkx_edge_labels(G, node_pos, edge_labels=edge_labels)
	plt.axis('on')
	# file_path = 'documents/analysis_smart/' + G.node[total_nodes-2]['type'] + '_' + G.node[total_nodes-1]['type'] + '_'+ str(total_nodes-2)  +'_'  + G.graph['type'] + '_' + str(G.node[total_nodes-1]['budget'])
	# file_path = 'documents/' + G.node[total_nodes-2]['type'] + '_' + G.node[total_nodes-1]['type'] + '_'+ str(total_nodes-2)  +'_'  + G.graph['type'] + '_' + str(G.node[total_nodes-1]['budget'])
	# plt.savefig(file_path)
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