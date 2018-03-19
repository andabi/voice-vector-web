# -*- coding: utf-8 -*-
#!/usr/bin/env python

import csv
import pickle
import os

speaker_list = []
img_list = os.listdir('vvapp/static/img/celeb_face')

with open('vvapp/speaker_list.csv', 'rU') as f:
    reader = csv.DictReader(f)
    for row in reader:
        speaker_list.append(row)
        name = row['full_name']
        jpg = '{}/jpg'.format(name)
        png = '{}/png'.format(name)
        if jpg in img_list:
            speaker_list['picture'] = 'jpg'
        elif png in img_list:
            speaker_list['picture'] = 'png'

print(speaker_list)

with open('vvapp/speaker_list.pkl', 'wb') as f:
    pickle.dump(speaker_list, f)