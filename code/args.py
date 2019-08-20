import argparse
import torch
import os

args = argparse.Namespace()

# 参数和数据加载
args.input_size = 5
args.output_size = 2

args.batch_size = 30
args.data_size = 100 # dataset size

args.lr = 0.001
args.momentum = 0.9

args.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
args.load_path = os.path.join('checkpoint', '4gpu.pth')
args.save_path = os.path.join('checkpoint', '4gpu.pth')


