import numpy as np
from Utilities.Utils import sigmoid


def activation_function(x, d=False):
    return sigmoid(x, d)


# this class performs the convolution operation in a source image
class ConvolutionLayer:

    # performs convolution
    @staticmethod
    def convolution(source, kernel, row_step=1, col_step=1):

        # process original data
        o_rows = source.shape[0]
        o_cols = source.shape[1]
        o_chans = source.shape[2]

        # find kernel dimensions
        k_rows = kernel.shape[0]
        k_cols = kernel.shape[1]

        # compute zero padding dimensions
        pad_rows = int((int(k_rows / 2) + (k_rows % 2)) / 2)
        pad_cols = int((int(k_cols / 2) + (k_cols % 2)) / 2)

        # compute result dimensions
        r_rows = int(o_rows / row_step)
        r_cols = int(o_cols / col_step)

        # allocate result data
        r_data = np.zeros((r_rows, r_cols, o_chans))

        # apply zeros border padding
        padding_width = ((pad_rows, pad_rows), (pad_cols, pad_cols), (0, 0))
        o_pix = np.pad(source, pad_width=padding_width, mode='constant', constant_values=0)

        # convolution
        for r in range(0, o_rows, row_step):
            for c in range(0, o_cols, col_step):
                for chan in range(o_chans):
                    sub_matrix = o_pix[r:r + k_rows, c:c + k_cols, chan]
                    result = sum(sub_matrix * kernel[chan])
                    r_data[r, c, chan] = sum(result)

        # produce feature
        r_data = np.array(r_data, dtype=np.float)
        return r_data


# this class performs the ReLU operation
class RectifiedLinearUnitLayer:

    # performs ReLU
    @staticmethod
    def rectify(source):
        # rectify data
        r_data = np.clip(source, 0, 255)

        # produce rectified feature
        r_data = np.array(r_data, dtype=np.uint8)
        return r_data


# this class performs the pooling operation on a set of features
class PoolingLayer:

    # performs pooling
    @staticmethod
    def max(source, window):

        o_rows = source.shape[0]
        o_cols = source.shape[1]
        o_chans = source.shape[2]

        w_rows = window.shape[0]
        w_cols = window.shape[1]

        r_rows = int(o_rows / w_rows)
        r_cols = int(o_cols / w_cols)

        # allocate result data
        r_data = np.zeros((r_rows, r_cols, o_chans), dtype=np.uint8)

        # iteration
        for r in range(r_rows):
            for c in range(r_cols):
                for chan in range(o_chans):
                    sub_matrix = source[
                                 r * w_rows: (r * w_rows) + w_rows,
                                 c * w_cols: (c * w_cols) + w_cols, chan]
                    result = np.max(sub_matrix)
                    r_data[r, c, chan] = result
        return r_data


# this class produces a fully connected neural network
class FullyConnectedNetworkLayer:

    # initializer - layers should be an array of integers, indicating the number os neurons each layer
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




