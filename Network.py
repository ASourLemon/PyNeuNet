import numpy as np

# learning speed coefficient
eta = 0.1

# number of training iterations
max_training_steps = 1000
# number of nodes per network layer
layers_nodes = np.array([2, 4, 8, 8, 4, 2], dtype=int)
# random seed for synapses weight initialization
np.random.seed(5)

# training input data
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1],
])
# training expected data
Y = np.array([
    [0, 1],
    [1, 0],
    [1, 1],
    [0, 0]
])


# sigmoid activation function
def sigmoid(x, d=False):
    if d:
        return x*(1-x)
    return 1/(1+np.exp(-x))


# activation function being used in the network
def activation_function(x, d=False):
    return sigmoid(x, d)


# create component arrays
node = np.array(range(len(layers_nodes)), dtype=object)
error = np.array(range(len(layers_nodes) - 1), dtype=object)
syn = np.array(range(len(layers_nodes) - 1), dtype=object)
# max index calculation for each entity
max_index_node = len(node) - 1
max_index_syn = len(syn) - 1
max_index_error = len(error) - 1

# initialize array of synapses matrix
for l in range(len(syn)):
    syn[l] = 2 * np.random.random((layers_nodes[l + 1], layers_nodes[l])) - 1

# initialize array of node vectors
for n in range(len(node)):
    node[n] = np.array(range(0, layers_nodes[n]))

# network training section
for i in range(max_training_steps):

    # iterate through training data entries
    for e in range(len(X)):

        # feed-forward propagation
        node[0] = X[e]
        for l in range(max_index_node):
            node[l + 1] = activation_function(np.dot(syn[l], node[l]))

        # error back-propagation
        error[max_index_error] = Y[e] - node[max_index_node]
        total_error = sum(error[max_index_error])
        for l in range(1, len(error)):
            error[max_index_error - l] = np.dot(syn[max_index_syn - l + 1].T, error[max_index_error - l + 1])

        # synapses weight coefficients adjustment
        for s in range(0, len(syn)):
            delta = eta * error[s] * activation_function(node[s + 1], d=True)
            syn[s] += np.dot(np.reshape(delta, (len(delta), 1)), np.reshape(node[s], (len(node[s]), 1)).T)

    print("Error: " + str(total_error))

# prediction section
node[0] = X[2]
for l in range(max_index_node):
    node[l + 1] = activation_function(np.dot(syn[l], node[l]))
print(node[max_index_node])




