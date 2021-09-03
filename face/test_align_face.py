# -*- coding: utf-8 -*-
# @Time    : 2021-9-3 14:41:00
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
from get_face_features import detect_face
from face_utils import align_face


def align_max_face(img_path):
    with open(img_path, 'rb') as f:
        image_content = base64.b64encode(f.read())
        result = detect_face(image_content)
        assert(result['success'])
    
    if len(result['faces']) == 0: 
        print(f'{img_path}: no face found')
        return

    #find max face
    max_face = None
    max_area = 0
    for face in result['faces']:
        area = face['width'] * face['height']
        if area > max_area:
            max_face = face
            max_area = area

    #align face and save
    img = cv2.imread(img_path)
    face_img_align = align_face(img , np.array(face['5p']))
    cv2.imwrite(img_path + '.align.jpg', face_img_align)

    
def main():
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} <img_path>')
        return

    align_max_face(sys.argv[1])    


if __name__ == '__main__':
    main()
    
