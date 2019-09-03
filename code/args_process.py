import torch
import os
import time
import argparse

def _process(args):
    # 后处理 argument
    if args.continue_epoch:
        if 'train' in args.phases:
            args.start_epoch = int(args.continue_epoch) + 1
        else:
            args.start_epoch = int(args.continue_epoch)

    args.use_cuda = torch.cuda.is_available()
    args.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # ----------------------------------------------------------------------------------------------
    # 自动生成目录路径
    # project/
    #     code
    #     __data__/
    #     __result__/
    #         [exper]/
    #             [experid]/
    #                 log
    #                 tensorboard/
    #                 checkpoint/

    # absolute path of this file and then goto its ../
    args.root_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    args.data_path = os.path.join(args.root_path, '__data__')

    # __result__/
    args.result_path = os.path.join(args.root_path , '__result__')
    #   [exper]/
    args.exper = args.exper or time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    args.exper_path = os.path.join(args.result_path, args.exper)
    os.makedirs(args.exper_path, exist_ok=True) # if no such path exists, iteratively created the dir
    #       [experid]/
    dirnames = [d for d in os.listdir(args.exper_path) if os.path.isdir(os.path.join(args.exper_path, d)) and d[0]!=0]
    args.experid = args.experid or ( '0' if dirnames == [] else str(max([int(name) for name in dirnames]) + 1) )
    args.experid_path = os.path.join(args.exper_path, args.experid)
    #       [experid]/*
    args.checkpoint_path = os.path.join(args.experid_path , 'checkpoint')
    args.load_path = args.load_path or ( os.path.join(args.checkpoint_path, 'epoch_'+args.continue_epoch+'.pth') if args.continue_epoch else '')
    args.tensorboard_path = os.path.join(args.experid_path , 'tensorboard')
    args.log_path = os.path.join(args.experid_path , 'log')

    os.makedirs(args.checkpoint_path, exist_ok=True)
    os.makedirs(args.tensorboard_path, exist_ok=True)

argparse.Namespace.process = _process