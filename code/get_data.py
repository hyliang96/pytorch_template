import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
# from dataset import RandomDataset

transform=transforms.Compose([
                            transforms.ToTensor(),
                            transforms.Normalize((0.1307,), (0.3081,))
                            ])


def get_data(args, stage):
    kwargs = {'num_workers': 1, 'pin_memory': True} if args.use_cuda else {}
    if stage == 'train':
        dataloader = torch.utils.data.DataLoader(
            datasets.MNIST(args.data_path, train=True, download=True, transform=transform),
            batch_size=args.batch_size, shuffle=True, **kwargs)
        # dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
        #                  batch_size=args.batch_size, shuffle=True)
    elif stage == 'val':
        dataloader = torch.utils.data.DataLoader(
            datasets.MNIST(args.data_path, train=True,  download=True, transform=transform),
            batch_size=args.test_batch_size, shuffle=True, **kwargs)
        # dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
        #                  batch_size=args.batch_size, shuffle=True)
    elif stage == 'test':
        dataloader = torch.utils.data.DataLoader(
            datasets.MNIST(args.data_path, train=False,  download=True, transform=transform),
            batch_size=args.test_batch_size, shuffle=True, **kwargs)
        # dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
        #                  batch_size=args.batch_size, shuffle=True)
    return dataloader




