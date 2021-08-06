import os
import threading
import time
import json
import numpy as np
import requests
import hashlib
import cv2
import sys


def parse_txt(txt_path):
    img_info_list = []
    with open(txt_path) as f:
        for each in f:
            if each.strip() == '' or each[0] =='#':
                continue
            strs = each.split('\t')
            # print(each, strs)
            item = {'name':strs[0], 'id':int(strs[1]), 'url': strs[2], 'md5':strs[4]}
            item['rect'] = []
            for each in strs[3].split(','):
                item['rect'].append(int(each))
            img_info_list.append(item)

    return img_info_list


def crop_image(img, rect, kPadRatio):
    
    face_w, face_h = rect[2] - rect[0] + 1, rect[3] - rect[1] + 1
    pad_w = int(face_w * kPadRatio)
    pad_h = int(face_h * kPadRatio)
    face_img = np.zeros((face_h + pad_h * 2, face_w + pad_w * 2, 3), np.uint8)
    left = max(rect[0] - pad_w, 0)
    top =  max(rect[1] - pad_h, 0)
    right = min(rect[2] + pad_w, img.shape[1])
    bottom = min(rect[3] + pad_h, img.shape[0])
    return img[top: bottom, left: right]


def download(url, file_path, md5, rect):
    try:
        file_data = requests.get(url, allow_redirects=True, timeout=5).content
        # actual_md5 = hashlib.md5(file_data).hexdigest()
        # if actual_md5 != md5:
        #     return 'bad md5'
        kPadRatio = 0.5
        img_array = np.frombuffer(file_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if not isinstance(img, np.ndarray):
            return 'invalid image'

        img = crop_image(img, rect, kPadRatio)
        cv2.imwrite(file_path, img)
        return 'success'

        with open(file_path, 'wb') as f:  
            f.write(file_data)     
        return 'success'

    except Exception as e:
        return str(e)


class DownloadThread (threading.Thread):
    def __init__(self, threadID, img_urls, img_pathes, md5s, rects):
        threading.Thread.__init__(self)
        assert(len(img_urls) == len(img_pathes))
        self.threadID = threadID
        self.img_urls = img_urls
        self.img_pathes = img_pathes
        self.md5s = md5s
        self.rects = rects
        self.result = []
        self.cost  = 0

    def run(self):
        start = time.time()
        for i in range(len(self.img_urls)):
            img_url = self.img_urls[i]
            img_path = self.img_pathes[i]     
            md5 = self.md5s[i] 
            rect = self.rects[i] 
            ret = download(img_url, img_path, md5, rect)            
            self.result.append(ret)
        self.cost = time.time() - start


def download_all(img_infos, img_dir):
    if not os.path.exists(img_dir): os.makedirs(img_dir)

    download_path = 'download_info.log'
    with open(download_path, 'w') as f: 
        pass

    count = 0
    thread_count = 1000
    max_count = len(img_infos)    
    while count < max_count:
        # create threads                
        threads = []
        for i in range(count, min(count + thread_count, max_count)):
            img_info = img_infos[count + i]
            img_id = '%05d' % (img_info['id'])
            urls = [img_info['url']]
            imgs = [f"{img_dir}/{img_info['name']}-{img_id}.jpg"]
            md5s = [img_info['md5']]
            rects = [img_info['rect']]
            one_thread = DownloadThread(i, urls, imgs, md5s, rects)
            threads.append(one_thread)
        
        start = time.time()

        # start threads
        for each in threads:
            each.start()

        # wait finish
        for each in threads:
            each.join()

        total_cost = time.time() - start

        #show result
        costs = []
        for each in threads:                        
            costs.append(each.cost)

        with open(download_path, 'w') as f: 
            for i, each in enumerate(threads):
                img_info = img_infos[count + i]
                log = "%s-%05d:%s" % (img_info['name'], img_info['id'], each.result[0])
                f.write(log + '\n')
                    
        count += thread_count
        print('%05d/%d download cost: mean=%.3fs, max=%.3fs, min=%.3fs,' %(count, max_count,
                np.mean(costs), np.max(costs), np.min(costs)))

        break

        

def main(save_dir):
    image_infos = parse_txt('pubfig/dev_urls.txt')
    download_all(image_infos, save_dir)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} <save_dir>')
        sys.exit(0)
    main(sys.argv[1])