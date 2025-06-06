import cv2 as cv
import os
import matplotlib.pyplot as plt

def EncodeDataIntoImage():
    root = os.getcwd()
    imgPath = os.path.join(root, 'images/kollane_lill.jpg')
    img = cv.imread(imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    
    testString = 'test'
    byteArrayString = ' '.join('{0:08b}'.format(ord(x), 'b') for x in testString).replace(" ", "")
    byteArrayStringLength = len(byteArrayString)
    print(byteArrayString)
    
   
    for i in range(len(imgRGB)):
        if len(byteArrayString) <= 0:
            break
        else:
            for j in range(len(imgRGB[i])):
                pixel = imgRGB[i, j]
                for k in range(len(pixel)):
                    if len(byteArrayString) <= 0:
                        break
                    if int(byteArrayString[0]) != pixel[k] % 2:
                        if pixel[k] > 0:
                            imgRGB[i, j][k] -= 1
                        else:
                            imgRGB[i, j][k] += 1
                    byteArrayString = byteArrayString[1:]

    pixelLSBValues = []
    for i in range(len(imgRGB[0])):
        pixel = imgRGB[0, i]
        for k in pixel:
            if(k % 2 == 0):
                pixelLSBValues.append('0')
            else: 
                pixelLSBValues.append('1')

    assert("".join(pixelLSBValues[:byteArrayStringLength]) == ' '.join('{0:08b}'.format(ord(x), 'b') for x in testString).replace(" ", ""))

    # for i in range(len(imgRGB)):
    #     for j in range(len(imgRGB[i])):
    #         imgRGB[i, j] = (255, 0, 0)

    # plt.imsave('red.jpg', imgRGB)

if __name__ == '__main__':
    EncodeDataIntoImage()
