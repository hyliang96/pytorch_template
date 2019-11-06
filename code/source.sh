#!/usr/bin/env bash

# get absoltae path to the dir this is in, work in bash, zsh
# if you want transfer symbolic link to true path, just change `pwd` to `pwd -P`
project_root=$(cd "$(dirname "${BASH_SOURCE[0]-$0}")"/..; pwd)

. ${project_root}/code/utils/statistic/source.sh


run()
{
    if [ "$1" = 'help' ] || [ "$1" = '--help' ] || [ "$1" = '-h' ]; then
        echo "Usage:"
        # echo "gpuid [n,m,...] run <experiment_name>                      : for a commited status, tag it with its name, then run experiment"
        echo "gpuid [n,m,...] run <experiment_name> [--fix-seed|-f]  : for a uncommited status, commit a new experiment and tag it with its name, then run experiment"
        echo "gpuid [n,m,...] run --rerun(-r) <experiment_name>   : git checkout a git tag, then rerun the experiment"
        return
    fi

    if ! [[ "$(cd ${project_root} && git status)" =~ 'nothing to commit, working directory clean' ]]; then
        echo 'Please commit or stash before run experiment'
        return
    fi

    if [ "$1" = '--rerun' ] || [ "$1" = '-r' ]; then
        shift
        if [ $# -ne 1 ]; then echo "Can't get tag to rerun, while args number is not correct."; echo; run help; return; fi
        local tag="$1"
        git checkout "$tag" && \
        python3 ${project_root}/code/main.py --exper "$tag"
    else
        if [ $# -lt 1  ] || [ $# -gt 2 ]; then echo "Trying to set new tag, but args number is not correct."; echo; run help; return; fi
        local tag="$1"

        # 若tag是已有的，则报错，退出
        for i in $(git tag); do
            if [ "$i" = "$tag"  ]; then
                echo "$tag is existing"; return
            fi
        done

        local seed_file="${project_root}/code/seed"
        if [ "$1" = '--fix-seed' ] || [ "$1" = '-f' ]; then
            shift
            ( ! [ -f "$seed_file" ] ) &&  echo 0 > $seed_file
        else
            echo $RANDOM > $seed_file
        fi

        if ! [[ "$(cd ${project_root} && git status)" =~ 'nothing to commit, working directory clean' ]]; then
            git add -A ${project_root} &&
            git commit -m "commit before run experiment"
        fi

        git tag -a "$tag" -m "run experiment" && \
        python3 ${project_root}/code/main.py --exper "$tag"
    fi
}


alias rerun='run --rerun'

# eval $(cat <<EOF
# run()
# {
#     if [ "$1" = 'help' ] || [ "$1" = '--help' ] || [ "$1" = '-h' ]; then
#         echo "Usage:"
#         echo "gpuid [n,m,...] run <experiment_name>                      : for a commited status, tag it with its name, then run experiment"
#         echo "gpuid [n,m,...] run <experiment_name> <git-commit-mesage>  : for a uncommited status, commit a new experiment and tag it with its name, then run experiment"
#         echo "gpuid [n,m,...] run --rerun(-r) <experiment_name>          : git checkout a git tag, then rerun the experiment"
#     elif [ "$1" = '--rerun' ] || [ "$1" = '-r' ]; then
#         if [ $# -ne 2 ]; then
#             echo "Gonna checkout to a node in git, while args number is not correct."
#             echo
#             run help
#             return
#         fi
#         git checkout "$2" && \
#         python3 ${project_root}/code/main.py --exper "$2"
#     else
#         if ! [[ "$(cd ${project_root} && git status)" =~ 'nothing to commit, working directory clean' ]]; then
#             if [ $# -ne 2 ]; then
#                 echo "This is an uncommited status, while args number is not correct."
#                 echo
#                 run help
#                 return
#             fi
#             git add -A ${project_root} &&
#             git commit -m "$2"
#         else
#             if [ $# -ne 1 ]; then
#                 echo "This is a commited status, while args number is not correct."
#                 echo
#                 run help
#                 return
#             fi
#         fi

#         git tag -a "$1" -m "experiment" && \
#         python3 ${project_root}/code/main.py --exper "$1"
#     fi
# }
# EOF
# )

expls()
{
    if [ $# -eq 0 ]; then
        ls $project_root/__result__
    else
        for i in "$@"; do
            echo $i:
            local dir_path="$project_root/__result__/$i"
            echo '        '$dir_path
            ls $dir_path
        done
    fi
}



# tensorboard for my pytorch-template
itb()
{
    local exper_names
    declare -a exper_names
    while [ $# -ne 0 ]; do
        if [[ "$1" =~ "^-"  ]]; then
            break
        else
            exper_names=("${exper_names[@]}" "$1")
            shift
        fi
    done

    if [ ${#exper_names} -eq 0 ]; then
        local exper_name="$(basename $(cd .. && pwd -P ))/$(basename $(cd . && pwd -P ))"
        exper_names=("$exper_name")
    fi

    local dir_arg='--logdir_spec='
    local exper_name
    for exper_name in "${exper_names[@]}"; do
        if [ -d "$exper_name"  ]; then
            local dir_path="$exper_name/tensorboard"
            local exper_name="$(basename $(cd "$exper_name/.." && pwd -P ))/$(basename $(cd "$exper_name" && pwd -P ))"
        else
            local dir_path="${project_root}/__result__/$exper_name/tensorboard"
        fi
        local dir_arg="${dir_arg}${exper_name}:${dir_path},"
    done
    dir_arg="${dir_arg:0:-1}"

    tensorboard $dir_arg $@
}


# release this variable in the end of file
# unset -v here
