# -*- coding: utf-8 -*-
#!/usr/bin/env python

import csv
import pickle
import os

speaker_dict = {}
img_list = os.listdir('vvapp/static/img/celeb_face')

with open('vvapp/speaker_list.csv', 'rU') as f:
    reader = csv.DictReader(f)
    for meta in reader:
        name = meta['full_name']
        jpg = '{}.jpg'.format(name)
        png = '{}.png'.format(name)
        if jpg in img_list:
            meta['picture'] = 'jpg'
        elif png in img_list:
            meta['picture'] = 'png'
        index = int(meta['index'])
        speaker_dict[index] = meta

with open('vvapp/speaker_list.pkl', 'wb') as f:
    pickle.dump(speaker_dict, f)