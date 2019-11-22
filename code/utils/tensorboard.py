# tensorboard<2.0 加载时会报如下警告，其余tensorboard>=2.0不会
    # /home/haoyu/ENV/localENV/anaconda3/lib/python3.7/site-packages/tensorboard/compat/tensorflow_stub/dtypes.py:541:
    # FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy,
    # it will be understood as (type, (1,)) / '(1,)type'.
# 如此以在加载tensorboard时暂时关闭之
__import__('warnings').filterwarnings('ignore',category=FutureWarning)
from torch.utils.tensorboard.writer import SummaryWriter
__import__('warnings').filterwarnings('default',category=FutureWarning)

from .thread import StoppableThread
import subprocess
import os
import re
# def Tensorboard(log_dir):
#     def _launch_tensorboard(log_dir, output=None):
#         output = output or os.path.join(log_dir, 'tensorboard_output')
#         os.system('tensorboard --logdir={:s} >> {:s} 2>&1'.format(log_dir, output))
#     def launch_tensorboard(log_dir):
#         p = threading.Thread(target=_launch_tensorboard, args=(log_dir,))
#         # p.daemon = True
#         p.start()
#         return p
#     p = launch_tensorboard(log_dir)
#     writer = SummaryWriter(log_dir=log_dir)
#     return writer

class Tensorboard(SummaryWriter):
    def __init__(self, log_dir, **wagrs):
        # def _launch_tensorboard(log_dir, output=None):
        #     output = output or os.path.join(log_dir, 'tensorboard_output')
        #     os.system('tensorboard --logdir={:s} >> {:s} 2>&1'.format(log_dir, output))
        tb_output = os.path.join(log_dir, 'tensorboard_output')

        def _launch_tensorboard(log_dir, output='/dev/null'):
            outputf = open(output, 'w')
            subprocess.Popen(['tensorboard', '--logdir={:s}'.format(log_dir)],
                            stdout=outputf,
                            stderr=outputf,
                            universal_newlines=True)

        # def _launch_tensorboard(log_dir, output=None):
        #     print('hello')

        def launch_tensorboard(log_dir):
            # p = Thread(target=_launch_tensorboard, args=(log_dir,))
            # p = threading.Thread(target=_launch_tensorboard, args=(log_dir,))
            p = StoppableThread(target=_launch_tensorboard, args=(log_dir, tb_output))
            # p.daemon = True
            p.start()
            return p
        self.p = launch_tensorboard(log_dir)
        super().__init__(log_dir=log_dir, **wagrs)


        print('TensorBoard:')
        get = False
        while not get:
            with open(tb_output, 'r') as f:
                for line in f:
                    if re.match('TensorBoard [0-9.]+ at', line) or re.match('port', line):
                        print(line, end='')
                        get = True
                        break
        # writer = SummaryWriter(log_dir=log_dir)
    def close(self):
        self.p.stop()
        # self.p.terminate()

        self.p.join()
        super().close()

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


import matplotlib.pyplot as plt
from .heatmap import heatmap, annotate_heatmap

def _add_heatmap(self, tag, matrix, epoch, y_title=None, x_title=None, cmap="YlGn", cbarlabel=None):
    # 若用于画混淆矩阵，则
    # input： y轴，   y_title = [类1名,类2名,...]
    # output：x轴，   x_title = [类1名,类2名,...]
    # 绘制热度图，有横纵标签、标度
    if cbarlabel == None:
        cbarlabel = tag
    fig, ax = plt.subplots()
    im, cbar = heatmap(matrix, ax, y_title, x_title, cmap=cmap, cbarlabel=cbarlabel)
    # texts = annotate_heatmap(im, valfmt="{x:.3f}")
    self.add_figure(tag, fig, epoch)
SummaryWriter.add_heatmap = _add_heatmap

# import numpy as np
# import itertools
# import matplotlib.pyplot as plt


# # 原文链接：https://blog.csdn.net/qq_32425195/article/details/101537049
# def plot_confusion_matrix(cm, classes,
#                           normalize=False,
#                           title='Confusion matrix',
#                           cmap=plt.cm.Blues):
#     """
#     This function prints and plots the confusion matrix.
#     Normalization can be applied by setting `normalize=True`.
#     """
#     if normalize:
#         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
#         print("Normalized confusion matrix")
#     else:
#         print('Confusion matrix, without normalization')

#     print(cm)

#     fig = plt.figure()


#     plt.imshow(cm, interpolation='nearest', cmap=cmap)
#     plt.title(title)
#     plt.colorbar()
#     tick_marks = np.arange(len(classes))
#     plt.xticks(tick_marks, classes, rotation=45)
#     plt.yticks(tick_marks, classes)

#     fmt = '.2f' if normalize else 'd'
#     thresh = cm.max() / 2.
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(j, i, format(cm[i, j], fmt),
#                  horizontalalignment="center",
#                  color="white" if cm[i, j] > thresh else "black")

#     plt.tight_layout()
#     plt.ylabel('True label')
#     plt.xlabel('Predicted label')
#     return fig

# # cnf_matrix = np.array([
# #     [4101, 2, 5, 24, 0],
# #     [50, 3930, 6, 14, 5],
# #     [29, 3, 3973, 4, 0],
# #     [45, 7, 1, 3878, 119],
# #     [31, 1, 8, 28, 3936],
# # ])

# # class_names = ['Buildings', 'Farmland', 'Greenbelt', 'Wasteland', 'Water']

# #调用add_figure将figure放入tensorboardX中显示
# writer.add_figure('confusion matrix',figure=plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=False,title='Normalized confusion matrix'),global_step=1)
# writer.add_figure('confusion matrix',figure=plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,title='Normalized confusion matrix'),global_step=1)


