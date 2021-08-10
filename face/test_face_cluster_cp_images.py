# from face_cluster import Cluster
from face_cluster import FastCluster as Cluster
import os
from loguru import logger 
from tqdm import tqdm
import numpy as np
from sklearn import metrics
import random
import sys
import shutil


def load_features(feature_dir, feature_key):
    logger.info("load features...") 
    kFeaKey = feature_key    
    infos = [] 
    for each in os.listdir(feature_dir):
        if kFeaKey not in each:
            continue

        fea_path = os.path.join(feature_dir, each)
        fea = np.load(fea_path)
        infos.append({'fea': fea, 'name': each})

    #shuffle
    kSeed = 7
    random.seed(kSeed)
    random.shuffle(infos)
    logger.info("done") 

    return infos


def do_cluster(img_dir, infos, kThresh, feature_key):
    cluster_result_dir = f'cluster_{feature_key}'
    if not os.path.exists(cluster_result_dir): os.makedirs(cluster_result_dir)
    
    face_cluster = Cluster(sim_thresh = kThresh)
    for each in tqdm(infos):
        pred, max_sim = face_cluster.add_feature(each['fea'])
        img_name = each['name'].replace(f'.{feature_key}.npy', '')
        src_img_path = os.path.join(img_dir, img_name)
        dst_img_path = os.path.join(cluster_result_dir, '%03d_%s' % (pred, img_name))
        shutil.copyfile(src_img_path, dst_img_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} <img_dir>')
        sys.exit(0)

    img_dir = sys.argv[1]
    img_dir = img_dir[:-1] if '/' == img_dir[-1] else img_dir
    feature_dir = img_dir + '_feature'
    
    key_thresh = {'fea20210326':0.67, 'fea1906':0.78}
    for feature_key in key_thresh.keys():        
        infos = load_features(feature_dir, feature_key)
        thresh = key_thresh[feature_key]
        do_cluster(img_dir, infos, thresh, feature_key)
                
    

    

