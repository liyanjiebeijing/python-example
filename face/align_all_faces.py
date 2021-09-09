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
    req_json['face_feature_names'] = ['fea_1906'] 
    
    data=json.dumps(req_json)
        
    req = requests.post(hulk_url, data=data)
    ack_json = json.loads(req.text)
    assert ack_json['success']
    return ack_json
    

class PostThread (threading.Thread):
    def __init__(self, img_path, aligned_path):
        threading.Thread.__init__(self)
        self.img_path = img_path   
        self.aligned_path = aligned_path   

    def run(self):
        try:
            with open(self.img_path, 'rb') as f:
                image_b64 = base64.b64encode(f.read())    
                result = detect_face(image_b64)
                if len(result['faces']) == 0:
                    print(f'{self.img_path}: no face found')
                    return

            max_face = None
            max_area = 0
            for face in result['faces']:
                area = face['width'] * face['height']
                if area > max_area:
                    max_face = face
                    max_area = area

            #align face and save
            img = cv2.imread(self.img_path)
            face_img_align = align_face(img , np.array(face['5p']))
            cv2.imwrite(self.aligned_path, face_img_align)
        except Exception as e:
            print(e)


def align_face_dir(img_dir):
    img_dir = img_dir[:-1] if '/' == img_dir[-1] else img_dir
    align_dir = img_dir + '_align'
    if not os.path.exists(align_dir): os.makedirs(align_dir)

    names = os.listdir(img_dir)
    names.sort()
    threads = []
    img_count = 0
    for name in tqdm(names):
        img_count += 1
        if name[-4:] != '.jpg' and name[-4:] != '.jpeg' and name[-4:] != '.png':
            continue

        img_path = os.path.join(img_dir, name)        
        assert(os.path.exists(img_path))
        threads.append(PostThread(img_path, os.path.join(align_dir, name)))

        if len(threads) > 50:
            for each in threads:
                each.start()
            for each in threads:
                each.join()
            threads = []


    if len(threads) > 0:
        for each in threads:
            each.start()
        for each in threads:
            each.join()
        threads = []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('usage: %s <img_dir>' % (sys.argv[0]))
        sys.exit(0)

    if os.path.isdir(sys.argv[1]):
        align_face_dir(sys.argv[1])
    else:
        print('usage: %s <img_dir>')

  