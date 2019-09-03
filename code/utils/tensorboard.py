from torch.utils.tensorboard.writer import SummaryWriter
import threading
import os

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