import math
import numpy as np
import time 
import matplotlib.pyplot as plt

def get_distribution(data, num_steps, step_size, EPS=1e-9):
    """
    Returns distribution of data at n pieces.
    """

    distribution = []
    for i in range(num_steps):
        distribution.append(np.sum((data > (np.min(data) + i * step_size - EPS)) & (data < (np.min(data) + (i + 1) * step_size + EPS))))

    return distribution

def get_step_num(data):
    return round(1 + 3.33 * math.log(len(data), 10))

def get_step_size(data, num_steps):
    return (np.max(data) - np.min(data)) / num_steps

def draw_distribution(distribution, step_size, min_data, fnames=32):
    x = [i for i in range(len(distribution))]
    plt.bar(x, distribution, label='Распределение измерений')
    plt.xticks(x, [f'{round(min_data + step_size * i, 1)} - {round(min_data + step_size * (i + 1), 1)}' for i in x], rotation=16, size=7)
    plt.xlabel("Интенсивность гамма-измерения, Iγ")
    plt.ylabel("Количество измерений, N")
    plt.legend()
    fname = f'images/dist-{fnames}.png'
    plt.savefig(fname)
    plt.cla()

    return fname 

def get_avg_sigma(data, distribution, step_size):
    return (2 * np.min(data) + step_size * (2 * np.argmax(distribution) + 1)) / 2

def get_delta(data, avg_sigma):
    return np.sqrt(np.sum((data - avg_sigma) ** 2) / (len(data) - 1))    

def find_outliers(data:np.array, delta_modifier:float=3, EPS:float=1e-9, theta:float=2.7, iters=0):
    """
    Finding thresolds of outliers in data.
        np.array: data -> Np array with data
        int: delta_modifier
        float: EPS -> Denominator for numerical stability

    return: turple(lower, upper) thresolds of outliers
    """
    if iters == 0:
        f = open('info.md', 'w', encoding='utf-8')
    else:
        f = open('info.md', 'a', encoding='utf-8')

    f.write(f'## Итерация {iters} \n\n')

    f.write('--- \n\n')

    num_steps = get_step_num(data)
    f.write(f'Количество шагов: `{num_steps}` \n\n')
    step_size = get_step_size(data, num_steps)
    f.write(f'Размер шага: `{step_size}` \n\n')
    distribution = get_distribution(data, num_steps, step_size, EPS=EPS)
    fname = draw_distribution(distribution, step_size, np.min(data), iters)

    f.write(f'![Illustration](https://github.com/Datasciensyash/geophys18/raw/master/rockphys/labworks/07/{fname}) \n\n')


    avg_sigma = get_avg_sigma(data, distribution, step_size)
    f.write(f'Среднее значение: `{avg_sigma}` \n\n')
    delta = get_delta(data, avg_sigma)
    f.write(f'Среднеквадратичное отклонение: `{delta}` \n\n')

    #Get thresolds
    lower_thresold = avg_sigma - delta_modifier * delta
    upper_thresold = avg_sigma + delta_modifier * delta

    f.write(f'Верхняя граница: `{upper_thresold}`  \n\n')
    f.write(f'Нижняя граница: `{lower_thresold}` \n\n')
    
    data_new = data[(data > (lower_thresold - EPS)) & (data < (upper_thresold + EPS))].copy()
    
    if len(data_new) != len(data):
        f.write(f'Кол-во обнаруженых аномальных значений: `{len(data) - len(data_new)}` \n\n')
        f.close()
        return find_outliers(data_new, delta_modifier=delta_modifier, EPS=EPS, iters=iters+1)
    else:
        f.write(f'Аномальных значений `не найдено`. \n\n')
        f.close()
        density_average = np.sum(data_new) / len(data_new)
        sigma_ro = delta / np.sqrt(len(data_new))
        delta_sigma = sigma_ro * theta
        accuracy = 1 / delta_sigma
        return lower_thresold, upper_thresold, distribution, [avg_sigma, delta, step_size, np.min(data), accuracy, sigma_ro], density_average, delta_sigma
