#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from pprint import pprint

from get_data import get_data
from state import State
from epoch import run_epoch

from tqdm import tqdm
from utils import patch

from utils.misc import Max, symlink_force


from model import Net
from torch import optim






def main(s):
    s.model = Net()
    s.optimizer = optim.SGD(s.model.parameters(), lr=s.args.lr, momentum=s.args.momentum)

    if args.load_path:
        s.load(s.args.load_path)

    if 'train' in s.args.phases or 'val' in s.args.phases:
        dummy_loader = train_loader = get_data(s.args, 'train')
    if 'test'  in s.args.phases:
        dummy_loader = test_loader  = get_data(s.args, 'test')

    s.writer.add_model_graph(s.model, dummy_loader)
    s.deploy()

    if 'train' in s.args.phases and 'test' in s.args.phases:
        s.best = Max('test-acc')
    for s.epoch in range(s.args.start_epoch, s.args.start_epoch + s.args.n_epoch):
        s.epoch_pbar = tqdm(bar_format='{desc}', leave=True, desc = 'Epoch {} |'.format(s.epoch))
        if 'train' in s.args.phases:
            _  = run_epoch('train', s, train_loader )
        if 'test' in s.args.phases:
            result = run_epoch('test',  s, test_loader  )
        if 'train' in s.args.phases and 'test' in s.args.phases:
            s.best.add(s.epoch, result)
        s.epoch_pbar.close()

        if 'train' in s.args.phases and (s.epoch - s.args.start_epoch) % s.args.save_interval == 0:
            s.save( os.path.join(s.args.checkpoint_path, 'epoch_'+str(s.epoch)+'.pth') )
            symlink_force('epoch_'+str(s.epoch)+'.pth', os.path.join(s.args.checkpoint_path, 'epoch_latest.pth'))
            if 'test' in s.args.phases:
                symlink_force('epoch_' + str(s.best.id()) + '.pth', os.path.join(s.args.checkpoint_path, 'epoch_best.pth'))
                s.stati.add('metric', s.best.data())
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





