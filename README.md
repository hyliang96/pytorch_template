
# Introduction

This is an experiment managing template for pytorch based on git. It can

* record code, config, random seed, metric, output for each experiment with git commit

* reproduce recorded experiments by git check

* visualize the metric, model structure with tensorboard

* record hyperparameters and metrics of experiments and make table to comapre them

* save all traning state into a checkpoint and allow loading it to continue training

The principles:

* all arguments are stastic, saved in the config.py, rather than argparsed from command lines (except the tag of a experiment), so that config can bre recorded by git

# Usage

* always source the command line tools when entering the project

    ~~~bash
    . ./code/source.sh
    ~~~

* record codes and run with tag `<expertag>`

    ~~~bash
    git commit -m '<commit-message>'
    CUDA_VISIBLE_DEVICES=n1[,n2[,..]] run <expertag> [-f]    # -f to fix random seed
    ~~~

* rerun an experiment

    git checkout to `<expertag>`

    ~~~bash
    CUDA_VISIBLE_DEVICES=n1[,n2[,..]] rerun <expertag> [-f]  # -f to fix random seed
    ~~~

* record a set of experiments

    All finished experiments are automatically added to `__statistic__/exper-list/finished.txt`

    Mannually add an experiment `<expertag>/<experid>` to `__statistic__/exper-list/record.txt`

    ~~~bash
    record [<expertag>/<experid>]   # xxx=record for default
    ~~~

    Besides, you can write your own experiment set in `__statistic__/exper-list/xxx.txt`, a `<expertag>/<experid>` per line

* make table title

    collect all hyperparameters and metrcis from the statictics.json of the experiments recorded in `__statistic__/exper-list/xxx.txt`, and write them to `__statistic__/title/xxx.json`.

    ~~~bash
    title [xxx]               # xxx=record for default
    ~~~

    then you can edit `__statistic__/title/xxx.json` by commenting some lines if you do not need them

* make table

    make table for experiment in `__statistic__/exper-list/xxx.txt`  with the table title in `__statistic__/title/xxx.json`

    ~~~bash
    table [xxx]               # xxx=record for default
    ~~~

# misc

* Tensorboard server will be started up background when you run `python main.py` or `run`. The port used will be reported on screen output as

    > TensorBoard 2.0.0 at http://localhost:6006/ (Press CTRL+C to quit)

* `tqdm` output growing processing bars (expect the remained bar) through stderror, and `utils/log.py` only record stdout. Thus the growing processing bar is not recorded in to the log.


# Directory Structure

~~~
project/
    code/                     they will be recorded by git
        source.sh             command line tools
        config.py             all statistic arguments
        args_process.py       process the statistic arguments
        main.py
        model.py
        dataloarder.py        define a dataloader
        epoch.py              the iteration in an epoch
        state.py              training state -- a class of all objects, save and load
        utils/
            _*.py             patch some existing packages
            [^_]*.py          new packages
            statistic/        record metrics, hyperparameters of experiments; make tables to compare
        seed                  random seed
    __data__/                 dataset
    __result__/
        [expertag]/                  code will be git tagged with [expertag]
            [experid]/               each id represents a run of the code [expertag], id=0,1,2...
                log
                tensorboard/
                checkpoint/
                    epoch_n.path                        n=0,1,2...
                    epoch_last.path,epoch_best.path     soft link
                statistic.json                          metrics, hyperparameters of an experiment
    __statistic__/
        exper-list/                                 sets of experiments as [expertag]/[experid]
            finished.txt, record.txt, xxx.txt       finished, manually recorded, customs' experiment set
        title/                                      table title. i.e. metrics, hyperparameters
            finished.json, record.json, xxx.json
        table/                                      tables to compare experiments
            finished.csv, record.csv, xxx.csv
~~~


# development

- [x] automatically split train set, train|test|val set instead of val|test set

- [x] class Record: [reference](https://github.com/QuantScientist/Deep-Learning-Boot-Camp/blob/dbfa7d5f796d8d19a6e7e924548669741fd125b2/Kaggle-PyTorch/PyTorch-Ensembler/utils.py)

- [x] save/load checkpoint, [reference](https://discuss.pytorch.org/t/how-to-save-and-load-lr-scheduler-stats-in-pytorch/20208)

- [ ] append to tensorboard events


