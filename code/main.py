#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from args import args
from get_data import get_data
from state import State
from epoch import run_epoch

from utils import *
from tqdm import tqdm
from utils.log import Log
from utils.tensorboard import Tensorboard

from model import Net
from torch import optim


def main(args):
    s = State(args)
    s.log = Log(args.log_path)
    s.writer = Tensorboard(s.args.tensorboard_path)

    s.model = Net()
    s.optimizer = optim.SGD(s.model.parameters(), lr=args.lr, momentum=args.momentum)

    s.load()
    s.deploy()

    train_loader = get_data(args, 'train')
    test_loader = get_data(args, 'test')

    for s.epoch in range(0, args.epochs):
        s.epoch_pbar = tqdm(bar_format='{desc}', leave=True, desc = 'Epoch {} |'.format(s.epoch))
        run_epoch('train', s, train_loader )
        run_epoch('test',  s, test_loader  )
        s.epoch_pbar.close()
        # compare which is the best and save the best as a link
        s.save( os.path.join(s.args.checkpoint_path, str(s.epoch)+'.pth') )

    s.writer.close()
    s.log.close()

if __name__ == "__main__":
    main(args)
