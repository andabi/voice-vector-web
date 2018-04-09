import glob, datetime, random, os, json

import numpy as np
from flask import render_template, request, jsonify

from vvapp import app
from vvapp.tf_model import request_sim

# List of Open Source
open_source_list = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../open_source.json')))


@app.route('/')
@app.route('/index')
def end_index():
    return render_template("index.html", open_source_list=open_source_list)


@app.route('/api', methods=['POST'])
def end_api():
    result_dict = {}
    
    if request.method == 'POST':
        user_file = request.files["user_wav"]
        if user_file:
            # TODO save wav to tenth or minio
            speaker_id = get_most_sim(user_file)
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


def get_most_sim(stream):
    result = request_sim(stream)
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


# def generate_random_datetime_salt():
#     rand_salt = str(random.randrange(1000000, 10000000))
#     nowdt = datetime.datetime.now()
#     nowstr = nowdt.strftime('%Y%m%d%H%M%S')
#
#     return nowstr + rand_salt