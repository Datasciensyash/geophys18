import numpy as np

def print_array(arr, diag_val=0, print_end=',', prettify_out=True):
	rows = arr.shape[0]
	cols = arr.shape[1]

	if prettify_out:
		max_len = len(str(np.max(arr)))

	for i in range(rows):
		for j in range(cols):
			if arr[i, j] != diag_val:
				element = str(arr[i, j])
				if prettify_out:
					element = (max_len - len(element)) * ' ' + element
				print(element, end=print_end)
			else:
				print(' ', end=print_end)
		print('\n', end='')
	print('\n', end='')

def get_all_matrices(arr_size:int=10, diag:bool=True, print_end:str=',', prettify_out:bool=True):
	"""
	Процедура получения всех массивов сразу.

	int:arr_size: Размер массива.
	bool:diag: Если False, то элементы на диагонали заменяются на пробелы.
	str:print_end: Строка, завершающая вывод каждого элемента массива.
	bool:prettify_out: Если True, то массив будет выводиться красиво.

	"""
	arr = np.array([i for i in range(1, arr_size**2 + 1)]).reshape((-1, arr_size))

	if not diag:
		np.fill_diagonal(arr, 0)
		np.fill_diagonal(np.fliplr(arr), 0)

	for index in range(4):
		print_array(arr, diag_val=0, print_end=print_end, prettify_out=prettify_out)
		print_array(arr.T, diag_val=0, print_end=print_end, prettify_out=prettify_out)
		arr = np.rot90(arr)
	return None

get_all_matrices(arr_size=10, diag=False, print_end=',', prettify_out=True)



