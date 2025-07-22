import cv2 as cv
import os
import matplotlib.pyplot as plt
import cherrypy
from cherrypy._json import encode
from cherrypy.lib.static import serve_download

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

def readf(filename):
    file = open(filename)
    read = file.read()
    return read

def EncodeDataIntoImage(inputString, imgPath, fullFileName, password):
    root = os.getcwd()
    imgPath = os.path.join(root, imgPath)
    print(imgPath, password)
    img = cv.imread(imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    if (password == ""):
        key = "&&&"
    else:
        key = password
    
    bitArrayString = ' '.join('{0:08b}'.format(ord(x), 'b') for x in inputString+key).replace(" ", "")    
    print(bitArrayString)

    passwordValue = PasswordValueCalculation(password, imgRGB)

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

def BitStringToString(s):
    return (int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')).decode('utf-8')

def DecodeDataFromImage(imgPath, password):
    if (password == ""):
        key = "001001100010011000100110" # binary for "&&&"
    else:
        key = StringToBinary(password)
    img = cv.imread(imgPath)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    passwordValue = PasswordValueCalculation(password, imgRGB)

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
    return BitStringToString("".join(pixelLSBValues[:len(pixelLSBValues)-len(key)])), None
    

def PasswordValueCalculation(password, imgRGB):
    passwordValue = 0
    if password == "":
        return 0
    for char in password:
        passwordValue += ord(char) 
    
    passwordValue = passwordValue%len(imgRGB) # normalize passwordValue within the bounds of image pixel length

    return passwordValue

def StringToBinary(s):
    return ''.join(format(ord(char), '08b') for char in s)

class Root:
    @cherrypy.expose
    def index(self):
        return "aaa"
    
    @cherrypy.expose
    def upload(self, imgFile, fileName, password):
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
    def encode(self, inputString, fileName, password):
        imgPath = os.path.join("images/", fileName)
        print("imgPath: ", imgPath, "password: ", password)
        EncodeDataIntoImage(inputString, imgPath, fileName, password)
        out = '''
        Image encoded.
        Filename: {}
        ''' .format(fileName)
        return out
    
    @cherrypy.expose
    def decode(self, fileName, password):
        imgPath = os.path.join("images/", fileName)
        print("imgPath: ", imgPath, "password: ", password)
        result, err = DecodeDataFromImage(imgPath, password)
        print("The result is: ", result)
        if err or result == None:
            return encode({"error": 'Wrong password!'})
        return encode(result)
    
    
    @cherrypy.expose
    def download(self, fileName):
        path = os.path.join(absDir, './images/'+fileName)
        return serve_download(path, fileName)
    
    index_shtml = index_html = index_htm = index_php = index

def CreateDirectory(directoryName):
    try:
        os.mkdir(directoryName)
        print(f"Directory '{directoryName}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directoryName}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directoryName}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__=='__main__':
    CreateDirectory("images")
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


