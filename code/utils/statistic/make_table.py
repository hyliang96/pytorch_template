from statistic import Statistic_Dir, parse_exper_file
import sys, os
import commentjson, json
from jsoncomment import JsonComment
import csv
# import re

def make_table(exper_set, title_set):
    path = Statistic_Dir()

    exper_file = os.path.join(path.exper, exper_set + '.txt')
    title_file = os.path.join(path.title, title_set + '.json')
    table_file = os.path.join(path.table, exper_set + '.csv')


    expers = parse_exper_file(exper_file)
    with open(title_file, 'r') as f:
        parser = JsonComment(json)
        titles = parser.load(f)
        # titles = commentjson.load(f)

    type_list = ['hparam']
    title_list = ['expernameid']
    for _type, _type_title_list in titles.items():
        for title in _type_title_list:
            if title != 'expernameid':
                type_list.append(_type)
                title_list.append(title)

    table = []
    # table.append(type_list)
    table.append(title_list)


    for exper in expers:
        exper_data = []
        exper_stati_file = os.path.join(path.root, '__result__', exper, 'statistic.json')
        with open(exper_stati_file, 'r') as f:
            exper_stati = json.load(f)
            for _type, title in zip(type_list, title_list):
                value = exper_stati[_type][title]
                # if re.match(r'^[-+]*[0-9]+.[0-9]+$', value):
                #     value = '%' % float(value)
                exper_data.append(value)
        table.append(exper_data)

    # print(table)

    with open(table_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(table)


if __name__ == "__main__":
    exper_sets = sys.argv[1:]

    if len(exper_sets) == 0:
        exper_sets = ['record']

    for exper_set in exper_sets:
        title_set = exper_set
        make_table(exper_set, title_set)
