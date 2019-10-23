from statistic import Statistic_Dir
import sys, os

# parser = argparse.ArgumentParser()
# parser.add_argument('--exper', type=str, default=args.exper, help='the name of this set of experiment')



if __name__ == "__main__":
    path = Statistic_Dir()
    record_path = os.path.join(path.exper, 'record.txt')
    argvs = sys.argv[1:]
    print(argvs)

    if len(argvs) == 0:
        tag = '\n'.join(os.popen('git tag -l --points-at HEAD 2>/dev/null').readlines())
        print(tag)
        # tag = os.system('git tag -l --points-at HEAD')
        if tag == '':
            print('no tag on current commit!')
            sys.exit(1)

        exper_name_ids = tag
    else:
        exper_name_ids = argvs

    with open(record_path, 'a') as f:
        for exper_name_id in exper_name_ids:
            print(exper_name_id, file=f)

