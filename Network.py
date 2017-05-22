import numpy as np


layers_nodes = np.array([2, 3, 1], dtype=int)
np.random.seed(1)


X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
Y = np.array([[0, 0, 1, 1]]).T


def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))


syn = np.array(range(len(layers_nodes) - 1), dtype=object)
node = np.array(range(len(layers_nodes)), dtype=object)


for l in range(len(syn)):
    syn[l] = 2 * np.random.random((layers_nodes[l + 1], layers_nodes[l])) - 1

for n in range(len(node)):
    node[n] = np.array(range(layers_nodes[n]))

node_max_index = len(node) - 1
syn_max_index = len(syn) - 1

for i in range(15000):
    for e in range(len(X)):
        node[0] = X[e]
        # forward propagation
        for l in range(node_max_index):
            node[l + 1] = sigmoid(np.dot(syn[l], node[l]))

        # back propagation
        for l in range(node_max_index):
            error = Y[e] - node[node_max_index]     #dE / dyj
            delta = error * sigmoid(node[node_max_index - l], True)     #dE / dzj
            syn[syn_max_index - l] += np.dot(node[node_max_index - l], delta)   #dE / dwij

