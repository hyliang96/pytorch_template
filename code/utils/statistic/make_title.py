from statistic import Statistic_Dir, parse_exper_file
import sys, os
import json



def make_title(exper_set):
    path = Statistic_Dir()
    title_set = exper_set

    exper_file = os.path.join(path.exper, exper_set+'.txt')
    title_file = os.path.join(path.title, title_set + '.json')
    print('read experiments from:', exper_file)
    print('write titles to:', title_file)

    expers = parse_exper_file(exper_file)

    combined_stati = {}
    for exper in expers:
        exper_stati_file = os.path.join(path.root, '__result__', exper, 'statistic.json')
        with open(exper_stati_file, 'r') as f:
            exper_stati = json.load(f)
            for stati_set, statis_dict in exper_stati.items():
                if stati_set not in combined_stati.keys():
                    combined_stati[stati_set] = list(statis_dict.keys())
                else:
                    for stati_name in statis_dict.keys():
                        if stati_name not in combined_stati[stati_set]:
                            combined_stati[stati_set].append(stati_name)

    # print(combined_stati)

    with open(title_file, 'w') as f:
       json.dump(combined_stati, f, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    exper_sets = sys.argv[1:]

    if len(exper_sets) == 0:
        exper_sets = ['record']

    for exper_set in exper_sets:
        make_title(exper_set)
