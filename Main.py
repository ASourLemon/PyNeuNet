import numpy as np
from Network import FullyConnectedNetwork


s = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]])

e = np.array([0, 0, 0, 1])


net = FullyConnectedNetwork(np.array([2, 8, 1], dtype=int))
print("Before")
print(net.test(s[0]))
print(net.test(s[1]))
print(net.test(s[2]))
print(net.test(s[3]))


net.train(source=s, expected=e, repeat=150000, eta=0.1)
print("After")
print(net.test(s[0]))
print(net.test(s[1]))
print(net.test(s[2]))
print(net.test(s[3]))
