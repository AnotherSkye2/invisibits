import cv2 as cv
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def EncodeDataIntoImage(inputString):
    root = os.getcwd()
    imgPath = os.path.join(root, 'images/cover.png')
    img = cv.imread(imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    key = "&&&"
    bitArrayString = ' '.join('{0:08b}'.format(ord(x), 'b') for x in inputString+key).replace(" ", "")    
    print(bitArrayString)
   
    for i in range(len(imgRGB)):
        if len(bitArrayString) <= 0:
            break
        else:
            for j in range(len(imgRGB[i])):
                pixel = imgRGB[i, j]
                for k in range(len(pixel)):
                    if len(bitArrayString) <= 0:
                        break
                    if int(bitArrayString[0]) != pixel[k] % 2:
                        if pixel[k] > 0:
                            imgRGB[i, j][k] -= 1
                        else:
                            imgRGB[i, j][k] += 1
                    bitArrayString = bitArrayString[1:]
    print(imgRGB[0][0])

    plt.imsave('images/img.png', imgRGB)

def BitStringToString(s):
    return (int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')).decode('utf-8')

def DecodeDataFromImage(imgPath):
    key = "001001100010011000100110"
    img = cv.imread(imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    pixelLSBValues = []
    keyFound = False
    for i in range(len(imgRGB)):
        if keyFound:
            break
        for j in range(len(imgRGB[i])):
            if keyFound:
                break
            pixel = imgRGB[i, j]
            for k in pixel:
                if len(pixelLSBValues) > len(key):
                    potentialKey = "".join(pixelLSBValues[-len(key):])
                    if potentialKey == key:
                        keyFound = True
                        break
                if(k % 2 == 0):
                    pixelLSBValues.append('0')
                else: 
                    pixelLSBValues.append('1')

    print(BitStringToString("".join(pixelLSBValues)))

if __name__ == '__main__':
    load_dotenv()

    INPUT_STRING=os.getenv("INPUT_STRING")
    IMAGE_PATH='images/img.png'
    EncodeDataIntoImage(INPUT_STRING)
    DecodeDataFromImage(IMAGE_PATH)

