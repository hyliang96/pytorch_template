#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from pprint import pprint

from dataloader import DataLoaders
from state import State
from epoch import run_epoch

import time
from tqdm import tqdm
from utils import patch
from utils.record import Record

from utils.misc import Max, symlink_force


from model import Net
from torch import optim
from torch.optim import lr_scheduler


def main(s):
    s.model = Net()
    s.optimizer = optim.SGD(s.model.parameters(), lr=s.args.lr, momentum=s.args.momentum)
    milestones  = [5, 10, 15, 20,40, 50]
    s.scheduler = lr_scheduler.MultiStepLR(s.optimizer, milestones, gamma=0.1)
    # lr_scheduler.ReduceLROnPlateau(s.optimizer, mode='min', factor=0.1, patience=10, verbose=False)

    if args.load_path:
        s.load(s.args.load_path)

    loaders = DataLoaders(s.args)
    s.writer.add_model_graph(s.model, loaders['dummy'])

    s.deploy()

    record_phase = [phase for phase in ['val', 'test'] if phase in s.args.phases][0]

    for s.epoch in range(s.args.start_epoch, s.args.end_epoch + 1):
        s.epoch_pbar = tqdm(bar_format='{desc}', leave=True, desc='{} | Epoch {} |'.
            format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), s.epoch))
        for phase in s.args.phases:
            results = run_epoch(phase, s, loaders[phase])
            s.record.add_phase(phase, results, s.epoch)
        s.epoch_pbar.close()

        best_dict, best_epoch = s.record.best(record_phase, 'acc')
        last_dict, last_epoch = s.record.last()
        wargs = {'last_epoch': last_epoch, 'best_epoch': best_epoch}

        s.stati.add('metric', best_dict)

        if 'train' in s.args.phases and (s.epoch - s.args.start_epoch) % s.args.save_interval == 0:
            s.save(s.args.checkpoint_path, 'epoch_' + str(s.epoch) + '.pth', **wargs)

        if not 'train' in s.args.phases:
            break

    # s.writer.add_hparams(hparam_dict={}, metric_dict={'test_acc':s.best.value})
    # s.writer.add_hparams(hparam_dict=s.args.dict(), metric_dict={'best_test_acc':s.best.value})


if __name__ == "__main__":
    from config import args
    s = State(args)
    s.show_args()

    try:
        main(s)
        s.close()
    except KeyboardInterrupt:
        s.close()
        s.exit()
    else:
        try:
            print('ctrl+c to close tensorboard server')
            while True: input()
        except KeyboardInterrupt:
            s.exit()





