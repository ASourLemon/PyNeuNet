import numpy as np
from PIL import Image
from Network import FullyConnectedNetwork
from Network import ConvolutionLayer
from Network import RectifiedLinearUnit


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

im = Image.open("resources/bernas0.jpg")
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
feature.save('resources/l0.jpg')

r_feature = RectifiedLinearUnit.rectify(feature)
feature.save('resources/l1.jpg')



#net = FullyConnectedNetwork(np.array([5, 8, 1], dtype=int))
#print("Before")
#for i in s:
#    print(net.test(i))
#net.train(source=s, expected=e, repeat=150000, eta=0.1)
#print("After")
#or i in s:
#   print(net.test(i))
