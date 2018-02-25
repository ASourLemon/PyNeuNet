import numpy as np


#  sigmoid activation function
def sigmoid(x, d=False):
    if d:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


# converts byte list into bit list
def byte_to_bit(byte_list):
    bits = []
    for byte in byte_list:
        for i in range(8):
            if byte & 0x80:
                bits.append(1)
            else:
                bits.append(0)
            byte <<= 1
    return bits


# converts bit list into byte list
def bit_to_byte(bit_list):
    bytes = []
    for byte in range(0, len(bit_list), 8):
        byte_bits = bit_list[byte:byte+8]
        byte_value = 0
        for b in byte_bits:
            byte_value <<= 1
            byte_value |= b
        bytes.append(byte_value)
    return bytes
