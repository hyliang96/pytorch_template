import torch
import os
import time
import argparse


def _parse_override_to(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--exper', type=str, default=args.exper, help='the name of this set of experiment')
    new_args = parser.parse_args()

    for key,value in vars(new_args).items():
        setattr(args, key, value)
    return args

def _process(args):
    _parse_override_to(args)

    # 后处理 argument
    args.use_cuda = torch.cuda.is_available()
    args.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # ----------------------------------------------------------------------------------------------
    # 自动生成目录路径
    # project/
    #     code/
    #         seed
    #     __statictic__/
    #         exper-list/deafult.txt -> selected.txt, finished.txt, <experiments>.txt
    #         title/default.json->all.json, <titles>.txt
    #         table/selected.csv, finished.csv <experiments-titles>.csv
    #     __data__/
    #     __result__/
    #         [exper]/
    #             [experid]/
    #                 log
    #                 tensorboard/
    #                 checkpoint/
    #                 statistic.json

    # absolute path of this file and then goto its ../
    args.root_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
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
    args.expernameid = args.exper + '/' + args.experid
    args.experid_path = os.path.join(args.exper_path, args.experid)

    #           checkpoint/
    args.checkpoint_path = os.path.join(args.experid_path , 'checkpoints')
    os.makedirs(args.checkpoint_path, exist_ok=True)
    if args.continue_epoch:
        continue_epoch_path = os.path.join(args.checkpoint_path, 'epoch_'+args.continue_epoch+'.pth')
        if os.path.islink(continue_epoch_path):
            args.continue_epoch = os.path.basename(os.readlink(continue_epoch_path) ).replace('epoch_', '').replace('.pth', '')
        if 'train' in args.phases:
            args.start_epoch = int(args.continue_epoch) + 1
        else:
            args.start_epoch = int(args.continue_epoch)
    args.load_path = args.load_path or (os.path.join(args.checkpoint_path, 'epoch_'+args.continue_epoch+'.pth') if args.continue_epoch else '')
    #           tensorboard/
    args.tensorboard_path = os.path.join(args.experid_path , 'tensorboard')
    os.makedirs(args.tensorboard_path, exist_ok=True)
    #           log
    args.log_path = os.path.join(args.experid_path , 'log')
    #           statistic.json
    # args.exper_stati_path = os.path.join(args.experid_path , 'statistic.json')

    # __statistic__/
    # args.stati_path = os.path.join(args.root_path , '__statistic__')
    # os.makedirs(args.stati_path, exist_ok=True) # if no such path exists, iteratively created the dir
    # #       exper-list/
    # args.exper_list_path = os.path.join(args.stati_path , 'exper-list')
    # os.makedirs(args.exper_list_path, exist_ok=True) # if no such path exists, iteratively created the dir
    # #       title/
    # args.title_path = os.path.join(args.stati_path , 'title')
    # os.makedirs(args.title_path, exist_ok=True) # if no such path exists, iteratively created the dir
    # #       table/
    # args.table_path = os.path.join(args.stati_path , 'table')
    # os.makedirs(args.table_path, exist_ok=True) # if no such path exists, iteratively created the dir


    assert args.start_epoch <= args.end_epoch, \
        "error args: start_epoch = {}, end_epoch = {}, while it should be start_epoch <= end_epoch".format(args.start_epoch, args.end_epoch)

    # 随机数
    args.code_path = os.path.join(args.root_path, 'code')
    args.seed_path = os.path.join(args.code_path, 'seed')
    with open(args.seed_path,'r') as f:
        lines = f.readlines()
        assert len(lines) == 1
        seed_str = lines[0].replace('\n','')
        args.seed = int(seed_str)



argparse.Namespace.process = _process


