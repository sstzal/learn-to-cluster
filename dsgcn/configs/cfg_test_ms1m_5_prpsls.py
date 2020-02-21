# the same result as dsgcn/configs/yaml/cfg_test_0.7_0.75.yaml
# On 1 TitanX, it takes around 2hr for testing (exclude the proposal generation)
# test on pretrained model: (pre, rec, fscore) = (94.62, 72.59, 82.15)

import os.path as osp
from proposals import generate_proposals

# model
model = dict(type='dsgcn',
             kwargs=dict(feature_dim=256,
                         featureless=False,
                         reduce_method='max',
                         hidden_dims=[512, 64]))

batch_size_per_gpu = 256

# misc
workers_per_gpu = 1

log_level = 'INFO'
log_config = dict(interval=100, hooks=[
    dict(type='TextLoggerHook'),
])

# post_process
th_pos = -1
th_iou = 1

# testing metrics
metrics = ['pairwise', 'bcubed', 'nmi']

# data locations
prefix = './data'
test_name = 'part9_test'
k = 80
knn_method = 'faiss'

step = 0.05
minsz = 3
maxsz = 300
thresholds = [0.55, 0.6, 0.65, 0.7, 0.75]

proposal_params = [
    dict(
        k=k,
        knn_method=knn_method,
        th_knn=th_knn,
        th_step=step,
        minsz=minsz,
        maxsz=maxsz,
    ) for th_knn in thresholds
]

feat_path = osp.join(prefix, 'features', '{}.bin'.format(test_name))
label_path = osp.join(prefix, 'labels', '{}.meta'.format(test_name))
proposal_path = osp.join(prefix, 'cluster_proposals')
test_data = dict(wo_weight=False,
                 feat_path=feat_path,
                 label_path=label_path,
                 proposal_folders=generate_proposals(
                     params=proposal_params,
                     prefix=prefix,
                     oprefix=proposal_path,
                     name=test_name,
                     dim=model['kwargs']['feature_dim'],
                     no_normalize=False))
