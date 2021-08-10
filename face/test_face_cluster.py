from face_cluster import Cluster
import os
from loguru import logger 
from tqdm import tqdm
import numpy as np
from sklearn import metrics

def test_face_cluster(kThresh):    
    # dst_dir = 'cluster_%.2f' % (kThresh)
    # if not os.path.exists(dst_dir): os.makedirs(dst_dir)

    logger.info("load features...") 
    kFeaKey = 'fea20210326'
    feature_dir = '/dev/shm/pubfig/all_feature' 
    infos = []
    name_label = {}
    for each in tqdm(os.listdir(feature_dir)[:10000]):        
        if kFeaKey not in each:
            continue

        name = each.split('-')[0]
        if name not in name_label: name_label[name] = len(name_label)

        fea_path = os.path.join(feature_dir, each)
        fea = np.load(fea_path)
        infos.append({'fea': fea, 'name': each, 'label': name_label[name]})
    logger.info("done") 

    #test cluster
    logger.info("do cluster ...") 
    face_cluster = Cluster(sim_thresh = kThresh)
    labels_true = []
    labels_pred = []
    for each in tqdm(infos):
        labels_true.append(each['label'])
        pred = face_cluster.add_feature(each['fea'])
        labels_pred.append(pred)
    logger.info("done") 

    #get cluster score
    print(f"thresh={kThresh}:")
    homogeneity_score = metrics.homogeneity_score(labels_true, labels_pred)
    print('homogeneity_score=', homogeneity_score)
    
    completeness_score = metrics.completeness_score(labels_true, labels_pred)
    print('completeness_score=', completeness_score)

    v_measure_score = metrics.v_measure_score(labels_true, labels_pred)
    print('v_measure_score=', v_measure_score)

    rand_score = metrics.rand_score(labels_true, labels_pred)
    print('rand_score=', rand_score)

    cluster_result_dir = 'cluster_result'
    if not os.path.exists(cluster_result_dir): os.makedirs(cluster_result_dir)
    with open('%s/cluster_score_%.2f\n' % (cluster_result_dir, kThresh), 'w') as f:
        f.write('homogeneity_score=%.6f\n' % (homogeneity_score))
        f.write('completeness_score=%.6f\n' % (completeness_score))
        f.write('v_measure_score=%.6f\n' % (v_measure_score))
        f.write('rand_score=%.6f\n' % (rand_score))


if __name__ == '__main__':
    test_face_cluster(0.5)
    test_face_cluster(0.6)
    test_face_cluster(0.7)
    

    

