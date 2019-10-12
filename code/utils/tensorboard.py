# tensorboard<2.0 加载时会报如下警告，其余tensorboard>=2.0不会
    # /home/haoyu/ENV/localENV/anaconda3/lib/python3.7/site-packages/tensorboard/compat/tensorflow_stub/dtypes.py:541:
    # FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy,
    # it will be understood as (type, (1,)) / '(1,)type'.
# 如此以在加载tensorboard时暂时关闭之
__import__('warnings').filterwarnings('ignore',category=FutureWarning)
from torch.utils.tensorboard.writer import SummaryWriter
__import__('warnings').filterwarnings('default',category=FutureWarning)

import threading
import os, sys, signal

def Tensorboard(log_dir):
    def _launch_tensorboard(log_dir, output=None):
        output = output or os.path.join(log_dir, 'tensorboard_output')
        os.system('tensorboard --logdir={:s} >> {:s} 2>&1'.format(log_dir, output))
    def launch_tensorboard(log_dir):
        p = threading.Thread(target=_launch_tensorboard, args=(log_dir,))
        # p.daemon = True
        p.start()
        return p
    p = launch_tensorboard(log_dir)
    writer = SummaryWriter(log_dir=log_dir)
    return writer

# def _quit(signum, frame):
#     print('You choose to stop me.')
#     sys.exit()

# signal.signal(signal.SIGINT, _quit)
# signal.signal(signal.SIGTERM, _quit)