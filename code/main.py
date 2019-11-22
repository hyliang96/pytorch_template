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
    if s.args.load_path and not s.args.continue_epoch: s.load(s.args.load_path)
    s.optimizer = optim.SGD(s.model.parameters(), lr=s.args.lr, momentum=s.args.momentum)
    s.scheduler = lr_scheduler.MultiStepLR(s.optimizer, [5, 10, 15, 20,40, 50], gamma=0.1)
    # lr_scheduler.ReduceLROnPlateau(s.optimizer, mode='min', factor=0.1, patience=10, verbose=False)
    if s.args.load_path and s.args.continue_epoch:     s.load(s.args.load_path)


    loaders = DataLoaders(s.args)

    s.writer.add_model_graph(s.model, loaders['dummy'])

    s.deploy()

    for s.epoch in range(s.args.start_epoch, s.args.end_epoch + 1):
        # run an epoch
        s.epoch_pbar = tqdm(bar_format='{desc}', leave=True, desc='{} | Epoch {} |'.
            format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), s.epoch))
        for phase in s.args.phases:
            results = run_epoch(phase, s, loaders[phase])
            s.record.add_phase(phase, results, s.epoch)
        s.epoch_pbar.close()

        # record metrics to statistics
        record_phase = [phase for phase in ['val', 'test'] if phase in s.args.phases]
        if record_phase != []:
            record_phase = record_phase[0]
            best_dict, best_epoch = s.record.best(record_phase, 'acc')
            last_dict, last_epoch = s.record.last()
            wargs = {'last_epoch': last_epoch, 'best_epoch': best_epoch}
            s.stati.add('metric', best_dict)
        else:
            wargs = {}

        # save checkpoints
        if 'train' in s.args.phases and (s.epoch - s.args.start_epoch) % s.args.save_interval == 0:
            s.save(s.args.checkpoint_path, 'epoch_' + str(s.epoch) + '.pth', **wargs)

        if not 'train' in s.args.phases:
            break

        # print(s.scheduler.get_lr())
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





