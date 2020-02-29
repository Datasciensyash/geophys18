import numpy as np

def get_coeffs(p):
	"""
	Works good enough for p in range(200, 50)
	"""
	a = 3.1843687374749496 + -0.010020040080160442 * p
	b = -1.3392612376400044
	return a, b

def get_K(A, a, b):
	return np.e ** (a + b * np.log(A))
