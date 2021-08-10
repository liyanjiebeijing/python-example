from sklearn import metrics
labels_true = [0, 0, 0, 1, 1, 1]
labels_pred = [0, 0, 1, 1, 2, 2]

# 基本用法
score = metrics.adjusted_rand_score(labels_true, labels_pred)
print(score)

# 与标签名无关
labels_pred = [1, 1, 0, 0, 3, 3]
score = metrics.adjusted_rand_score(labels_true, labels_pred)
print(score)

# 具有对称性
score = metrics.adjusted_rand_score(labels_pred, labels_true)
print(score)

# 接近 1 最好
labels_pred = labels_true[:]
score = metrics.adjusted_rand_score(labels_true, labels_pred)
print(score)

# 独立标签结果为负或者接近 0
labels_true = [0, 1, 2, 0, 3, 4, 5, 1]
labels_pred = [1, 1, 0, 0, 2, 2, 2, 2]
score = metrics.adjusted_rand_score(labels_true, labels_pred)
print(score)


labels_true = [0, 1, 2, 0, 3, 4, 5, 1]
labels_pred = [1, 1, 0, 0, 2, 2, 2, 2]
score = metrics.homogeneity_score(labels_true, labels_pred)
print('homogeneity_score=', score)

labels_true = [0, 1, 2, 0, 3, 4, 5, 1]
labels_pred = [1, 1, 0, 0, 2, 2, 2, 2]
score = metrics.completeness_score(labels_true, labels_pred)
print('completeness_score=', score)

labels_true = [0, 1, 2, 0, 3, 4, 5, 1]
labels_pred = [1, 1, 0, 0, 2, 2, 2, 2]
score = metrics.v_measure_score(labels_true, labels_pred)
print('v_measure_score=', score)

labels_true = [0, 1, 2, 0, 3, 4, 5, 1]
labels_pred = [1, 1, 0, 0, 2, 2, 2, 2]
score = metrics.rand_score(labels_true, labels_pred)
print('rand_score=', score)


