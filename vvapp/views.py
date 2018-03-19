from vvapp import app
from flask import render_template, redirect, abort, url_for, json, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

import os, requests, time, pickle

from vvapp.tf_model import do_inference
import numpy as np


def tf_inf(filename):
    result = do_inference(filename)
    response = np.array(result.outputs['prob'].float_val)
    top_index = np.argmax(response)
    return top_index
    

# index
@app.route('/')
@app.route('/index')
def end_index():
    #return "Hello, Voice Vector!"
    return render_template("index.html")


@app.route('/process')
def api_process():
    avin_top3 = tf_inf(os.path.join('voice_file','avin_voice.wav'))
    return jsonify(avin_top3.tolist())


@app.route('/api', methods=['POST'])
def end_api():
    result_dict = {}
    
    if request.method == 'POST':
        user_file = request.files["user_wav"]
        if user_file:
            file_name = secure_filename(user_file.filename)
            file_name = os.path.join('voice_file', file_name)
            user_file.save(file_name)

            result = tf_inf(file_name)

            speaker_meta = app.config['SPEAKER_META'][result]
            print(speaker_meta)
            result_dict = speaker_meta.copy()
            result_dict['success'] = 1

        else:
            result_dict['success'] = 0
    else:
        result_dict['success'] = 0
            
    return jsonify(result_dict)