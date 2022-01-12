#! /usr/bin/python

# coding=utf-8

import sys,os


import base64
import socket
import requests
import json
import base64
import string
import traceback
import time
import base64
import cv2
import random
import datetime
import threading
import numpy as np

g_use_url = False
img_ip_port = 'dlgpu1.ai.bjmd.qihoo.net:8002'


def detect(img_base64):
    # IP_port = "10.202.209.15:80" #indoor online
    IP_port = "10.217.36.98:80" #outdoor online
    
    hulk_url = "http://%s/v1/models/person/versions/2:detect"  % (IP_port)


    req_json = {'qid': 'lhc-test',
            'model': 'D177',
            'sn': 'lhc-test',
            'id': str(time.time()) + str(random.random()),
            'img_b64': img_base64}

    try:
        r = requests.post(url=hulk_url, data=json.dumps(req_json))  # 发起请求
        ack_json = json.loads(r.text)
        return ack_json
    except:        
        traceback.print_exc()
        return None
        

def test(image_path):                

    with open(image_path, "rb") as f:
        img_base64 = str(base64.b64encode(f.read()), 'utf-8')
        
        start = time.time()
        ret_info = detect(img_base64)
        end = time.time()        
        print ('cost %.1f ms: ' % (1000 * (end- start)) + str(ret_info))
        
        img = cv2.imread(image_path)  
        line_width = 3

        if 'human_rect' in ret_info['task_results']['data']:
            for roi in ret_info['task_results']['data']['human_rect']:
                color_blue = (255, 0, 0)
                cv2.rectangle(img, (roi[0], roi[1]),
                                (roi[2], roi[3]), color_blue, line_width)

        cv2.imwrite(image_path + '_result.jpg', img)
        with open(image_path + '_result.json', 'w') as f:
            f.write(json.dumps(ret_info, indent = 4))


def main():
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} <img_path>')
        return
    test(sys.argv[1])


if __name__ == '__main__':
    main()