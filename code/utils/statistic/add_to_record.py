from .statistic import Statistic_Dir
import sys, os

# parser = argparse.ArgumentParser()
# parser.add_argument('--exper', type=str, default=args.exper, help='the name of this set of experiment')



if __name__ == "__main__":
    path = Statistic_Dir()
    record_path = os.path.join(path.exper, 'record.txt')

    if len(sys.argv) == 0:
        exper_name_ids = ['tag']
    else:
        exper_name_ids = sys.argv

    with open(record_path, 'a') as f:
        for exper_name_id in exper_name_ids:
            print(exper_name_id, file=f)

