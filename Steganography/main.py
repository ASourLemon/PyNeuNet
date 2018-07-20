import numpy as np
from PIL import Image
from Utilities.Utils import bit_to_byte, byte_to_bit

metadata_byte_length = 10

def hide():

    # loads secret
    secret = open('Resources/secret.png', 'rb')
    secret_bytes = secret.read()

    # computes metadata
    metadata = len(secret_bytes).to_bytes(metadata_byte_length, byteorder="big")
    secret_bytes = metadata + secret_bytes

    # convert data to bits
    secret_bits = byte_to_bit(secret_bytes)

    # loads target
    image = Image.open('Resources/original.png')
    pixels = image.load()
    size = image.size
    w = size[0]
    h = size[1]

    # creates result
    secret_bit = 0
    for i in range(h):
        for j in range(w):
            r = pixels[j, i][0]
            g = pixels[j, i][1]
            b = pixels[j, i][2]
            if secret_bit < len(secret_bits):
                if secret_bits[secret_bit]:
                    r |= 1
                    g |= 1
                    b |= 1
                else:
                    r &= ~1
                    g &= ~1
                    b &= ~1
                pixels[j, i] = (r, g, b)
                secret_bit += 1

    # creates result
    image.save('Resources/output.png')

def show():

    # loads result
    image = Image.open('Resources/output.png', 'r')
    pixels = np.array(image).flatten()

    # splits data and metadata
    metadata_bit_length = metadata_byte_length * 8
    metadata_pixels = pixels[:metadata_bit_length * 4]
    data_pixels = pixels[metadata_bit_length * 4:]

    # computes metadata
    data_byte_length = 0
    for i in range(0, metadata_bit_length * 4, 4):
        r = metadata_pixels[i]
        data_byte_length = (data_byte_length << 1) | (r & 1)
    data_bit_length = data_byte_length * 8

    # computes data
    data_bits = []
    for i in range(0, data_bit_length * 4, 4):
        r = data_pixels[i]
        data_bits.insert(i, (r & 1))
    data_bytes = bit_to_byte(data_bits)

    # write to disk
    secret = open('Resources/outsecret.png', 'wb')
    secret.write(bytearray(data_bytes))

hide()
show()












