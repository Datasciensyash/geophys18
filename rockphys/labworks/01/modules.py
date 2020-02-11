import math
import numpy as np

def get_distribution(data, num_steps, step_size, EPS=1e-6):
    """
    Returns distribution of data at n pieces.
    """

    distribution = []
    for i in range(num_steps):
        distribution.append(np.sum((data > (np.min(data) + i * step_size - EPS)) & (data < (np.min(data) + (i + 1) * step_size))))

    return distribution

def get_step_num(data):
    return round(1 + 3.32 * math.log(len(data), 10))

def get_step_size(data, num_steps):
    return (np.max(data) - np.min(data)) / num_steps

def get_avg_sigma(data, distribution, step_size):
    return (2 * np.min(data) + step_size * (2 * np.argmax(distribution) + 1)) / 2

def get_delta(data, avg_sigma):
    return np.sqrt(np.sum((data - avg_sigma) ** 2) / (len(data) - 1))    

def find_outliers(data:np.array, delta_modifier:int=3, EPS:float=1e-6):
    """
    Finding thresolds of outliers in data.
        np.array: data -> Np array with data
        int: delta_modifier
        float: EPS -> Denominator for numerical stability

    return: turple(lower, upper) thresolds of outliers
    """
    num_steps = get_step_num(data)
    step_size = get_step_size(data, num_steps)
    distribution = get_distribution(data, num_steps, step_size, EPS=EPS)
    avg_sigma = get_avg_sigma(data, distribution, step_size)
    delta = get_delta(data, avg_sigma)

    #Get thresolds
    lower_thresold = avg_sigma - delta_modifier * delta
    upper_thresold = avg_sigma + delta_modifier * delta
    
    print((data > (lower_thresold - EPS)) & (data < (upper_thresold + EPS)))
    data_new = data[(data > (lower_thresold - EPS)) & (data < (upper_thresold + EPS))].copy()
    
    if len(data_new) != len(data):
        return find_outliers(data_new, delta_modifier=delta_modifier, EPS=EPS)
    else:
        return lower_thresold, upper_thresold
