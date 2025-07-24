import os
import cherrypy
import utils
from cherrypy.lib.static import serve_download
from handlers import encodeHandler, uploadHandler, decodeHandler

localDir = os.path.dirname(__file__)
absDir = os.getcwd()
imgDir = os.path.join(absDir, "images")

class Root:
    @cherrypy.expose
    def index(self):
        return "aaa"
    
    @cherrypy.expose  
    def upload(self, imgFile, fileName, password):
        return uploadHandler(self, imgFile, fileName, imgDir)
    
    @cherrypy.expose
    def encode(self, inputString, fileName, password):
        return encodeHandler(self, inputString, fileName, password, imgDir)

    @cherrypy.expose
    def decode(self, fileName, password):

        return decodeHandler(self, fileName, password, imgDir)
    
    @cherrypy.expose
    def download(self, fileName):
        path = os.path.join(absDir, './images/'+fileName)
        return serve_download(path, fileName)
    
    index_shtml = index_html = index_htm = index_php = index

if __name__=='__main__':
    utils.createDirectory("images")
    location = os.path.join(absDir, 'static')  
    print( "\nstatic_dir: %s\n" % location)
    print("localDir, absDir, imgDir: ", localDir, absDir, imgDir)

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


