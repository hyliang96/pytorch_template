__all__ = [ "Statistic"]

import json
import os
import warnings
import re


class Statistic_Dir(object):
    def __init__(self, root_path=None):
        self.dir = {}
        self.dir['root']  = root_path or os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..'))
        self.dir['stati'] = os.path.join(self.dir['root'], '__statistic__')
        self.dir['exper'] = os.path.join(self.dir['stati'], 'experiment')
        self.dir['title'] = os.path.join(self.dir['stati'], 'title')
        self.dir['table'] = os.path.join(self.dir['stati'], 'table')

        for path in self.dir.values():
            os.makedirs(path, exist_ok=True) # if no such path exists, iteratively created the dir

        for path_name, path in self.dir.items():
            setattr(self, path_name, path)

class Statistic(object):
    def __init__(self, expernameid, experid_path, root_path=None):
        self.expernameid = expernameid
        self.experid_path = experid_path
        self.exper_stati_path = os.path.join(self.experid_path, 'statistic.json')
        self.path = Statistic_Dir(root_path)
        self.finished_exper_path = os.path.join(self.path.exper, 'finished.txt')
        self.stati = {}

        self.finished_exper_list_file = open(self.finished_exper_path, 'a')

    def close(self):
        print(self.expernameid, file = self.finished_exper_list_file)
        self.finished_exper_list_file.close()

    def __del__(self):
        if not self.finished_exper_list_file.closed:
            self.close()



    def add(self, tag, Dict, mode='cover'):
        Dict = {str(key): '%.4f' % value if type(value) in [float ] \
            else str(value) for key, value in Dict.items()}


        if mode not in ['replace', 'cover', 'add']:
            warnings.warn("mode "+mode+" is not in [replace|cover|add]; automatically set it to 'cover'.", SyntaxWarning)
            mode = 'cover'

        if mode == 'replace':
            self.stati[tag] = Dict
        else:
            if tag not in self.stati.keys():
                self.stati[tag] = {}
            for key, value in Dict.items():
                if mode != 'add' or key not in self.stati[tag].keys():
                    self.stati[tag][key] = value


        with open(self.exper_stati_path, 'w') as f:
            json.dump(self.stati, f, indent=4, ensure_ascii=False)


        # Dict 处理成 int, float, double, bool, str
        # exper_name/dict_name.json 中 写Dict
        # pass


def parse_exper_file(exper_file):
    expers = []
    with open(exper_file, 'r') as f:
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            answer = re.search(r'^[\s]*$', line)
            if answer:
                continue
            expers.append(line)
    return expers


# def make_tables(exper_list_path, result_path, filenames, statistic_path):

#     # exper_list = 读 exper_list_path
#     statistics={}

#     for exper in exper_list:
#         for filename in filenames:
#             # dict = result_path/从exper_list/filename中读json
#             statistics[exper][filename]=dict






# if __name__ == "__main__":
#     root_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
#     result_path = os.path.join(root_path, '__result__')

#     statistic_path = os.path.join(root_path, '__statistic__')
#     exper_list_path = os.path.join(statistic_path, 'experiments.txt')
#     key_list_path = os.path.join(statistic_path, 'keys.txt')


#     make_tables(exper_list_path, result_path, filenames, statistic_path)
