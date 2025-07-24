import cv2 as cv
import utils
import matplotlib.pyplot as plt

def encodeDataIntoImage(inputString, imgPath, fullFileName, password):
    img = cv.imread(imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    if (password == ""):
        key = "&&&"
    else:
        key = password
    
    bitArrayString = ' '.join('{0:08b}'.format(ord(x), 'b') for x in inputString+key).replace(" ", "")    
    print(bitArrayString)

    passwordValue = utils.passwordValueCalculation(password, imgRGB)

    print("passwordValue: ", passwordValue)

    print("new row!")
    jumpCount = 0
    j = 0
    jumpedForward = False
    while j < len(imgRGB)*len(imgRGB[0]):
        if len(bitArrayString) <= 0:
            break
        row = j%len(imgRGB[0])
        column = int(j/len(imgRGB[0]))
        pixel = imgRGB[column, row]
        for k in range(len(pixel)):
            if len(bitArrayString) <= 0:
                break
            if int(bitArrayString[0]) != pixel[k] % 2:
                if pixel[k] > 0:
                    imgRGB[column, row][k] -= 1
                else:
                    imgRGB[column, row][k] += 1
            bitArrayString = bitArrayString[1:]
        if passwordValue == 0:
            j += 1
            continue
        if jumpedForward == False:
            j += passwordValue+1
            jumpedForward = True
        elif jumpedForward == True:
            j -= passwordValue
            jumpedForward = False
        jumpCount += 1
        print(j, len(imgRGB[0]), jumpCount, (passwordValue+1)*2, jumpCount == (passwordValue+1)*2-1)
        if jumpCount == (passwordValue+1)*2-1:
            jumpedForward = False
            jumpCount = 0
    print(imgRGB[0][0])

    fileNameArray = fullFileName.split('.')
    fileExtension = "."+fileNameArray[1]
    print(fileExtension)
    fileName = fileNameArray[0]
    if '_steg' in fileName:
        plt.imsave('images/'+fileName+fileExtension, imgRGB)
        return
    plt.imsave('images/'+fileName+'_steg'+fileExtension, imgRGB)
    return 

def decodeDataFromImage(imgPath, password):
    if (password == ""):
        key = "001001100010011000100110" # binary for "&&&"
    else:
        key = utils.stringToBinary(password)
    img = cv.imread(imgPath)
    print(img, imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    passwordValue = utils.passwordValueCalculation(password, imgRGB)

    print("passwordValue: ", passwordValue)

    pixelLSBValues = []
    keyFound = False
    jumpCount = 0
    j = 0
    jumpedForward = False
    while j < len(imgRGB)*len(imgRGB[0]):
        if keyFound:
            break
        row = j%len(imgRGB[0])
        column = int(j/len(imgRGB[0]))
        pixel = imgRGB[column, row]
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
        if passwordValue == 0:
            j += 1
            continue
        if jumpedForward == False:
            j += passwordValue+1
            jumpedForward = True
        elif jumpedForward == True:
            j -= passwordValue
            jumpedForward = False
        jumpCount += 1
        # print(j, len(imgRGB[0]), jumpCount, (passwordValue+1)*2, jumpCount == (passwordValue+1)*2-1)
        if jumpCount == (passwordValue+1)*2-1:
            jumpedForward = False
            jumpCount = 0
    print("".join(pixelLSBValues[:100]))
    print("passwordValue: ", passwordValue)
    print(key)
    if not keyFound:
        return None, "Key not found!"
    return utils.bitStringToString("".join(pixelLSBValues[:len(pixelLSBValues)-len(key)])), None
