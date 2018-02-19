import numpy as np


#  sigmoid activation function
def sigmoid(x, d=False):
    if d:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))
