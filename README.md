
# Introduction

This is an experiment managing template for pytorch based on git. It can

* record code, config, random seed, metric, output for each experiment with git commit

* reproduce recorded experiments by git check

* visualize the metric, model structure with tensorboard

* record hyperparameters and metrics of experiments and make table to comapre them

* save all traning state into a checkpoint and allow loading it to continue training

The principles

* Minimal dependence: do not depend on database or other dashboard, so that one can install it easily.

* Readability: saved results in and readable files (like json, csv) under an organized directory, rather than database.

* Minimal encapsulation: to ensure flexibility for reseach codes, no high-level encapsulation dependence is applied, such as [fastai](https://github.com/fastai/fastai), [lighting](https://github.com/williamFalcon/pytorch-lightning#why-do-i-want-to-use-lightning), [iginite](https://github.com/pytorch/ignite), [torchnet](https://github.com/pytorch/tnt), [ray](https://github.com/ray-project/ray).

* Reproducibility: all arguments are stastic, saved in the config.py, rather than argparsed from command lines (except the tag of an experiment, whether continue an experiment), so that config can bre recorded by git.

# Install

~~~bash
pip install -r code/requirements.txt
~~~

# Usage

* always source the command line tools when entering the project

    ~~~bash
    . ./code/source.sh
    ~~~

## Run experiments

* record codes and run with tag `<expertag>`

    ~~~bash
    git commit -m '<commit-message>'
    CUDA_VISIBLE_DEVICES=n1[,n2[,..]] run <expertag> [-f]    # -f to fix random seed
    ~~~

* continue an experiment

    git checkout to `<expertag>` and continue an unfinished experiment

    ~~~bash
    CUDA_VISIBLE_DEVICES=n1[,n2[,..]] con|continue <expertag> [-f]  # -f to fix random seed
    ~~~

* rerun an experiment

    git checkout to `<expertag>`

    ~~~bash
    CUDA_VISIBLE_DEVICES=n1[,n2[,..]] re|rerun <expertag> [-f]  # -f to fix random seed
    ~~~

## Record experiments and make tables

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

## start tensorboard

* list all experiment

~~~bash
expls               # list all expertag
expels <expertag>   # list all experid under the <expertag>
~~~

* compare experiments in tensorboard

~~~bash
itb <expertag1>[/<experid1>] [<expertag2>[/<experid2>] ...]
 # <expertag1> for all <experid1>s under <expertag1>
 # <expertag1>/<experid1> for a specific <experid1> under <expertag1>
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
    README.md
    .gitignore
    .git/
~~~

According to `.gitignore`, `/__*__` are ignored by the git for their large size.

# development

- [x] automatically split train set, train|test|val set instead of val|test set

- [x] class Record: [reference](https://github.com/QuantScientist/Deep-Learning-Boot-Camp/blob/dbfa7d5f796d8d19a6e7e924548669741fd125b2/Kaggle-PyTorch/PyTorch-Ensembler/utils.py)

- [x] save/load checkpoint, [reference](https://discuss.pytorch.org/t/how-to-save-and-load-lr-scheduler-stats-in-pytorch/20208)

- [x] it is not suppoed to append to tensorboard events [details](https://github.com/tensorflow/tensorflow/issues/2399#issuecomment-219837074); just write to a new tensorboard event under the same dir. tensorboard sever will how them as the same experiment when you use `itb`


