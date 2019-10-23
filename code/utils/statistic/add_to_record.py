from statistic import Statistic_Dir
import sys, os
import re

# parser = argparse.ArgumentParser()
# parser.add_argument('--exper', type=str, default=args.exper, help='the name of this set of experiment')



if __name__ == "__main__":
    path = Statistic_Dir()
    record_path = os.path.join(path.exper, 'record.txt')
    argvs = sys.argv[1:]

    if len(argvs) == 0:
        result = os.popen('git tag -l --points-at HEAD 2>/dev/null').readlines()
        result = [line for line in result if not re.search(r'^[\s]*$', line)]
        result = [line[:-1] if line[-1] == '\n'  else line for line in result ]
        tag = '\n'.join(result)
        if tag == '':
            print('no tag on current commit!')
            sys.exit(1)
        exper_name_ids = [tag]
    else:
        exper_name_ids = argvs




    # exper_name_ids = '\n'.join(exper_name_ids)
    for exper_name_id in exper_name_ids:
        exper_name_id_path = os.path.join(path.root, '__result__', exper_name_id)
        if not os.path.isdir(exper_name_id_path):
            print('not existing path:',exper_name_id_path)
            continue
        with open(record_path, 'a') as f:
            print('\n'+exper_name_id, file=f, end='')



# s1 = 'adkkdk'

# #判断s1字符串是否负责都为小写的正则
# an = re.search('^[a-z]+$', s1)
# if an:
#     print 'yes'
# else:
#     print 'no'
