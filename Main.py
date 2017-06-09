import numpy as np
from PIL import Image

from Network import ConvolutionLayer
from Network import RectifiedLinearUnitLayer
from Network import PoolingLayer
from Network import FullyConnectedNetworkLayer

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

im = Image.open("resources/0.jpg")
im = np.array(im, dtype=float)
kernel = np.array(
    [
        [[-1, -1, -1],
         [-1, 8, -1],
         [-1, -1, -1]],

        [[-1, -1, -1],
         [-1, 8, -1],
         [-1, -1, -1]],

        [[-1, -1, -1],
         [-1, 8, -1],
         [-1, -1, -1]],
    ]
)
feature = ConvolutionLayer.convolution(im, kernel)
feature = RectifiedLinearUnitLayer.rectify(feature)
feature = ConvolutionLayer.convolution(feature, kernel)
feature = RectifiedLinearUnitLayer.rectify(feature)
feature = PoolingLayer.max(feature, np.zeros((2, 2)))

feature = ConvolutionLayer.convolution(im, kernel)
feature = RectifiedLinearUnitLayer.rectify(feature)
feature = ConvolutionLayer.convolution(feature, kernel)
feature = RectifiedLinearUnitLayer.rectify(feature)
feature = PoolingLayer.max(feature, np.zeros((2, 2)))

feature = ConvolutionLayer.convolution(im, kernel)
feature = RectifiedLinearUnitLayer.rectify(feature)
feature = ConvolutionLayer.convolution(feature, kernel)
feature = RectifiedLinearUnitLayer.rectify(feature)
feature = PoolingLayer.max(feature, np.zeros((2, 2)))



feature = Image.fromarray(feature)
feature.save('resources/o1.jpg')


#net = FullyConnectedNetwork(np.array([5, 8, 1], dtype=int))
#print("Before")
#for i in s:
#    print(net.test(i))
#net.train(source=s, expected=e, repeat=150000, eta=0.1)
#print("After")
#or i in s:
#   print(net.test(i))
