# -*- coding: utf-8 -*-
# @Time    : 2020-4-8 10:52:48
# @Author  : Li Yanjie

import cv2
import sys
import os
import time
import random
import json
import requests
import base64
import numpy as np
from face_utils import *
from tqdm import tqdm
import threading

import platform 
print("python vesion:", platform.python_version())
assert( platform.python_version().split('.')[0] == '3')

def detect_face(img_base64):
    hulk_url = "http://10.220.193.97:80/ai_detect" #AR3X testing environment
    req_json = {}
    req_json['img_base64'] = str(img_base64, 'utf-8')
    req_json['detect_type'] = 'detect_face'
    req_json['face_feature_names'] = ['fea_1906', 'fea_20210326' ] 
    
    data=json.dumps(req_json)
        
    req = requests.post(hulk_url, data=data)
    ack_json = json.loads(req.text)
    assert ack_json['success']
    return ack_json
    


def compare_image_face_dir(img_dir):
    names = os.listdir(img_dir)
    names.sort()
    features = []
    for name in names[:4]:
        if name[-4:] != '.jpg' and name[-4:] != '.png':
            continue

        img_path = os.path.join(img_dir, name)        
        assert(os.path.exists(img_path))
        img = cv2.imread(img_path)
        if not isinstance(img, np.ndarray):
            print('failed to load image: %s' % (name))
            continue
        
        with open(img_path, 'rb') as f:
            image_content = base64.b64encode(f.read())
            result = detect_face(image_content)

        if len(result['faces']) > 0 and result['faces'][0]['valid']:
            face = result['faces'][0]
            # if 'fea_20210326' in face: features.append((name, face['fea_20210326'], img)) 

            features.append((name, np.load(os.path.join(img_dir + '_feature', name + '.fea20210326.npy')), img))
           
    visilize_similarity(features, 'face_similarity')



class PostThread (threading.Thread):
    def __init__(self, img_b64, img_name):
        threading.Thread.__init__(self)
        self.img_b64 = img_b64
        self.img_name = img_name   
        self.result = {}

    def run(self):
        try:
            self.result = detect_face(self.img_b64)
        except Exception as e:
            print(e)


def get_face_features_dir(img_dir):
    img_dir = img_dir[:-1] if '/' == img_dir[-1] else img_dir
    feature_dir = img_dir + '_feature'
    if not os.path.exists(feature_dir): os.makedirs(feature_dir)

    names = os.listdir(img_dir)
    names.sort()
    # names = names[:32]
    threads = []
    img_count = 0
    for name in tqdm(names):
        img_count += 1
        if name[-4:] != '.jpg' and name[-4:] != '.jpeg' and name[-4:] != '.png':
            continue

        img_path = os.path.join(img_dir, name)        
        assert(os.path.exists(img_path))
        
        with open(img_path, 'rb') as f:
            image_b64 = base64.b64encode(f.read())                            
            one_thread = PostThread(image_b64, name)
            threads.append(one_thread)

        if len(threads) > 50 or img_count == len(names):
            for each in threads:
                each.start()

            for each in threads:
                each.join()

            #save features
            for thread in threads:
                if 'faces' in thread.result and len(thread.result['faces']) > 0 and \
                        thread.result['faces'][0]['valid']:
                    face = thread.result['faces'][0]
                    np.save(os.path.join(feature_dir, thread.img_name + '.fea1906.npy'), face['fea_1906'])
                    np.save(os.path.join(feature_dir, thread.img_name + '.fea20210326.npy'), face['fea_20210326'])

            threads = []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('usage: %s <img_dir|img_path>' % (sys.argv[0]))
        sys.exit(0)

    if os.path.isdir(sys.argv[1]):
        get_face_features_dir(sys.argv[1])
        # compare_image_face_dir(sys.argv[1])
    else:
        print('usage: %s <img_dir>')

  