import cv2
import sys
import os
import time
import random
import json
import requests
import base64
from tqdm import tqdm


def decode_video(video_dir, interval_ms):
    if not os.path.exists(video_dir):
        print('not find ', video_dir)
        return

    dst_dir = video_dir + '_decode'
    if not os.path.exists(dst_dir): os.makedirs(dst_dir)

    for name in tqdm(os.listdir(video_dir)):
        if name[-4:] != '.mp4' and name[-5:] != '.mpeg':
            continue
        video_path = os.path.join(video_dir, name)

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        interval = 1000 / fps
                
        frame_index = 0
        elapse = 0
        ret = True
        while ret:
            ret, frame = cap.read()
            frame_index += 1
            elapse += interval
            if elapse < interval_ms:               
                continue

            cv2.imwrite('%s/%s_%04d.jpg' % (dst_dir, name, frame_index), frame)
            elapse = 0

    cap.release()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ('%s: usage <video_dir> <save_interval(ms)>' % (sys.argv[0]))
        sys.exit(0)

    decode_video(sys.argv[1], int(sys.argv[2]))