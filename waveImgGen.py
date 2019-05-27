from PIL import Image
import numpy as np

def distance(x, y, ox, oy):
    return np.sqrt((x-ox)**2 + (y-oy)**2)

def sin(x):
    return np.sin(x)

def zdistance(x, y, origin, factor):
    return round(distance(x, y, origin[0], origin[1])) % factor

def colorSin(freq, o, x, y, factor, num):
    return np.floor((128 + 127 * sin(freq * np.pi*2 * zdistance(x,y,o, factor)/factor))/num)

def createImg(dim, factor, waves, colorSplit, originSplit):
    w, h = dim, dim
    data = np.zeros((w, h, 3), dtype=np.uint8)

    waves = sorted(waves)
    factor = min(waves)*dim/(2*factor)
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
                if colorSplit:
                    data[x,y][colorCount] += colorSin(wave, waveOrigins[waveCount], x, y, factor, 1)
                    data[x,y][colorCount] %= 256
                else:
                    v = colorSin(wave, waveOrigins[waveCount], x, y, factor, len(waves))
                    data[x,y][0] += v
                    data[x,y][1] += v
                    data[x,y][2] += v
        waveCount = waveCount+1
        colorCount = (colorCount+1)%3

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
    for i in range(0, 13):
        saveImage(dim, factor,[base, base*intervalRatios[i]], intervalNames[i], colorDif, originDif)

def chordImages(dim, factor, base, colorDif = False, originDif = False):
    saveImage(dim, factor, [base, base*intervalRatios[4], base*intervalRatios[7]], "major", colorDif, originDif)
    saveImage(dim, factor, [base, base*intervalRatios[3], base*intervalRatios[7]], "minor", colorDif, originDif)
    saveImage(dim, factor, [base, base*intervalRatios[5], base*intervalRatios[7]], "sus4", colorDif, originDif)
    saveImage(dim, factor, [base, base*intervalRatios[2], base*intervalRatios[7]], "sus2", colorDif, originDif)
    saveImage(dim, factor, [base, base*intervalRatios[1], base*intervalRatios[7]], "phyrgian", colorDif, originDif)
    saveImage(dim, factor, [base, base*intervalRatios[6], base*intervalRatios[7]], "tritone", colorDif, originDif)
    

def arrayFromImage(filename):
    im = Image.open(filename)
    return np.array(im)

def intervalAnalysis(filename):
    count = 0
    arr = arrayFromImage(filename)
    for x in range(0, arr.shape[0]):
        for y in range(0, arr.shape[1]):
            if( np.abs(int(arr[x,y][2]) - int(arr[x,y][0])) < 5): #Purple or Black
                count = count + 1  
            if( int(arr[x,y][0]) > 0 and int(arr[x,y][2])/int(arr[x,y][0]) < 0.1): #Red
                count = count + 1     
            if( int(arr[x,y][2]) > 0 and int(arr[x,y][0])/int(arr[x,y][2]) < 0.1): #Blue
                count = count - 0
    return count

tetImages(512, 1, 200, True, False)

#chordImages(512, 1, 200, True, False)

#intervalsAnalysisArray = [intervalAnalysis(intervalNames[0]+".png"),intervalAnalysis(intervalNames[1]+".png"),intervalAnalysis(intervalNames[2]+".png"),intervalAnalysis(intervalNames[3]+".png"),intervalAnalysis(intervalNames[4]+".png"),intervalAnalysis(intervalNames[5]+".png"),intervalAnalysis(intervalNames[6]+".png"),intervalAnalysis(intervalNames[7]+".png"),intervalAnalysis(intervalNames[8]+".png"),intervalAnalysis(intervalNames[9]+".png"),intervalAnalysis(intervalNames[10]+".png"),intervalAnalysis(intervalNames[11]+".png"),intervalAnalysis(intervalNames[12]+".png")]
#print(intervalsAnalysisArray)

#showImage(512, 1, [200, 300], originSplit= False, colorSplit=True)