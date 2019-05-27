from PIL import Image
import numpy as np

def sin(freq, x):
    return 127 + 128*np.sin(np.pi*2 * x * freq)

def distance(origin, x, y):
    return np.sqrt((x-origin)**2 + (y-origin)**2)

dim = 256
w, h = dim, dim
data = np.zeros((w, h, 3), dtype=np.uint8)

#data[int(w/2), int(h/2)] = [0, 0, 0]

waves = [100]
factor = dim/52
zoom = factor * int(np.ceil(min(waves)/dim)) #Every period takes zoom number of pixels
for wave in waves:
    for x in range(0, w):
        for y in range(0, h):
            data[x,y] = [sin(wave, distance(dim/2, x, y)), 8, 14]


img = Image.fromarray(data, 'RGB')
#img.save('my.png')
img.show()

