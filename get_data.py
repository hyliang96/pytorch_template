from torch.utils.data import DataLoader
from dataset import RandomDataset


def get_data(args, stage):
    if stage == 'train':
        dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
                         batch_size=args.batch_size, shuffle=True)
    elif stage == 'val':
        dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
                         batch_size=args.batch_size, shuffle=True)
    elif stage == 'test':
        dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
                         batch_size=args.batch_size, shuffle=True)
    return dataloader
