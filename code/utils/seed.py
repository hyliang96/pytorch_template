
import torch
import numpy as np
import random
import os


def set_seed(seed=0, cudnn='normal'):
    '''
    [ 'benchmark', 'normal', 'slow', 'none' ], cudnn 随机性从左到右减小，复现接近程度增加，速度减慢
    'benchmark': 启动CUDNN_FIND自动寻找最快的操作, 若每个iteration计算图不变（即输入形状、模型不变），则加速一点；否则减速一点
    一般都写：'normal'，分类准确度从0.1%这位开始不同
    'slow'：会减慢速度，但只要gpu的数目相同，分类准确度（百分数）几乎完全一样；gpu的数目不同的话，效果稍好于'normal
    'none'：gpu和cpu运行结果一样，但速度慢
    '''

    assert type(seed) == int and seed in range(0,4294967296), "`seed` must be anint in [0,4294967295]"
    assert cudnn in [ 'benchmark', 'normal', 'none', 'slow' ], "`cudnn` must be in [ 'benchmark', 'normal', 'none', 'slow' ]"

    os.environ['PYTHONHASHSEED'] = str(seed) # seed for hash() function, affects the iteration order of dicts, sets and other mappings, str(seed) int [0; 4294967295]
    random.seed(seed) # random and transforms, seed int or float
    np.random.seed(seed) #numpy, seed int
    torch.manual_seed(seed) # cpu, seed int or float
    torch.cuda.manual_seed(seed) # gpu, seed int or float
    torch.cuda.manual_seed_all(seed) # multi-gpu, seed int or float

    if cudnn=='none':
        torch.backends.cudnn.enabled = False # if True, cudnn 加速，但结果仅接近而不全相等
    elif cudnn=='slow':
        # cuDNN在使用deterministic模式时，可能会造成计算速度下降（取决于model）
        # 不过实际上这个设置对复现的精度影响不大，仅仅是小数点后几位的差别。所以如果不是对精度要求极高，其实不太建议修改，因为会使计算效率降低。
        torch.backends.cudnn.deterministic = True  # if True, cudnn无随机性随机，cpu/gpu结果一致； 但卷积牺牲了进度
        torch.backends.cudnn.benchmark = False   # if True, 启动CUDNN_FIND自动寻找最快的操作
    elif cudnn == 'normal':
        torch.backends.cudnn.benchmark = False   # if True, 启动CUDNN_FIND自动寻找最快的操作
    elif cudnn=='benchmark':
        torch.backends.cudnn.benchmark = True    # if True, 启动CUDNN_FIND自动寻找最快的操作


def set_work_init_fn(seed):
    def worker_init_fn(worker_id):
        np.random.seed(seed  + worker_id)
    return worker_init_fn
