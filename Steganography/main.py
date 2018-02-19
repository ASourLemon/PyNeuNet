from PIL import Image


def hide():

    secret = open('Resources/secret.png', 'rb')
    bits = secret.read()
    lim = len(bits)
    print(lim)
    bit = 0

    image = Image.open('Resources/original.png', 'r')
    pixels = image.load()
    size = image.size
    w = size[0]
    h = size[1]


    for i in range(w):
        for j in range(h):
            r = pixels[i, j][0]
            g = pixels[i, j][1]
            b = pixels[i, j][2]
            if bit < lim:
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

    lim = 5969 * 8
    bit = 0
    bits = [range(lim)]

    for i in range(w):
        for j in range(h):
            if bit < lim:
                break
            r = pixels[i, j][0]
            if r & 1:
                bits[bit] = 1
            else:
                bits[bit] = 0
            bit += 1

    newFile = open("Resources/outsecret.png", "wb")
    newFileByteArray = bytearray(bits)
    newFile.write(newFileByteArray)

hide()
show()












