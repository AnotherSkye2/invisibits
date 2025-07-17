import cv2 as cv
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import cherrypy
from cherrypy._json import encode
from cherrypy.lib.static import serve_download

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

def readf(filename):
    file = open(filename)
    read = file.read()
    return read

def EncodeDataIntoImage(inputString, imgPath, fullFileName):
    root = os.getcwd()
    imgPath = os.path.join(root, imgPath)
    print(imgPath)
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

    fileNameArray = fullFileName.split('.')
    fileExtension = fileNameArray[1]
    print(fileExtension)
    fileName = fileNameArray[0]
    plt.imsave('images/'+fileName+'_steg.'+fileExtension, imgRGB)

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

    return BitStringToString("".join(pixelLSBValues[:len(pixelLSBValues)-len(key)]))

class Root:
    @cherrypy.expose
    def index(self):
        return "aaa"
    
    @cherrypy.expose
    def upload(self, imgFile, fileName):
        upload_path = os.path.join(localDir, "./images")

        upload_filename = fileName

        print("\nimgFile: ", imgFile, "\nfileName: ", fileName)

        upload_file = os.path.normpath(
            os.path.join(upload_path, upload_filename))
        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = imgFile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        out = '''
        File received.
        Filename: {}
        Length: {}
        Mime-type: {}
        ''' .format(imgFile.filename, size, imgFile.content_type, data)
        return out
    
    @cherrypy.expose
    def encode(self, inputString, fileName):
        imgPath = os.path.join("images/", fileName)
        print(imgPath)
        EncodeDataIntoImage(inputString, imgPath, fileName)
        out = '''
        Image encoded.
        Filename: {}
        ''' .format(fileName)
        return out
    
    @cherrypy.expose
    def decode(self, fileName):
        imgPath = os.path.join("images/", fileName)
        print("imgPath: ", imgPath)
        return encode(DecodeDataFromImage(imgPath))
    
    
    @cherrypy.expose
    def download(self, fileName):
        path = os.path.join(absDir, './images/'+fileName)
        return serve_download(path, fileName)
    
    index_shtml = index_html = index_htm = index_php = index


if __name__=='__main__':
    location = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')  
    print( "\nstatic_dir: %s\n" % location)

    cherrypy.config.update( {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8001,
        } )
    conf = {
        '/': {  # Root folder.
            'tools.staticdir.on':   True, 
            'tools.staticdir.dir':  '',
            'tools.staticdir.root': location,
            'tools.staticdir.index': "index.html",

        }
    }

    cherrypy.quickstart(Root(), '/', config=conf)
