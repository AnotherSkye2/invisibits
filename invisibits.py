import cv2 as cv
import os
import matplotlib.pyplot as plt

def ReadAndWriteSinglePixel():
    root = os.getcwd()
    imgPath = os.path.join(root, 'images/kollane_lill.jpg')
    img = cv.imread(imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # pixelLSBValues = []
    # for i in range(len(imgRGB)):
    #     pixel = imgRGB[i, 0]
    #     for j in pixel:
    #         if(j % 2 == 0):
    #             pixelLSBValues.append(0)
    #         else: 
    #             pixelLSBValues.append(1)

    # print(pixelLSBValues)
    
    for i in range(len(imgRGB)):
        for j in range(len(imgRGB[i])):
            imgRGB[i, j] = (255, 0, 0)
    plt.figure()
    plt.imshow(imgRGB)
    plt.show()
    
    plt.imsave('red.jpg', imgRGB)

if __name__ == '__main__':
    ReadAndWriteSinglePixel()
