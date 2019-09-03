import args_process, argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('--exper', type=str, default='', help='the name of this set of experiment')
# args = parser.parse_args()
args = argparse.Namespace()

# ----------------------------------------------------------------------------------------------
# 参数和数据定义
args.input_size = 5
args.output_size = 2

args.start_epoch = 0
args.n_epoch = 10
args.save_interval = 1
args.pbar_interval = 1

args.batch_size = 64
args.test_batch_size = 512
args.data_size = 100 # dataset size

args.lr = 0.01
args.momentum = 0.5

args.phases = ['train', 'test']

args.exper = "exper1"
args.experid = '0'
# 若写下属任意一个，则load，否则不load
args.continue_epoch = "2" # 此即继续训练之意，或测试某个epoch的checkpoint
args.load_path = ""

# ----------------------------------------------------------------------------------------------
args.process()