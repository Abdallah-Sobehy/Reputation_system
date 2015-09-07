import sys
# Exception triggered when the R_inf values are different when calculated by equation and by iteration
class ConvergenceError(AssertionError):
	def __init__(self,decimal_places):
		self.decimal_places = decimal_places
		print 'ConvergenceError: convergence of R_inf is not correct to %d decimal places' %self.decimal_places
		sys.exit()
	def __str__(self):
		tmp = 'convergence of R_inf is not correct to %d decimal places' %self.decimal_places
		return repr(tmp)

# Exception triggered when a node is not in one of the specified category
class UncategorizedNodeError(Exception):
	def __init__(self,n_key):
		self.node = n_key