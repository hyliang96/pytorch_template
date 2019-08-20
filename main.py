#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from torch.autograd import Variable
import os

from get_data import get_data
from args import args
from get_model import save_model, load_model, get_all

def main(args):
    dataloader = get_data(args, 'test')
    get_all(args)
    load_model(args.model, args.load_path, args.device)
    print(args.model)

    return
    model = nn.DataParallel(model)
    model.to(args.device)

    for data in dataloader:
        input_var = data.to(args.device)
        output = model(input_var)
        print("Outside: input size", input_var.size(),
            "args.output_size", output.size())

    # save_model(model, args.save_path)

if __name__ == "__main__":
    main(args)
