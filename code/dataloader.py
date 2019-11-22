import torch
from torchvision import datasets, transforms
from utils.seed import set_work_init_fn
# from dataset import RandomDataset




def DataLoaders(args):
    assert set(args.phases) <= {'train', 'train_test', 'val', 'test'}

    transform=transforms.Compose([
                            transforms.ToTensor(),
                            transforms.Normalize((0.1307,), (0.3081,))
                            ])

    dataset = {}
    if {'train', 'val'}.intersection(set(args.phases)):
        dataset['train'] = datasets.MNIST(args.data_path, train=True, download=True, transform=transform)
    if 'val' in args.phases:
        val_length = round(len(dataset['train']) * args.val_rate)
        lengths = [len(dataset['train']) - val_length, val_length]
        # https://pytorch.org/docs/stable/data.html#torch.utils.data.random_split
        classes = dataset['train'].classes
        dataset['train'], dataset['val'] = torch.utils.data.random_split(dataset['train'], lengths)
        dataset['train'].classes = dataset['val'].classes = classes
    if 'test'  in args.phases:
        dataset['test'] = datasets.MNIST(args.data_path, train=False, download=True, transform=transform)


    dataloaders = {}
    for stage in args.phases:
        dataloader = dataloaders[stage] = torch.utils.data.DataLoader(
            dataset[stage if stage != 'train_test' else 'train'],
            batch_size=args.batch_size['train'] if stage=='train' else args.batch_size['test'],
            shuffle=True, worker_init_fn=set_work_init_fn(args.seed),
            num_workers=args.num_workers, pin_memory=True
        )


    dataloaders['dummy'] = list(dataloaders.values())[0]

    for stage in args.phases + ['dummy']:
        dataloader = dataloaders[stage]
        print('dataloader[{:10s}]: batch_num={:<8d} batch_size={:<4d} data_num={:<8d} '.format(stage, len(dataloader), dataloader.batch_size, len(dataloader.dataset) ) )


    #     # dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
    #     #                  batch_size=args.batch_size, shuffle=True)
    # if 'train'  in args.phases:
    #     dataloaders['val'] = torch.utils.data.DataLoader(dataset['val'],
    #         batch_size=args.test_batch_size, shuffle=True, worker_init_fn=set_work_init_fn(args.seed), **kwargs)

    #     # dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
    #     #                  batch_size=args.batch_size, shuffle=True)
    # elif stage == 'test':
    #     dataloader = torch.utils.data.DataLoader(
    #         dataset['test' ],
    #         batch_size=args.test_batch_size, shuffle=True, worker_init_fn=set_work_init_fn(args.seed), **kwargs)
    #     # dataloader = DataLoader(dataset=RandomDataset(args.input_size, args.data_size),
    #     #                  batch_size=args.batch_size, shuffle=True)
    return dataloaders




