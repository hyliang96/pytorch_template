#!/usr/bin/env python
# -*- coding: utf-8 -*-
import torch
import torch.nn.functional as F
from tqdm import tqdm
import torchnet.meter as meter
from functools import wraps
import numpy as np

def detach_input(f):
    @wraps(f)
    def _f(*args, **wargs):
        args = [arg.detach() if type(arg)==torch.Tensor else arg for arg in args ]
        wargs = { key : arg.detach() if type(arg)==torch.Tensor else arg for key,arg in wargs.items() }
        return f(*args, **wargs)
    return _f

class ClassErrorMeter(meter.ClassErrorMeter):
    @detach_input
    def add(self, *args, **wargs):
        return super().add(*args, **wargs)

    def value(self, *args, **wargs):
        value = super().value(*args, **wargs)
        if type(value)==list and len(value)==1:
            return value[0]
        else:
            return value

class AverageValueMeter(meter.AverageValueMeter):
    @detach_input
    def add(self, *args, **wargs):
        return super().add(*args, **wargs)

    def value(self):
        return super().value()[0]

    # 变量 std


class ConfusionMeter(meter.ConfusionMeter):
    @detach_input
    def add(self, *args, **wargs):
        return super().add(*args, **wargs)

# def get_value_std(f):
#     @wraps(f)
#     def _value(self):
#         return f(self)[0]
#     @wraps(f)
#     def _std(self):
#         return f(self)[1]
#     return _value, _std

# meter.meter.Meter.__call__, meter.meter.Meter.std  = get_value_std(meter.meter.Meter.value)


# # def _value(self):
# #     return self.value()[0]
# # meter.meter.Meter.__call__ = _value

# # def _std(self):
# #     return self.value()[1]
# # meter.meter.Meter.std = _std

# def detach_input(f):
#     @wraps(f)
#     def _f(self, *args):
#         args = [arg.detach() if type(arg)==torch.Tensor else arg for arg in args ]
#         return f(self, *args)
#     return _f
# # meter.meter.Meter.add = detach_input(meter.meter.Meter.add)
# meter.ClassErrorMeter.add = detach_input(meter.ClassErrorMeter.add)

# def _add(self, *args):
#     args = [arg.detach() if type(arg)==torch.Tensor else arg for arg in args ]
#     return self.add(*args)
# meter.ClassErrorMeter.add = _add

# class Meter(object):



def run_epoch(stage, state, data_loader):
    """stage = 'train' or 'test' or 'val' or anything"""
    if stage=='train':
        state.model.train()
    else:
        state.model.eval()

    pbar = tqdm(initial=0, total=len(data_loader), leave=False)
    _loss = AverageValueMeter()
    _acc = ClassErrorMeter(accuracy=True)
    _conf = ConfusionMeter(k=10, normalized=True)

    for batch_idx, (data, target) in enumerate(data_loader):
        data, target = data.to(state.args.device), target.to(state.args.device)
        if stage=='train':
            state.optimizer.zero_grad()
        output = state.model(data)
        loss = F.nll_loss(output, target)
        if stage=='train':
            loss.backward()
            state.optimizer.step()

        _loss.add(loss.mean().item())
        _acc.add(output, target)
        _conf.add(output, target)

        if batch_idx % state.args.log_interval == 0:
            pbar.desc = '{:6s} Epoch {}:'.format(stage, state.epoch)
            pbar.postfix = 'Loss {:.4f} Acc {:.4f}%'.format(
                _loss.value(), _acc.value())
            pbar.update(state.args.log_interval)

    pbar.close()
    print('{:6s} Epoch {}: loss {:.4f}, Acc {:.4f}%'.format(
        stage, state.epoch, _loss.value(), _acc.value()))

    # conf = _conf.value()
    # np.array([k,k]), 纵坐标是输入，横坐标是预测
    # print(conf.sum(1)) == np.ones([k])

    # print('_conf')
    # print(_conf.value())


# def train(state, train_loader, stage='train'):
#     state.model.train()

#     pbar = tqdm(initial=0, total=len(train_loader), leave=False)
#     loss_collector = AverageValueMeter()
#     correct_collector = ClassErrorMeter(accuracy=True)
# #     confusion_collector = ConfusionMeter()

#     for batch_idx, (data, target) in enumerate(train_loader):
#         data, target = data.to(state.args.device), target.to(state.args.device)
#         state.optimizer.zero_grad()
#         output = state.model(data)
#         loss = F.nll_loss(output, target)
#         loss.backward()
#         state.optimizer.step()

#         loss_collector.add(loss.mean().item())
#         correct_collector.add(output, target)

#         if batch_idx % state.args.log_interval == 0:
#             pbar.desc = '{:6s} Epoch {}:'.format(stage, state.epoch)
#             pbar.postfix = 'Loss {:.4f} Acc {:.4f}%'.format(
#                 loss_collector.value(), correct_collector.value())
#             pbar.update(state.args.log_interval)

#     pbar.close()
#     print('{:6s} Epoch {}: loss {:.4f}, Acc {:.4f}%'.format(
#         stage, state.epoch, loss_collector.value(), correct_collector.value()))


# def test(state, test_loader, stage='test'):
#     state.model.eval()

#     pbar = tqdm(initial=0, total=len(test_loader), leave=False)
#     loss_collector = AverageValueMeter()
#     correct_collector = ClassErrorMeter(accuracy=True)

#     with torch.no_grad():
#         for batch_idx, (data, target) in enumerate(test_loader):
#             data, target = data.to(state.args.device), target.to(state.args.device)
#             output = state.model(data)
#             loss = F.nll_loss(output, target)

#             loss_collector.add(loss.mean().item())# sum up batch loss
#         #     pred = output.argmax(dim=1, keepdim=True) # get the index of the max log-probability
#             correct_collector.add(output, target)

#             if batch_idx % state.args.log_interval == 0:
#                 pbar.desc = '{:6s} Epoch {}:'.format(stage, state.epoch)
#                 pbar.postfix = 'Loss {:.4f} Acc {:.4f}%'.format(
#                     loss_collector.value(), correct_collector.value())
#                 pbar.update()

#     pbar.close()
#     print('{:6s} Epoch {}: loss {:.4f}, Acc {:.4f}%'.format(
#         stage, state.epoch, loss_collector.value(), correct_collector.value()))