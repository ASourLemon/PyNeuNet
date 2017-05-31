import numpy as np


layers_nodes = np.array([2, 4, 4, 8, 1], dtype=int)
np.random.seed(5)


X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]])
Y = np.array([0, 0, 0, 1])


def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))

node = np.array(range(len(layers_nodes)), dtype=object)
error = np.array(range(len(layers_nodes) - 1), dtype=object)
syn = np.array(range(len(layers_nodes) - 1), dtype=object)

for l in range(len(syn)):
    syn[l] = 2 * np.random.random((layers_nodes[l + 1], layers_nodes[l])) - 1

for n in range(len(node)):
    node[n] = np.array(range(0, layers_nodes[n]))



max_index_node = len(node) - 1
max_index_syn = len(syn) - 1
max_index_error = len(error) - 1
max_index_X = len(X) - 1

#print(syn)

eta = 1
for i in range(15000):
    #print(syn)
    #print("\n")
    for e in range(len(X)):

        # forward propagation
        node[0] = X[e]
        for l in range(max_index_node):
            node[l + 1] = sigmoid(np.dot(syn[l], node[l]))

        # error back-propagation
        error[max_index_error] = Y[e] - node[max_index_node]
        for l in range(1, len(error)):
            error[max_index_error - l] = np.dot(syn[max_index_syn - l + 1].T, error[max_index_error - l + 1])

        # synapses weight coefficients adjustment
        for s in range(0, len(syn)):
            delta = eta * error[s] * sigmoid(node[s], True)
            syn[s] += np.dot(node[s].T, delta)


        #for l in range(0, len(syn)):
        #    l1_delta = l1_error * sigmoid(l1, True)
        #    syn[0] += np.dot(l0.T, l1_delta)

print(delta)
#print(syn)

node[0] = X[0]
for l in range(max_index_node):
    node[l + 1] = sigmoid(np.dot(syn[l], node[l]))
print(node[max_index_node])




