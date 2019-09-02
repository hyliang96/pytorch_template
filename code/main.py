#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from torch.autograd import Variable
import os
from torch.utils.tensorboard.writer import SummaryWriter

from get_data import get_data
from args import args
from get_model import State
from epoch import run_epoch
from log import Log
from tqdm import tqdm

from model import Net
from torch import optim


def main(args):
    s = State(args)
    s.log = Log(args.log_path)
    s.writer = SummaryWriter(log_dir=args.tensorboard_path)

    s.model = Net()
    s.optimizer = optim.SGD(s.model.parameters(), lr=args.lr, momentum=args.momentum)

    # s.load()
    s.deploy()

    train_loader = get_data(args, 'train')
    test_loader = get_data(args, 'test')
    
    for s.epoch in range(0, args.epochs):
        s.epoch_pbar = tqdm(bar_format='{desc}', leave=True, desc = 'Epoch {} |'.format(s.epoch))
        run_epoch('train', s, train_loader )
        run_epoch('test',  s, test_loader  )
        # s.log.tofile(s.epoch_pbar.desc)
        # close_and_leave(s.epoch_pbar)
        s.epoch_pbar.close()

    s.save()
    s.writer.close()
    s.log.close()

if __name__ == "__main__":
    main(args)
