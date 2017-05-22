import numpy as np


layers_nodes = np.array([2, 3, 1], dtype=int)
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


syn = np.array(range(0, len(layers_nodes) - 1), dtype=object)
node = np.array(range(0, len(layers_nodes)), dtype=object)


for l in range(0, len(syn)):
    syn[l] = np.random.random((layers_nodes[l + 1], layers_nodes[l]))

for n in range(0, len(node)):
    node[n] = np.array(range(0, layers_nodes[n]))

node[0] = X[0]

#print(syn[0])
#print("\n")
#print(node[0])




for i in range(15000):

    for e in range(0, len(X)):

        node[e] = X[e]

        # forward propagation
        for l in range(0, len(node)):
            node[l + 1] = sigmoid(np.dot(syn[l], node[l]))

        for l in range(0, len(node)):
            error = Y[e] - node[len(layers_nodes) - 1]



        # error and delta calculation


        # update synapses
        #for l in range(0, len(syn)):
        #    delta = error * sigmoid(node[l + 1], True)
        #    syn[0] += np.dot(l0.T, delta)

print(node[len(node) - 1])



