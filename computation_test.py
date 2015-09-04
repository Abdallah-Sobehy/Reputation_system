from __future__ import division
from scipy import linalg
import unittest as ut
import computation as cp
import numpy as np
import networkx as nx


class ComputationTest(ut.TestCase):
	# Setting up test fixture
	def setUp(self):
		self.alpha = 0.3
		self.G = nx.MultiGraph()
		self.G.add_nodes_from([0,1,2,3,4])
		self.G.add_edges_from([(0,1),(1,2)])
		self.G.node[0]['opinion'] = 0.3
		self.G.node[1]['opinion'] = 0.2
		self.G.node[2]['opinion'] = 0.5
		self.G.node[0]['initial_opinion'] = 0.3
		self.G.node[1]['initial_opinion'] = 0.2
		self.G.node[2]['initial_opinion'] = 0.5
		self.G.node[0]['type'] = 'normal'
		self.G.node[1]['type'] = 'normal'
		self.G.node[2]['type'] = 'normal'
		# Forceful peers
		self.G.node[3]['opinion'] = 1
		self.G.node[4]['opinion'] = -1
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
	# Asserting R_inf function if forceful peers are not attached
	# expected matrix calculated by hand
	def test_R_inf(self):
		R_inf = np.array([[ 0.28764706],
       [ 0.28235294],
       [ 0.34764706]])
		np.testing.assert_array_almost_equal(cp.R_inf(self.G,self.alpha),R_inf,7,'error in R_inf calculation')
	# Asserting R_inf with forceful peer attached
	def test_R_inf(self):
		self.G.add_edge(3,0)
		self.G.add_edge(3,0)
		self.G.add_edge(3,1)
		AF_exp = np.array([  [7/15,0],
						[7/30,0],
						[0,0]])
		np.testing.assert_array_almost_equal(cp.mat_AF(self.G,self.alpha),AF_exp,7,'error in AF calculation')
		RF = np.array([[1],[-1]])
		I = np.identity(3)
		# mat_A ad vec_h are used in previosus tests so if they do not fail they can be used in this test
		A = cp.mat_A(self.G,self.alpha)
		h = cp.vec_h(self.G,self.alpha)
		R_inf_exp = (linalg.inv(I-A)).dot(h+(AF_exp.dot(RF)))
		np.testing.assert_array_almost_equal(cp.R_inf(self.G,self.alpha),R_inf_exp,7,'Error in R_inf function')
if __name__ == "__main__":
	ut.main()