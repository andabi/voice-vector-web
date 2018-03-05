from flask import Flask
from flask import Response
from flask_compress import Compress
import os

class SecureFlask(Flask):
    def process_response(self, response):
        #Every response will be processed here first
        response.headers['server'] = 'Kakao Brain'
        super(SecureFlask, self).process_response(response)
        return(response)

app = SecureFlask(__name__)

#app.config['LOCATION_BOWER'] = "/bower_components"
#app.config['LOCATION_MEDIA'] = "/shared_media"
#app.config['LOCATION_ARTICLE'] = "/shared_article"
Compress(app)

import vvapp.views