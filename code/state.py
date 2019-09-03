import torch
from torch import nn
import os
import errno
# import warnings
from utils import *


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
        self.model = nn.Module()
        self.optimizer = nn.Module()

    def save(self, path):
        state_dict = {
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict()
        }
        torch.save(state_dict, path)

    def load(self, path):
        if os.path.isfile(path):
            state_dict = torch.load(path, map_location=self.args.device)
            # print('checkpoint =', checkpoint)
            self.model.load_state_dict(state_dict['model'])
            self.optimizer.load_state_dict(state_dict['optimizer'])
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
            # warnings.warn('checkpoint path '+path+' not exist; go on without load it.')

    def deploy(self):
        self.model = nn.DataParallel(self.model)
        self.model.to(self.args.device)

        self.optimizer.to(self.args.device)


    def show_para(self):
        # Print model's state_dict
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



