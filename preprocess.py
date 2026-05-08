import numpy as np

def prepare_input(n, p, k, temp, humidity, ph, rainfall):
    return np.array([[n, p, k, temp, humidity, ph, rainfall]])