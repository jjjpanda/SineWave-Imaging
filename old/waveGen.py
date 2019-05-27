from PIL import Image
import numpy as np

def distance(x, y, ox, oy = -1):
    if oy == -1:
        oy = ox
    return np.sqrt((x-ox)**2 + (y-oy)**2)

def sin(x):
    return np.sin(x)

def zdistance(x, y, zoom, origin):
    return np.ceil(distance(x, y, origin[0], origin[1])) % zoom

def colorSin(freq, o, x, y, base, zoom):
    return 128 + 127 * sin(base/freq * np.pi*2 * zdistance(x,y,zoom, o)/zoom)

def createImg(dim, factor, waves, colorSplit, originSplit):
    factor = np.floor(dim/factor)
    w, h = dim, dim
    data = np.zeros((w, h, 3), dtype=np.uint8)

    waves = sorted(waves)
    base = min(waves)
    zoom = factor * int(np.ceil(base/dim)) #Every period takes zoom number of pixels

    waveOrigins = [(dim/2, dim/2)] * len(waves)
    if originSplit == True:
        if len(waves) == 2:
            waveOrigins = [(dim/3, dim/2), (2*dim/3, dim/2)]
        if len(waves) == 3:
            waveOrigins = [(dim/3, dim/2), (2*dim/3, dim/3), (2*dim/3, 2*dim/3)]
        if len(waves) == 4:
            waveOrigins = [(dim/3, dim/3), (dim/3, 2*dim/3), (2*dim/3, dim/3), (2*dim/3, 2*dim/3)]

    colorCount = 2
    waveCount = 0
    for wave in waves:
        for x in range(0, w):
            for y in range(0, h):
                data[x,y][colorCount] += colorSin(wave, waveOrigins[waveCount], x, y, base, zoom)
                data[x,y][colorCount] %= 256
        waveCount = waveCount+1
        colorCount = (colorCount+1)%3 if colorSplit else 2

    return data

def saveImage(dim, factor, waves, filename, colorSplit = False, originSplit = False):
    data = createImg(dim, factor, waves, colorSplit, originSplit)
    img = Image.fromarray(data, 'RGB')
    img.save(filename+'.png')

def showImage(dim, factor, waves, colorSplit = False, originSplit = False):
    data = createImg(dim, factor, waves, colorSplit, originSplit)
    img = Image.fromarray(data, 'RGB')
    img.show()

intervalRatios = [1, 16/15, 9/8, 6/5, 5/4, 4/3, 7/5, 3/2, 8/5, 5/3, 9/5, 15/8, 2]
intervalNames = ["U", "mi2", "M2", "mi3", "M3", "P4", "T", "P5", "mi6", "M6", "mi7", "M7", "O"]

def tetImages(dim, factor, base, colorDif = False, originDif = False): 
    saveImage(dim, factor,[base, base*intervalRatios[0]], intervalNames[0], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[1]], intervalNames[1], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[2]], intervalNames[2], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[3]], intervalNames[3], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[4]], intervalNames[4], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[5]], intervalNames[5], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[6]], intervalNames[6], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[7]], intervalNames[7], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[8]], intervalNames[8], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[9]], intervalNames[9], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[10]], intervalNames[10], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[11]], intervalNames[11], colorDif, originDif)
    saveImage(dim, factor,[base, base*intervalRatios[12]], intervalNames[12], colorDif, originDif)

def arrayFromImage(filename):
    im = Image.open(filename)
    return np.array(im)

def intervalAnalysis(filename):
    count = 0
    arr = arrayFromImage(filename)
    for x in range(0, arr.shape[0]):
        for y in range(0, arr.shape[1]):
            if( np.abs(int(arr[x,y][2]) - int(arr[x,y][0])) < 5): #Purple or Black
                count = count + 2  
            if( int(arr[x,y][0]) > 0 and int(arr[x,y][2])/int(arr[x,y][0]) < 0.1): #Red
                count = count + 1     
            if( int(arr[x,y][2]) > 0 and int(arr[x,y][0])/int(arr[x,y][2]) < 0.1): #Blue
                count = count - 1 
    return count

#tetImages(512, 2, 200, True)

#intervalsAnalysisArray = [intervalAnalysis(intervalNames[0]+".png"),intervalAnalysis(intervalNames[1]+".png"),intervalAnalysis(intervalNames[2]+".png"),intervalAnalysis(intervalNames[3]+".png"),intervalAnalysis(intervalNames[4]+".png"),intervalAnalysis(intervalNames[5]+".png"),intervalAnalysis(intervalNames[6]+".png"),intervalAnalysis(intervalNames[7]+".png"),intervalAnalysis(intervalNames[8]+".png"),intervalAnalysis(intervalNames[9]+".png"),intervalAnalysis(intervalNames[10]+".png"),intervalAnalysis(intervalNames[11]+".png"),intervalAnalysis(intervalNames[12]+".png")]
#print(intervalsAnalysisArray)

showImage(512, 8, [300, 634], originSplit= True, colorSplit=True)