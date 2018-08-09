import numpy as np
from PIL import Image
import scipy.misc as smp
from Utilities.Utils import bit_to_byte, byte_to_bit

metadata_byte_length = 15
result_width = 5000
result_height = 5000

def hide():

    # loads secret
    secret = open('Resources/music.mp3', 'rb')
    secret_bytes = secret.read()

    print(len(secret_bytes))
    # computes metadata
    metadata = len(secret_bytes).to_bytes(metadata_byte_length, byteorder="big")
    secret_bytes = metadata + secret_bytes

    # convert data to bits
    secret_bits = byte_to_bit(secret_bytes)

    result_data = np.zeros((result_height, result_width, 4))
    secret_bit = 0
    for i in range(result_height):
        for j in range(result_width):
            if secret_bit < len(secret_bits) and secret_bits[secret_bit]:
                pixel = (255, 255, 255, 255)
            else:
                pixel = (0, 0, 0, 255)
            result_data[i, j] = pixel
            secret_bit += 1

    image = smp.toimage(result_data)
    image.save('Resources/output.png')

def show():

    # loads result
    image = Image.open('Resources/output.png', 'r')
    pixels = np.array(image).flatten()
    resolution = int(len(pixels) / 4)

    # splits data and metadata
    metadata_bit_length = metadata_byte_length * 8
    metadata_pixels = pixels[:metadata_bit_length * 4]
    data_pixels = pixels[metadata_bit_length * 4:]

    # computes metadata
    data_byte_length = 0
    for i in range(0, metadata_bit_length * 4, 4):
        r = metadata_pixels[i]
        if r == 255:
            data_byte_length = (data_byte_length << 1) | 1
        else:
            data_byte_length = (data_byte_length << 1) | 0
    data_bit_length = min(int(data_byte_length) * 8, resolution - metadata_bit_length)

    # computes data
    data_bits = []
    for i in range(0, data_bit_length * 4, 4):
        r = data_pixels[i]
        data_bits.insert(i, (r == 255))
    data_bytes = bit_to_byte(data_bits)

    # write to disk
    secret = open('Resources/outsecret.mp3', 'wb')
    secret.write(bytearray(data_bytes))

hide()
show()
