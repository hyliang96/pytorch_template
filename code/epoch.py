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
            state.writer.add_scalar(stage+' loss-iter', loss.mean(), 
                (batch_idx + state.epoch*len(data_loader)) )
                # * data.size()[0]  )


        _loss.add(loss.mean().item())
        _acc.add(output, target)
        _conf.add(output, target)

        if batch_idx % state.args.pbar_interval == 0:
            pbar.desc = '{:6s}'.format(stage)
            pbar.postfix = 'Loss {:.4f} Acc {:.4f}%'.format(_loss.value(), _acc.value())
            pbar.update(state.args.pbar_interval)

    pbar.close()
    state.epoch_pbar.desc += ' {:6s}: loss {:.4f}, Acc {:.4f}% |'.format(stage, _loss.value(), _acc.value())
    state.epoch_pbar.update()

    if stage!='train':
        state.writer.add_scalar(stage+' avg_loss-epoch', _loss.value(), state.epoch)
        state.writer.add_scalar(stage+' avg_acc-epoch',  _acc.value(),  state.epoch)



    # conf = _conf.value()
    # np.array([k,k]), 纵坐标是输入，横坐标是预测
    # print(conf.sum(1)) == np.ones([k])

    # print('_conf')
    # print(_conf.value())

