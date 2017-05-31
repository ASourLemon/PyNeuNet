import numpy as np


layers_nodes = np.array([2, 3, 3, 10, 1], dtype=int)
np.random.seed(1)


X = np.array([
    [0, 1],
    [1, 0],
    [1, 1],
    [1, 2],
    [2, 2],
    [2, 3],
    [3, 2]])
Y = np.array([[1, 1, 2, 3, 4, 5, 5]]).T


def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))


syn = np.array(range(len(layers_nodes) - 1), dtype=object)
node = np.array(range(len(layers_nodes)), dtype=object)
delta = np.array(range(len(layers_nodes) - 1), dtype=object)

for l in range(len(syn)):
    syn[l] = np.random.random((layers_nodes[l + 1], layers_nodes[l]))

for n in range(len(node)):
    node[n] = np.array(range(0, layers_nodes[n]))


max_index_node = len(node) - 1
max_index_syn = len(syn) - 1
max_index_delta = len(delta) - 1
max_index_X = len(X) - 1


for i in range(1):

    for e in range(1):

        # forward propagation
        node[0] = X[e]
        for l in range(max_index_node):
            node[l + 1] = sigmoid(np.dot(syn[l], node[l]))

        # error back-propagation
        delta[max_index_delta] = Y[e] - node[max_index_node]
        for l in range(1, len(delta)):
            delta[max_index_delta - l] = np.dot(syn[max_index_syn - l + 1].T, delta[max_index_delta - l + 1])



        # print(node[max_index_node - l])
        # error = Y[e] - node[len(layers_nodes) - 1]
        # error and delta calculation
        # update synapses
        #for l in range(0, len(syn)):
        #    delta = error * sigmoid(node[l + 1], True)
        #    syn[0] += np.dot(l0.T, delta)

#print(node[max_index_node])



