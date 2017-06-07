import numpy as np
from Utils import sigmoid

from PIL import Image


def activation_function(x, d=False):
    return sigmoid(x, d)


# this class produces a fully connected neural network
class FullyConnectedNetwork:

    # initializer
    def __init__(self, layers):

        self.layers_nodes = layers

        # create component arrays
        self.node = np.array(range(len(self.layers_nodes)), dtype=object)
        self.error = np.array(range(len(self.layers_nodes) - 1), dtype=object)
        self.syn = np.array(range(len(self.layers_nodes) - 1), dtype=object)

        # max index calculation for each entity
        self.max_index_node = len(self.node) - 1
        self.max_index_syn = len(self.syn) - 1
        self.max_index_error = len(self.error) - 1

        # initialize array of synapses matrix
        for l in range(len(self.syn)):
            self.syn[l] = 2 * np.random.random((self.layers_nodes[l + 1], self.layers_nodes[l])) - 1

        # initialize array of node vectors
        for n in range(len(self.node)):
            self.node[n] = np.array(range(0, self.layers_nodes[n]))

    # method used to train the network
    def train(self, source, expected, repeat, eta):

        # network training section
        for i in range(repeat):

            # iterate through training data entries
            for e in range(len(source)):

                # feed-forward propagation
                self.node[0] = source[e]
                for l in range(self.max_index_node):
                    self.node[l + 1] = activation_function(np.dot(self.syn[l], self.node[l]))

                # error back-propagation
                    self.error[self.max_index_error] = expected[e] - self.node[self.max_index_node]
                #total_error = sum(self.error[self.max_index_error])
                for l in range(1, len(self.error)):
                    self.error[self.max_index_error - l] =\
                        np.dot(self.syn[self.max_index_syn - l + 1].T,
                               self.error[self.max_index_error - l + 1])

                # synapses weight coefficients adjustment
                for s in range(0, len(self.syn)):
                    delta = eta * self.error[s] * activation_function(self.node[s + 1], d=True)
                    self.syn[s] += np.dot(
                        np.reshape(delta, (len(delta), 1)),
                        np.reshape(self.node[s], (len(self.node[s]), 1)).T)

    # method used to test the network
    def test(self, source):
        # feed-forward propagation
        self.node[0] = source
        for l in range(self.max_index_node):
            self.node[l + 1] = activation_function(np.dot(self.syn[l], self.node[l]))
        return self.node[self.max_index_node]


# this class performs the convolution operation in a source image
class ConvolutionLayer:

    # initializer
    def __init__(self):
        print("hi")

    #
    def convolution(self, source, step):

        #o_pix = np.arange(42 * 3).reshape(6, 7, 3)
        #kernel = np.arange(9).reshape(3, 3, 3)

        kernel = np.array([
            [[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]],
            [[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]],
            [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
        ])

        o_img = Image.open("resources/111.png")
        o_pix = np.array(o_img)

        o_rows = o_pix.shape[0]
        o_cols = o_pix.shape[1]

        k_rows = kernel.shape[0]
        k_cols = kernel.shape[1]

        r_rows = o_rows - k_rows + 1
        r_cols = o_cols - k_cols + 1

        r_data = np.zeros((r_rows, r_cols, 3), dtype=np.uint8)

        print("Original")
        print(o_pix)

        print("Kernel")
        print(kernel)

        print("\n")
        for r in range(r_rows):
            for c in range(r_cols):
                sub_matrix = o_pix[r:r+k_rows, c:c+k_cols]
                result = sub_matrix * kernel
                r_sum = sum(result)
                r_data[r][c] = sum(r_sum)

                print("Submatrix " + str(r) + " " + str(c))
                print(result)
                print("Result")
                #rint(result0.shape)
                print(r_sum)
                #print("\n")
            #print("\n")


        #print(r_data)


        r_img = Image.fromarray(r_data, 'RGB')
        r_img.save('resources/out.png')

        return 0
