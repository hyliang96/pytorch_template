#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pprint import pprint

from config import args
from get_data import get_data
from state import State
from epoch import run_epoch

from utils import *
from tqdm import tqdm
from utils.log import Log
from utils.tensorboard import Tensorboard
from utils.misc import Max, symlink_force


from model import Net
from torch import optim


def main(args):
    s = State(args)
    s.log = Log(s.args.log_path)
    s.writer = Tensorboard(s.args.tensorboard_path)

    print('----------------------------------------------------------------------------------------------')
    print('args:')
    print(s.args)
    print('----------------------------------------------------------------------------------------------')

    s.model = Net()
    s.optimizer = optim.SGD(s.model.parameters(), lr=s.args.lr, momentum=s.args.momentum)

    if args.load_path:
        s.load(s.args.load_path)
    s.deploy()

    if 'train' in s.args.phases or 'val' in s.args.phases:
        train_loader = get_data(s.args, 'train')
    if 'test'  in s.args.phases:
        test_loader  = get_data(s.args, 'test')

    if 'test' in s.args.phases:
        s.max_acc = Max()

    for s.epoch in range(s.args.start_epoch, s.args.start_epoch + s.args.n_epoch):
        s.epoch_pbar = tqdm(bar_format='{desc}', leave=True, desc = 'Epoch {} |'.format(s.epoch))
        if 'train' in s.args.phases:
            _, _   = run_epoch('train', s, train_loader )
        if 'test' in s.args.phases:
            _, acc = run_epoch('test',  s, test_loader  )
            s.max_acc.add(s.epoch, acc)
        s.epoch_pbar.close()

        if 'train' in s.args.phases and (s.epoch - s.args.start_epoch) % s.args.save_interval == 0:
            s.save( os.path.join(s.args.checkpoint_path, 'epoch_'+str(s.epoch)+'.pth') )
            if 'test' in s.args.phases:
                symlink_force('epoch_'+str(s.max_acc.key)+'.pth',
                                os.path.join(s.args.checkpoint_path, 'epoch_best.pth'))
        if not 'train' in s.args.phases:
            break

    s.writer.close()
    s.log.close()

if __name__ == "__main__":
    main(args)
