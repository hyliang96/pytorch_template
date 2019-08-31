from model import Net
import torch
from torch import nn
from torch import optim
import os
import warnings

def _state_dict(self):
    if hasattr(self, 'module'):
        return self.module.state_dict()
    else:
        return self.state_dict()
torch.nn.Module._state_dict = _state_dict

# def _save(self, save_path):
#     torch.save(self._state_dict(), save_path)
# torch.nn.Module.save = _save

# def _loadl(self, load_path, device):
#     checkpoint = torch.load(load_path, map_location=device)
#     self.load_state_dict(checkpoint)
# torch.nn.Module.load = _load






# state
#     model
#     optimizer
#     epoch
#     loss
#     args
#      

class State(object):
    def __init__(self, args):
        self.args = args

        self.model = Net()
        self.optimizer = optim.SGD(self.model.parameters(), lr=args.lr, momentum=args.momentum)
        # self.optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
        # self.loss = get_loss(args)

    def deploy(self):
        self.model = nn.DataParallel(self.model)
        self.model.to(self.args.device)

    def save(self):
        torch.save(self.model._state_dict(), self.args.save_path)

    def load(self):
        if os.path.isfile(self.args.load_path):
            checkpoint = torch.load(self.args.load_path, map_location=self.args.device)
            # print('checkpoint =', checkpoint)
            self.model.load_state_dict(checkpoint)
        else:
            warnings.warn('checkpoint path '+self.args.load_path+' not exist; go on without load it.', )

def show_para(model, optimizer):
    # Print model's state_dict
    print("Net's state_dict:")
    for param_tensor in model.state_dict():
        print(param_tensor, "\t", model.state_dict()[param_tensor].size())

    # Print optimizer's state_dict
    print("Optimizer's state_dict:")
    for var_name in optimizer.state_dict():
        print(var_name, "\t", optimizer.state_dict()[var_name])



# def get_all(args):
#     args.model = get_model(args)
#     args.optimizer = get_optimizer(args.model, args)
#     args.loss = 
#     show_para(args.model, args.optimizer)
#     # return args



