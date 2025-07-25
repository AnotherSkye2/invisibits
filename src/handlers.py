import os
from cherrypy._json import encode
from methods import encodeDataIntoImage, decodeDataFromImage
from PIL import Image


def encodeHandler(self, inputString, fileName, password, imgDir):
    imgPath = os.path.join(imgDir, fileName)
    print("imgPath: ", imgPath, "password: ", password)
    encodeDataIntoImage(inputString, imgPath, fileName, password)
    out = '''
    Image encoded.
    Filename: {}
    ''' .format(fileName)
    return out

def uploadHandler(self, imgFile, fileName, imgDir): 
    print("\nimgFile: ", imgFile, "\nfileName: ", fileName)

    upload_file = os.path.normpath(
        os.path.join(imgDir, fileName))
    size = 0
    with open(upload_file, 'wb') as out:
        while True:
            data = imgFile.file.read(8192)
            if not data:
                break
            out.write(data)
            size += len(data)
    if ".jpg" or ".JPG" in fileName:
        im = Image.open(upload_file)
        fileName = fileName.replace(".jpg", ".png")
        fileName = fileName.replace(".JPG", ".png")
        im.save(os.path.normpath(
        os.path.join(imgDir, fileName)))
        print("fileName:", fileName, im)

    out = '''
    File received.
    Filename: {}
    Length: {}
    Mime-type: {}
    ''' .format(imgFile.filename, size, imgFile.content_type, data)
    return out

def decodeHandler(self, fileName, password, imgDir):
    imgPath = os.path.join(imgDir, fileName)
    print("imgPath: ", imgPath, "password: ", password)
    result, err = decodeDataFromImage(imgPath, password)
    print("The result is: ", result)
    if err or result == None:
        return encode({"error": 'Wrong password!'})
    return encode(result)