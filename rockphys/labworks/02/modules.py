import numpy as np

def get_coeffs(p):
	"""
	Works good enough for p in range(200, 50)
	"""
	a = 3.1843687374749496 - 0.010020040080160442 * p
	b = -1.3392612376400044
	return a, b

def get_K(A, a, b):
	return np.e ** (a + b * np.log(A))

def arr_wa(arr, k=0.1):
	k_matrix = np.array([
		[k, k, k],
		[k, 1, k],
		[k, k, k],
		])
	new_arr = np.zeros(arr.shape)
	arr = np.pad(arr, 1, mode='edge') #, constant_values=0).copy()
	for i in range(new_arr.shape[0]):
		for j in range(new_arr.shape[1]):
			print(arr[i:i + 3, j:j+3].shape)
			new_arr[i, j] = np.sum(arr[i:i + 3, j:j+3].copy() * k_matrix) / np.sum(k_matrix)#np.sum((arr[i:i + 3, j:j+3].copy() != np.zeros((3, 3))) * k_matrix)
	return new_arr 