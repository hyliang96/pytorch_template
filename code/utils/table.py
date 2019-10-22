import json
import os

class Statistic(object):
    def __init__(self, exper_name, exper_statistic_path):
        # exper_list_path 中加 exper_name
        # os.makedirs(exper_statistic_path, exist_ok=True)
        pass

    def add(self, dict_name, Dict):
        # Dict 处理成 int, float, double, bool, str
        # exper_name/dict_name.json 中 写Dict
        pass



def make_tables(exper_list_path, result_path, filenames, statistic_path):

    # exper_list = 读 exper_list_path
    statistics={}

    for exper in exper_list:
        for filename in filenames:
            # dict = result_path/从exper_list/filename中读json
            statistics[exper][filename]=dict






if __name__ == "__main__":
    root_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
    result_path = os.path.join(root_path, '__result__')

    statistic_path = os.path.join(root_path, '__statistic__')
    exper_list_path = os.path.join(statistic_path, 'experiments.txt')
    key_list_path = os.path.join(statistic_path, 'keys.txt')


    make_tables(exper_list_path, result_path, filenames, statistic_path)