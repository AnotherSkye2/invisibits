import cv2 as cv
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def EncodeDataIntoImage(inputString):
    root = os.getcwd()
    imgPath = os.path.join(root, 'images/kollane_lill.jpg')
    img = cv.imread(imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    bitArrayString = ' '.join('{0:08b}'.format(ord(x), 'b') for x in inputString).replace(" ", "")
    byteArrayStringLength = len(bitArrayString)
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

    pixelLSBValues = []
    for i in range(len(imgRGB)):
        if len(pixelLSBValues) >= byteArrayStringLength:
            break
        for j in range(len(imgRGB[0])):
            if len(pixelLSBValues) >= byteArrayStringLength:
                break
            pixel = imgRGB[i, j]
            for k in pixel:
                if(k % 2 == 0):
                    pixelLSBValues.append('0')
                else: 
                    pixelLSBValues.append('1')

    assert("".join(pixelLSBValues[:byteArrayStringLength]) == ' '.join('{0:08b}'.format(ord(x), 'b') for x in inputString).replace(" ", ""))

    print(BitStringToString("".join(pixelLSBValues[:byteArrayStringLength])))

    # for i in range(len(imgRGB)):
    #     for j in range(len(imgRGB[i])):
    #         imgRGB[i, j] = (255, 0, 0)

    # plt.imsave('red.jpg', imgRGB)

def BitStringToString(s):
    return (int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')).decode('utf-8')

if __name__ == '__main__':
    load_dotenv()

    INPUT_STRING=os.getenv("INPUT_STRING")
    EncodeDataIntoImage(INPUT_STRING)
