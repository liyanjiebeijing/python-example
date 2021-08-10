from face_utils import get_similarity
import copy
import numpy as np

class Cluster():
    def __init__(self, sim_thresh):
        self.clusters = []
        self.max_count = 3
        self.sim_thresh = sim_thresh
        assert sim_thresh > 0 and sim_thresh < 1.0, \
            "invalid similarity thresh"


    def get_max_sim_one_vs_many(self, x, cluster):
        assert len(cluster) > 0, "empty cluster"
        max_sim = 0.0
        max_id = -1
        for i, each in enumerate(cluster):
            sim = get_similarity(x, each['fea'])
            if sim > max_sim:
                max_sim = sim
                max_id = i

        return max_sim, max_id            


    def add_feature(self, fea):
        max_sim = 0.0
        max_cluster_id = -1
        for i, cluster in enumerate(self.clusters):
            sim, _ = self.get_max_sim_one_vs_many(fea, cluster)            
            if sim > max_sim:
                max_sim = sim
                max_cluster_id = i

        if max_sim > self.sim_thresh:
            self.clusters[max_cluster_id].append({'fea':fea})
            cur_cluster = self.clusters[max_cluster_id]
            if len(cur_cluster) > self.max_count: cur_cluster = cur_cluster[1:]
            return (max_cluster_id, max_sim)
        else:
            self.clusters.append([{'fea':fea}])
            return (len(self.clusters) - 1, max_sim)
            

class FastCluster():
    def __init__(self, sim_thresh):
        self.max_count = 3
        self.sim_thresh = sim_thresh
        assert sim_thresh > 0 and sim_thresh < 1.0, \
            "invalid similarity thresh"        
        self.fea_capacity = 1024
        self.fea_count = 0
        self.feature_np = np.array([])
        self.id_count = {}


    def add_feature(self, fea):
        if len(self.feature_np) == 0:
            self.max_group_id = 0
            self.kDim = len(fea)
            self.feature_np = np.zeros((self.fea_capacity, self.kDim + 1), np.float32)
            self.feature_np[self.fea_count, :-1] = fea
            self.feature_np[self.fea_count, -1] = self.max_group_id
            self.fea_count += 1
            self.id_count[self.max_group_id] = 1
            return (self.max_group_id, 0.0)
        
        cos = (fea * self.feature_np[:self.fea_count, :-1]).sum(axis=1)
        sim = (1 + cos) / 2.0
        max_sim_id = sim.argmax()
        max_sim = sim[max_sim_id]
        # print(max_sim, self.fea_count)
        
        if max_sim > self.sim_thresh:
            group_id = round(self.feature_np[max_sim_id][-1])
            start_id = sum([self.id_count[i] for i in range(group_id)])
            # print ([self.id_count[i] for i in range(group_id)])

            if self.id_count[group_id] < 3:
                feature_np = copy.deepcopy(self.feature_np)                
                feature_np[:start_id]     = self.feature_np[:start_id]
                feature_np[start_id, :-1] = fea
                feature_np[start_id, -1]  = group_id
                feature_np[start_id + 1:self.fea_count + 1] = self.feature_np[start_id:self.fea_count]
                self.feature_np = feature_np
                self.fea_count += 1
                self.id_count[group_id] += 1
            else:
                self.feature_np[start_id: start_id + 2] = self.feature_np[start_id + 1: start_id + 3]
                self.feature_np[start_id + 2, :-1] = fea
                self.feature_np[start_id + 2, -1] = group_id
            ret = group_id
        else:
            self.max_group_id += 1
            self.feature_np[self.fea_count, :-1] = fea
            self.feature_np[self.fea_count, -1] = self.max_group_id
            self.fea_count += 1
            self.id_count[self.max_group_id] = 1
            ret = self.max_group_id

        if self.fea_count >= self.fea_capacity - 1:
            self.fea_capacity *= 2
            feature_np = np.zeros((self.fea_capacity, self.kDim + 1), np.float32)
            feature_np[:self.fea_count] = self.feature_np
            self.feature_np = feature_np

        return (ret, max_sim)

