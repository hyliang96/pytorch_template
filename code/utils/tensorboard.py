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

def _add_model_graph(self, model, dummy_loader):
    dummy_input, dummy_label = dummy_loader.dataset[0]
    dummy_input_batch = dummy_input.unsqueeze_(0)
    return self.add_graph(model, (dummy_input_batch, ))
SummaryWriter.add_model_graph = _add_model_graph


from torch.utils.tensorboard.summary import hparams

def _add_hparams(self, hparam_dict={}, metric_dict={}):
    """Add a set of hyperparameters to be compared in tensorboard.

    Args:
        hparam_dict (dictionary): Each key-value pair in the dictionary is the
            name of the hyper parameter and it's corresponding value.
        metric_dict (dictionary): Each key-value pair in the dictionary is the
            name of the metric and it's corresponding value. Note that the key used
            here should be unique in the tensorboard record. Otherwise the value
            you added by `add_scalar` will be displayed in hparam plugin. In most
            cases, this is unwanted.

    Examples::

        from tensorboardX import SummaryWriter
        with SummaryWriter() as w:
            for i in range(5):
                w.add_hparams({'lr': 0.1*i, 'bsize': i},
                                {'hparam/accuracy': 10*i, 'hparam/loss': 10*i})

    Expected result:

    .. image:: _static/img/tensorboard/add_hparam.png
        :scale: 50 %
    """
    if type(hparam_dict) is not dict or type(metric_dict) is not dict:
        raise TypeError('hparam_dict and metric_dict should be dictionary.')
    exp, ssi, sei = hparams(hparam_dict, metric_dict)

    with SummaryWriter(log_dir=os.path.join(self.file_writer.get_logdir(), "hparams")) as w_hp:
        w_hp.file_writer.add_summary(exp)
        w_hp._get_file_writer().add_summary(ssi)
        w_hp._get_file_writer().add_summary(sei)
        for k, v in metric_dict.items():
            w_hp.add_scalar(k, v)

    # self._get_file_writer().add_summary(exp)
    # self._get_file_writer().add_summary(ssi)
    # self._get_file_writer().add_summary(sei)
    # for k, v in metric_dict.items():
        # self.add_scalar(k, v)

SummaryWriter.add_hparams = _add_hparams

# def _quit(signum, frame):
#     print('You choose to stop me.')
#     sys.exit()

# signal.signal(signal.SIGINT, _quit)
# signal.signal(signal.SIGTERM, _quit)
