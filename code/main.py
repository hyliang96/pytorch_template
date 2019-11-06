#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pprint import pprint

from config import args
from get_data import get_data
from state import State
from epoch import run_epoch

from tqdm import tqdm
from utils import patch
from utils.statistic import Statistic
from utils.log import Log
from utils.tensorboard import Tensorboard
from utils.misc import Max, symlink_force
from utils.seed import set_seed


from model import Net
from torch import optim


def main(args):
    s = State(args)
    set_seed(s.args.seed, s.args.cudnn_behavoir)
    s.log = Log(s.args.log_path)
    s.writer = Tensorboard(s.args.tensorboard_path)
    s.stati  = Statistic(s.args.expernameid, s.args.experid_path, s.args.root_path)

    print('----------------------------------------------------------------------------------------------')
    print('args:')
    print(s.args)
    print('----------------------------------------------------------------------------------------------')
    s.stati.add('hparam', s.args.dict())
    # s.writer.add_hparams(hparam_dict=s.args.dict(), metric_dict={})

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
    s.stati.close()
    s.writer.close()
    s.log.close()

if __name__ == "__main__":
    main(args)
