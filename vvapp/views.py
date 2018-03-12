from vvapp import app
from flask import render_template, redirect, abort, url_for, json, request, send_from_directory, jsonify

import os, requests, time, pickle

from vvapp.tf_model import do_inference
import numpy as np

# index
@app.route('/')
@app.route('/index')
def end_index():
    #return "Hello, Voice Vector!"
    return render_template("index.html")


@app.route('/process')
def api_process():
#    result = do_inference('avin_voice.wav')
    result = do_inference('zeze_voice.wav')

    response = np.array(result.outputs['prob'].float_val)
    top3 = np.argsort(response)[::-1][:3]
    
    #max_prob = np.max(response)
    #speaker_id = np.argmax(response)
    #print('{}: {}'.format(speaker_id, max_prob))
    
    return jsonify(top3.tolist())