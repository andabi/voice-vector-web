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

#app = SecureFlask(__name__)
app = Flask(__name__)

app.config['TF_SERVER_HOST'] = 'csi-cluster-gpu23.dakao.io'
app.config['TF_SERVER_PORT'] = '1027'
Compress(app)

import vvapp.views