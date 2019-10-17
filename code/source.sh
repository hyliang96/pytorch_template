#!/usr/bin/env bash

# get absoltae path to the dir this is in, work in bash, zsh
# if you want transfer symbolic link to true path, just change `pwd` to `pwd -P`
project_root=$(cd "$(dirname "${BASH_SOURCE[0]-$0}")"/..; pwd)



# eval $(cat <<EOF
run()
{
    echo $#
    if [ "$1" = 'help' ] || [ "$1" = '--help' ] || [ "$1" = '-h' ] || [ "$#" -ne 2 ]; then
        echo "Usage:"
        echo "gpuid [n,m,...] run <experiment_name> <git-commit-mesage>  : commit a new experiment and tag it with its name"
        echo "gpuid [n,m,...] run --rerun(-r) <experiment_name>          : git checkout old tag and rerun the experiment"
    elif [ "$1" = '--rerun' ] || [ "$1" = '-r' ]; then
        git checkout "$2" && \
        python3 ${project_root}/code/main.py --exper "$2"
    else
        git add -A ${project_root} 
        git commit -m "experiment | $2" && \
        git tag -a "$1" -m "experiment" && \
        python3 ${project_root}/code/main.py --exper "$1"
    fi
}
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
