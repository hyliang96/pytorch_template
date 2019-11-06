
import torch
import numpy as np
import random
import os


def set_seed(seed=0, cudnn='normal'):
    assert cudnn in [ 'benchmark', 'normal', 'none', 'slow' ], "`cudnn` must be in [ 'benchmark', 'normal', 'none', 'slow' ]"

    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed) #random and transforms
    np.random.seed(seed) #numpy
    torch.manual_seed(seed) # cpu
    torch.cuda.manual_seed(seed) #gpu
    torch.cuda.manual_seed_all(seed) #multi-gpu

    if cudnn=='none':
        torch.backends.cudnn.enabled = False # if True, cudnn 加速，但结果仅接近而不全相等
    elif cudnn=='slow':
        # cuDNN在使用deterministic模式时（下面两行），可能会造成性能下降（取决于model）
        # 不过实际上这个设置对精度影响不大，仅仅是小数点后几位的差别。所以如果不是对精度要求极高，其实不太建议修改，因为会使计算效率降低。
        torch.backends.cudnn.deterministic = True  # if True, cudnn无随机性随机，cpu/gpu结果一致； 但卷积牺牲了进度
        torch.backends.cudnn.benchmark = False   # if True, 启动CUDNN_FIND自动寻找最快的操作
    elif cudnn == 'normal':
        torch.backends.cudnn.benchmark = False   # if True, 启动CUDNN_FIND自动寻找最快的操作
    elif cudnn=='benchmark':
        torch.backends.cudnn.benchmark = True  # if True, 启动CUDNN_FIND自动寻找最快的操作
#     # 若每个iteration计算图不变（即输入形状、模型不变），则加速一点；否则减速一点

def set_work_init_fn(seed):
    def worker_init_fn(worker_id):
        np.random.seed(seed  + worker_id)
    return worker_init_fn
