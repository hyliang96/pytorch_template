import argparse
import torch
import os

args = argparse.Namespace()

# 参数和数据加载
args.input_size = 5
args.output_size = 2

args.epochs=10
args.log_interval = 10

args.batch_size = 64
args.test_batch_size = 512
args.data_size = 100 # dataset size

args.lr = 0.01
args.momentum = 0.5

args.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
args.use_cuda = torch.cuda.is_available()

args.load_path = os.path.join('../__checkpoint__', '45gpu.pth')
args.save_path = os.path.join('../__checkpoint__', '45gpu.pth')

args.data_path = os.path.join('../__data__')

