from model import Model
import torch
import torch.optim as optim
from utils import show_para

# def get_model(args):



# def save(path, model, epoch, optimizer, scheduler, args):



# def load(path, model):


def get_model(args):
    model = Model(args.input_size, args.output_size)
    return model

def get_optimizer(model, args):
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
    return optimizer

def get_loss(args):
    return None

def get_all(args):
    args.model = get_model(args)
    args.optimizer = get_optimizer(args.model, args)
    args.loss = get_loss(args)
    show_para(args.model, args.optimizer)
    # return args

def save_model(model, save_path):
    if hasattr(model, 'module'):
        torch.save(model.module.state_dict(), save_path)
    else:
        torch.save(model.state_dict(), save_path)

def load_model(model, load_path, device):
    checkpoint = torch.load(load_path, map_location=device)
    print('checkpoint =', checkpoint)
    model.load_state_dict(checkpoint)




class State()
