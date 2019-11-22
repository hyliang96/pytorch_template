import torch
from torch import optim
from torch.optim import lr_scheduler
from torch import nn
import os
import errno
# import warnings
from utils import *
from utils.statistic import Statistic
from utils.log import Log
from utils.tensorboard import Tensorboard
from utils.seed import set_seed
from utils.misc import symlink_force
from utils.record import Record

# def _save(self, save_path):
#     torch.save(self._state_dict(), save_path)
# torch.nn.Module.save = _save

# def _loadl(self, load_path, device):
#     checkpoint = torch.load(load_path, map_location=device)
#     self.load_state_dict(checkpoint)
# torch.nn.Module.load = _load


class State(object):
    def __init__(self, args):
        self.args = args
        self.model = None
        self.optimizer = None
        self.scheduler = None
        self.epoch = 0

        # s = State(args)
        set_seed(self.args.seed, self.args.cudnn_behavoir)
        self.log = Log(self.args.log_path)
        self.writer = Tensorboard(self.args.tensorboard_path)
        self.stati  = Statistic(self.args.expernameid, self.args.experid_path, self.args.root_path)
        self.stati.add('hparam', self.args.dict())
        # s.writer.add_hparams(hparam_dict=s.args.dict(), metric_dict={})
        self.record = Record()

    def show_args(self):
        print('----------------------------------------------------------------------------------------------')
        print('args:')
        print(self.args)
        print('----------------------------------------------------------------------------------------------')


    def close(self):
        self.stati.close()
        self.log.close()

    def exit(self):
        self.writer.close()

    def save(self, dir_path, filename, last_epoch=None, best_epoch=None):
        checkpoint = {
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            'scheduler': self.scheduler.state_dict(),
            'record': self.record,
            'epoch': self.epoch
        }
        torch.save(checkpoint, os.path.join(dir_path, filename))

        if last_epoch:
            symlink_force('epoch_' + str(last_epoch) + '.pth', os.path.join(dir_path, 'epoch_last.pth'))

        if best_epoch:
            symlink_force('epoch_' + str(best_epoch) + '.pth', os.path.join(dir_path, 'epoch_best.pth'))

    def load(self, path):
        if os.path.isfile(path):
            checkpoint = torch.load(path, map_location=self.args.device)
            assert self.model, 'self.model is not defined before laoding a checkpoint'
            self.model.load_state_dict(checkpoint['model'])
            if self.optimizer: self.optimizer.load_state_dict(checkpoint['optimizer'])
            if self.scheduler: self.scheduler.load_state_dict(checkpoint['scheduler'])
            self.record = checkpoint['record']
            # checkpoint['epoch']
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
            # warnings.warn('checkpoint path '+path+' not exist; go on without load it.')

    def deploy(self):
        self.model = nn.DataParallel(self.model)
        self.model.to(self.args.device)
        if self.optimizer: self.optimizer.to(self.args.device)
        # if self.scheduler: self.scheduler.to(self.args.device)

    def show_para(self):
        # Print model'self state_dict
        print("Net's state_dict:")
        for param_tensor in self.model.state_dict():
            print(param_tensor, "\t", self.model.state_dict()[param_tensor].size())

        # Print optimizer's state_dict
        print("Optimizer's state_dict:")
        for var_name in self.optimizer.state_dict():
            print(var_name, "\t", self.optimizer.state_dict()[var_name])



# def get_all(args):
#     args.model = get_model(args)
#     args.optimizer = get_optimizer(args.model, args)
#     args.loss =
#     show_para(args.model, args.optimizer)
#     # return args



