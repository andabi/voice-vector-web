from vvapp import app
from flask import render_template, redirect, abort, url_for, json, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

import os, requests, time, pickle, random, datetime

from vvapp.tf_model import do_inference
import numpy as np
import glob


def tf_inf(filename):
    result = do_inference(filename)
    response = np.array(result.outputs['prob'].float_val)
    top_index = np.argmax(response)
    return top_index
    

def yt_url(vid, start):
    '''
    :param vid: video id
    :param start: start time in sec
    :return: youtube video link
    '''
    return 'https://www.youtube.com/watch?v={}&start={}'.format(vid, start)


def get_yt_params(speaker_name, n_video=2):
    params = []
    for file in glob.glob('vvapp/video_urls/{}/*.txt'.format(speaker_name)):
        with open(file, 'r') as f:
            lines = f.readlines()
            vid = lines[1].split('\t')[1].strip().replace('\n', '')
            s_time = int(float(lines[5].split(' ')[1]))
            params.append((vid, s_time))
    return params[:n_video]


def generate_random_datetime_salt():
    rand_salt = str(random.randrange(1000000,10000000))
    nowdt = datetime.datetime.now()
    nowstr = nowdt.strftime('%Y%m%d%H%M%S')

    return nowstr + rand_salt


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
        #print(user_file)
        if user_file:
            #file_name = secure_filename(user_file.filename)
            #file_name = os.path.join('voice_file', file_name)
            #print(file_name)
            file_name = os.path.join('voice_file', generate_random_datetime_salt()+".wav")
            user_file.save(file_name)

            speaker_id = tf_inf(file_name)
            speaker_meta = app.config['SPEAKER_META'][speaker_id]

            # append youtube video links
            params = get_yt_params(speaker_meta['full_name'])
            speaker_meta['yt_params'] = params

            result_dict = speaker_meta.copy()
            result_dict['success'] = 1

        else:
            result_dict['success'] = 0
    else:
        result_dict['success'] = 0
            
    return jsonify(result_dict)