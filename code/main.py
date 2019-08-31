#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from torch.autograd import Variable
import os

from get_data import get_data
from args import args
from get_model import State
from epoch import run_epoch

def main(args):
    train_loader = get_data(args, 'train')
    test_loader = get_data(args, 'test')

    s = State(args)
    # s.load()
    s.deploy()
    
    # for data, target in dataloader:
    #     input_var = data.to(args.device)
    #     output = s.model(input_var)
    #     print("Outside: input size", input_var.size(),
    #         "args.output_size", output.size())

    for s.epoch in range(0, args.epochs):
        run_epoch('train', s, train_loader )
        run_epoch('test',  s, test_loader  )
        # train(args, s.model, s.args.device, train_loader, s.optimizer, epoch)
        # test(args, s.model, s.args.device, test_loader, epoch)

    s.save()

if __name__ == "__main__":
    main(args)
