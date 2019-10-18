import args_process, argparse

args = argparse.Namespace()

# ----------------------------------------------------------------------------------------------
# 参数和数据定义
args.input_size = 5
args.output_size = 2

args.start_epoch = 0
args.n_epoch = 1
args.save_interval = 1
args.pbar_interval = 1

args.batch_size = 64
args.test_batch_size = 512
args.data_size = 100 # dataset size

args.lr = 0.01
args.momentum = 0.5

args.phases = ['train', 'test'] # 'train', 'test', 'val'

args.exper = ""
args.experid = ''

# 若写下属任意一个，则load，否则不load
# 继续训练，或测试某个epoch的checkpoint
args.continue_epoch = "" # 'latest', 'best', '0', '1', '2' ...
# 单纯加载，不必继续训练，建议写绝对路径
args.load_path = ""

# ----------------------------------------------------------------------------------------------
# merge argparse and this

args.process()
