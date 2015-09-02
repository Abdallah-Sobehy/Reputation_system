## @package computation
# contains functions related to the theoritical proof of convergence equation
# R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
from scipy import linalg
import numpy as np
import networkx as nx

##
# creates the A matrix that holds the (1-alpha)/deg part of the opinion calculation equation
# R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
# returns a square matrix with zeros in the diagonal and (1-alpha)/deg at indices representing neighbors
# @param A graph from which the A matrix will be extracted
# @param alpha weigh given to self opinion
def mat_A(G, alpha):
	n = nx.number_of_nodes(G)
	# initialize array A to zeros
	A = np.zeros(shape=(n,n))
	#iterate all nodes in the graph
	for i in range(0,n):
		# store keys of all neighbors in a list
		l_neighbors = G.neighbors(i)
		# store the degree of i
		deg = G.degree(i)
		# update A[i,j] if j is a neighbor of i
		for j in range(0,n):
			if j in l_neighbors:
				A[i,j] = (1-alpha)/deg
	return A;

##
# creates the h vector that contains the opinions of all nodes in the graph multiplied by alpha
# R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
# @param G Graph of nodes to retrieve the opinions from
# @param alpha wwight given to self opinion
#
def vec_h(G, alpha):
	n = nx.number_of_nodes(G)
	# initialize vector h to zeros
	h = np.zeros(shape=(n,1))
	#iterate all nodes in the graph
	for i in range(0,n):
		h[i] = G.node[i]['opinion']
	h = h*alpha
	return h;

##
# Calculates R (inf) using the eq R = (I - A[normal])^-1 ( h + A[forceful] * R[F])
# @param G graph under test
# @param alpha wight given to self opinion
#
def R_inf(G,alpha):
	n = nx.number_of_nodes(G)
	A = mat_A(G, alpha)
	h = vec_h(G,alpha)
	# Identity matrix to be used in the equation
	I = np.identity(n)

	R = (linalg.inv(I-A)).dot(h)
	return R;