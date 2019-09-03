import argparse
import torch
import os
import time

# parser = argparse.ArgumentParser()
# parser.add_argument('--exper', type=str, default='', help='the name of this set of experiment')
# args = parser.parse_args()

args = argparse.Namespace()
args.path = {}

# ----------------------------------------------------------------------------------------------

# 参数和数据加载
args.input_size = 5
args.output_size = 2

args.epochs=10
args.pbar_interval = 1

args.batch_size = 64
args.test_batch_size = 512
args.data_size = 100 # dataset size

args.lr = 0.01
args.momentum = 0.5

args.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
args.use_cuda = torch.cuda.is_available()

args.exper = "exper1"
args.load_epoch = "latest"
args.load_path = ""

# ----------------------------------------------------------------------------------------------
# 自动生成目录路径
# code
# __data__/
# __result__/
#   [exper]/
#       [experid]/
#           log
#           tensorboard/
#           checkpoint/

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
args.experid = '0' if dirnames == [] else str(max([int(name) for name in dirnames]) + 1)
args.experid_path = os.path.join(args.exper_path, args.experid)
#       [experid]/*
args.checkpoint_path = os.path.join(args.experid_path , 'checkpoint')
args.load_path = args.load_path or os.path.join(args.checkpoint_path, args.load_epoch) 
args.tensorboard_path = os.path.join(args.experid_path , 'tensorboard')
args.log_path = os.path.join(args.experid_path , 'log')

os.makedirs(args.checkpoint_path, exist_ok=True) 
os.makedirs(args.tensorboard_path, exist_ok=True) 