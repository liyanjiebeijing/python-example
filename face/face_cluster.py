from face_utils import get_similarity

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

        if max_cluster_id == -1 or max_sim < self.sim_thresh:
            self.clusters.append([{'fea':fea}])
            return len(self.clusters) - 1
        else:
            self.clusters[max_cluster_id].append({'fea':fea})
            return max_cluster_id

    


