from flask import Flask
from flask import Response
from flask_compress import Compress
import os
import pickle


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

with open('vvapp/speaker_list.pkl', 'rb') as f:
    app.config['SPEAKER_META'] = pickle.load(f)

# Initial warm-up for tf-model
from vvapp.tf_model import do_inference
result = do_inference(os.path.join('voice_file','zeze_voice.wav'))
print("warmed up!")

import vvapp.views