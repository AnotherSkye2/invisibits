import cv2 as cv
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import cherrypy
import random
import string

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

    return BitStringToString("".join(pixelLSBValues[:len(pixelLSBValues)-len(key)]))

class Root:
    @cherrypy.expose
    def index(self):
        return "aaa"
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))
    
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
