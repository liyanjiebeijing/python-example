#! /usr/bin/python
# coding=utf-8
import sys,os
import socket
import requests
import json
import base64
import string
import traceback
import time
import cv2
import random
import datetime
import threading
import numpy as np

c=0
def detect(img_base64, detect_type):        
    # hulk_url = "http://localhost:8080/ai_detect"    
    # hulk_url = "http://10.220.193.96:80/ai_detect" #hulk inland AR3X online
    hulk_url = "http://10.220.193.97:80/ai_detect" #hulk inland AR3X test 

    req_json = {}
    req_json['img_base64'] = img_base64
    req_json['detect_type'] = detect_type
    req_json['detect_type'] = detect_type
    req_json['face_feature_names'] = ['fea_1906', 'fea_20210326']
    req_json['edge_info'] =  json.dumps({"product_key":"pk_test","device_name":"sn_test","ai_info":""})
    req_json['edge_info'] =  {"product_key":"pk_test","device_name":"sn_test","ai_info":""}
    req = requests.post(hulk_url, data=json.dumps(req_json, indent=4))
    ack_json = json.loads(req.text)
    assert ack_json['success']

    # with open('./ack_result.json', 'w') as f:
    #     f.write(json.dumps(ack_json, indent = 4))

    return ack_json

def test(image_path):                
    with open(image_path, "rb") as f:
        img_base64 = str(base64.b64encode(f.read()), encoding='utf-8')

        detect_type = 'detect_body'
        start = time.time()
        ret_info = detect(img_base64, detect_type)
        end = time.time()
        print ('----------detect %s cost %d ms' % (image_path, 1000 * (end- start)))
                
        #save result
        img = cv2.imread(image_path)  
        line_width = 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        global c
        for face in ret_info['faces']: 
            print ('pitch=%.1f, yaw=%.1f, roll=%.1f, quality=%.1f, valid=%r' % (
                        face['pitch'], face['yaw'], face['roll'], face['quality'], face['valid']))       
            color_red = (0, 0, 255)
            cv2.rectangle(img, (face["x"], face["y"]),
                            (face["x"] + face["width"], face["y"]+face["height"]), color_red, line_width)             

            for i in range(0, 5):
                center = (int(face['5p'][i][0] + 0.5), int(face['5p'][i][1] + 0.5))                
                cv2.circle(img, center, 5, (0, 255, 255), 2)
            
            for i in range(0, 95):
                center = (int(face['95p'][i][0] + 0.5), int(face['95p'][i][1] + 0.5))
                cv2.circle(img, center, 1, (0, 255, 0), -1)

        for body in ret_info['bodies']:
            roi = body['roi']
            color_blue = (255, 0, 0)
            cv2.rectangle(img, (roi[0], roi[1]),
                            (roi[0] + roi[2], roi[1] + roi[3]), color_blue, line_width)

        save_dir = 'result'
        if not os.path.exists(save_dir): os.makedirs(save_dir)
        cv2.imwrite('%s/result.jpg' % (save_dir), img)
        with open('%s/result.json' % (save_dir), 'w') as f:
            f.write(json.dumps(ret_info, indent = 4))

        print ('decode_base64_cost:', json.dumps(ret_info['decode_base64_cost'], indent = 4))
        print ('body_cost:\n', json.dumps(ret_info['body_cost'], indent = 4))
        print ('face_cost:\n', json.dumps(ret_info['face_cost'], indent = 4))


def main():
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} <img_path>')
        return
    test(sys.argv[1])

if __name__ == '__main__':
    main()
    