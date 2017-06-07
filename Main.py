import numpy as np
from Network import FullyConnectedNetwork
from Network import ConvolutionLayer


s = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1],
    [0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [0, 0, 1, 1, 1],
    [0, 1, 0, 1, 1],
    [1, 0, 0, 1, 1],
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1],
])
e = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1])


conv = ConvolutionLayer()
conv.convolution("", "")



#net = FullyConnectedNetwork(np.array([5, 8, 1], dtype=int))
#print("Before")
#for i in s:
#    print(net.test(i))
#net.train(source=s, expected=e, repeat=150000, eta=0.1)
#print("After")
#or i in s:
#   print(net.test(i))
