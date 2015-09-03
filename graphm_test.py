import unittest as ut
import graph_modification as gm
import networkx as nx
import numpy as np

class graphm_test(ut.TestCase):
	# Setting up fixture
	def setUp(self):
		self.alpha = 0.3
		self.G = nx.MultiGraph()
		self.G.add_nodes_from([0,1,2])
		self.G.add_edges_from([(0,1),(1,2)])
		self.G.node[0]['opinion'] = 0.3
		self.G.node[1]['opinion'] = 0.2
		self.G.node[2]['opinion'] = 0.5
		self.G.node[0]['type'] = 'normal'
		self.G.node[1]['type'] = 'normal'
		self.G.node[2]['type'] = 'normal'
		# store a copy of the graph to be used in a test case
		self.G_copy = nx.MultiGraph(self.G)

	# Asserting local update function
	def test_local_update(self):
		# expected R after one local update iteration
		R_expected = [ 0.23, 0.34, 0.29]
		# Update nodes opnion
		gm.local_update(self.G,self.alpha)
		R_actual = []
		for i in self.G:
			R_actual += [self.G.node[i]['opinion']]
		np.testing.assert_array_almost_equal(R_actual,R_expected,6,'error in local update function.', True)

	# Asserting max_opinion_difference function
	def test_max_opinion_diff(self):
		gm.local_update(self.G,self.alpha)
		diff_expected = 0.21
		diff_actual = gm.max_opinion_difference(self.G,self.G_copy)
		np.testing.assert_almost_equal(diff_actual, diff_expected,7, 'error in max_opinion_difference function')
	# asserting strategy_D function
	def test_strategy_D(self):
		np.random.seed(1)
		budget = 3
		# list of neighbors expected to be chosen by the forceful peer
		f_neighbors_exp = []
		# list of random numbers between 0 and 1 to choose nodes
		rnd = np.random.random(budget)
		# comparing the random numbers against limits calculated by hand
		for i in range(budget):
			if rnd[i] >= 0 and rnd[i] < 0.25:
				f_neighbors_exp += [0]
			elif rnd[i] >= 0.25 and rnd[i] < 0.75:
				f_neighbors_exp += [1]
			elif rnd[i] >= 0.75 and rnd[i] < 1:
				f_neighbors_exp += [2]
		# reseeding
		np.random.seed(1)
		f_neighbors_actual =  gm.strategy_D(self.G, budget)
		np.testing.assert_array_almost_equal(f_neighbors_actual, f_neighbors_exp,6,'error in strategy D.')


ut.main()