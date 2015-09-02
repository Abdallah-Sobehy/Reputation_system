import unittest as ut
import computation as cp
import numpy as np
import networkx as nx


class ComputationTest(ut.TestCase):
	# Setting up test fixture
	def setUp(self):
		self.alpha = 0.3
		self.G = nx.MultiGraph()
		self.G.add_nodes_from([0,1,2])
		self.G.add_edges_from([(0,1),(1,2)])
		self.G.node[0]['opinion'] = 0.3
		self.G.node[1]['opinion'] = 0.2
		self.G.node[2]['opinion'] = 0.5
	# Asserting matrix A function with expected matrix calculated by hand
	def test_mat_A(self):
		A = np.array([  [0,0.7,0],
						[0.35,0,0.35],
						[0,0.7,0]])
		np.testing.assert_array_equal(cp.mat_A(self.G,self.alpha),A,'error in matrix A calculation')
	# Asserting vec_h function with expected matrix calculated by hand
	def test_vec_h(self):
		h = np.array([[0.09],[0.06],[0.15]])
		np.testing.assert_array_equal(cp.vec_h(self.G,self.alpha),h,'error in vector h calculation')
	def test_R_inf(self):
		R_inf = np.array([[ 0.28764706],
       [ 0.28235294],
       [ 0.34764706]])
		np.testing.assert_array_almost_equal(cp.R_inf(self.G,self.alpha),R_inf,1,'error in R_inf calculation')


ut.main()