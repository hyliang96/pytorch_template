import args_process, argparse

args = argparse.Namespace()

# ----------------------------------------------------------------------------------------------
# 参数和数据定义
args.input_size =  5
args.output_size = 2

args.start_epoch = 0
# args.n_epoch = 10
args.end_epoch = 10
args.save_interval = 1
args.pbar_interval = 1

args.batch_size = {'train':64, 'test': 512}
args.data_size = 100 # dataset size
args.num_workers = 8  # recommented 4 * num_GPU, https://discuss.pytorch.org/t/guidelines-for-assigning-num-workers-to-dataloader/813/3

args.lr = 0.001 # 0.01 is best
args.momentum = 0.5

args.phases = ['train', 'val', 'test'] # ['train', 'train_test', 'val', 'test'] 的子集
args.val_rate = 0.3  # val set 占 train set 的比例

# [ 'benchmark', 'normal', 'slow', 'none' ], cudnn 随机性从左到右减小，复现接近程度增加，一般用normal
args.cudnn_behavoir = 'normal'
# ----------------------------------------------------------------------------------------------

args.exper = "test2" # "2019-11-22_19-48-28"
args.experid = "0" # '0'

# 若写下属任意一个，则load，否则不load
# 继续训练，或测试某个epoch的checkpoint
args.continue_epoch = "3" # 'latest', 'best', '0', '1', '2' ...
# 单纯加载，不必继续训练，建议写绝对路径
args.load_path = ""

# ----------------------------------------------------------------------------------------------
# merge argparse and this

args.process()
