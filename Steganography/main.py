from PIL import Image
from Utilities.Utils import bit_to_byte, byte_to_bit


def hide():

    secret = open('Resources/secret.txt', 'rb')
    secret_bytes = secret.read()

    bits = byte_to_bit(secret_bytes)

    image = Image.open('Resources/original.png', 'r')
    pixels = image.load()
    size = image.size
    w = size[0]
    h = size[1]

    bit = 0
    for i in range(w):
        for j in range(h):
            r = pixels[i, j][0]
            g = pixels[i, j][1]
            b = pixels[i, j][2]
            if bit < len(bits):
                if bits[bit]:
                    r |= 1
                    g |= 1
                    b |= 1
                else:
                    r &= ~1
                    g &= ~1
                    b &= ~1
                pixels[i, j] = (r, g, b)
                bit += 1
    image.save('Resources/output.png')

def show():

    image = Image.open('Resources/output.png', 'r')
    pixels = image.load()
    size = image.size
    w = size[0]
    h = size[1]

    lim = 25 * 8

    bits = []
    for i in range(w):
        for j in range(h):
            if len(bits) < lim:
                r = pixels[i, j][0]
                if r & 1:
                    bits.append(1)
                else:
                    bits.append(0)

    bytes = bit_to_byte(bits)
    outsecret = open('Resources/outsecret.txt', 'wb')
    outsecret.write(bytearray(bytes))

hide()
show()












