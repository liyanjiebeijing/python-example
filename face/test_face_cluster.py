# from face_cluster import Cluster
from face_cluster import FastCluster as Cluster
import os
from loguru import logger 
from tqdm import tqdm
import numpy as np
from sklearn import metrics
import random

def load_features(feature_key):
    logger.info("load features...") 
    kFeaKey = feature_key
    feature_dir = '/dev/shm/pubfig/all_feature' 
    infos = []
    name_label = {}    
    for each in tqdm(os.listdir(feature_dir)):
    # for each in tqdm(os.listdir(feature_dir)[:10000]):
        if kFeaKey not in each:
            continue

        name = each.split('-')[0]
        if name not in name_label: name_label[name] = len(name_label)

        fea_path = os.path.join(feature_dir, each)
        fea = np.load(fea_path)
        infos.append({'fea': fea, 'name': each, 'label': name_label[name]})    

    #shuffle
    kSeed = 7
    random.seed(kSeed)
    random.shuffle(infos)
    logger.info("done") 

    return name_label, infos


def test_face_cluster(name_label, infos, kThresh, feature_key):
    logger.info("do cluster ...") 
    face_cluster = Cluster(sim_thresh = kThresh)
    labels_true = []
    labels_pred = []
    for each in tqdm(infos):
        labels_true.append(each['label'])
        pred, max_sim = face_cluster.add_feature(each['fea'])
        # print(each['label'], pred, max_sim)
        labels_pred.append(pred)
    logger.info("done") 

    #get cluster score
    print(f"thresh={kThresh}, person_count={len(name_label)}:")
    homogeneity_score = metrics.homogeneity_score(labels_true, labels_pred)
    print('homogeneity_score=', homogeneity_score)
    
    completeness_score = metrics.completeness_score(labels_true, labels_pred)
    print('completeness_score=', completeness_score)

    v_measure_score = metrics.v_measure_score(labels_true, labels_pred)
    print('v_measure_score=', v_measure_score)

    rand_score = metrics.rand_score(labels_true, labels_pred)
    print('rand_score=', rand_score)

    # cluster_result_dir = 'cluster_result'
    # if not os.path.exists(cluster_result_dir): os.makedirs(cluster_result_dir)
    # with open('%s/cluster_score_%.2f\n' % (cluster_result_dir, kThresh), 'w') as f:
    #     f.write('person_count=%d\n' % (len(name_label)))
    #     f.write('homogeneity_score=%.6f\n' % (homogeneity_score))
    #     f.write('completeness_score=%.6f\n' % (completeness_score))
    #     f.write('v_measure_score=%.6f\n' % (v_measure_score))
    #     f.write('rand_score=%.6f\n' % (rand_score))

    return (len(name_label),  homogeneity_score, completeness_score, v_measure_score, rand_score)


if __name__ == '__main__':    
    cluster_result_dir = 'cluster_result'
    if not os.path.exists(cluster_result_dir): os.makedirs(cluster_result_dir)
    with open('cluster_result/cluster_compare.txt', 'w') as f:
        f.write("feature_key\tthresh\tperson_count\thomogeneity_score\tcompleteness_score\tv_measure_score\trand_score\n")
        for feature_key in ['fea20210326', 'fea1906']:        
            name_label, infos = load_features(feature_key)
            for thresh in [0.5, 0.55, 0.65, 0.7, 0.75, 0.8]:        
                person_count, homogeneity_score, completeness_score, v_measure_score, rand_score = \
                    test_face_cluster(name_label, infos, thresh, feature_key)
                f.write(f"{feature_key}\t{thresh}\t{person_count}\t{homogeneity_score}\t{completeness_score}\t{v_measure_score}\t{rand_score}\n")
    

    

