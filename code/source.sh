#!/usr/bin/env bash

# get absoltae path to the dir this is in, work in bash, zsh
# if you want transfer symbolic link to true path, just change `pwd` to `pwd -P`
project_root=$(cd "$(dirname "${BASH_SOURCE[0]-$0}")"/..; pwd)

. ${project_root}/code/utils/statistic/source.sh


_tag_exist()
{
    local tag="$1"
    local existing_tag=false
    for i in $(git tag); do
        if [ "$i" = "$tag"  ]; then
            existing_tag=true
        fi
    done
    echo $existing_tag
}

run()
{

    # 使用规则
    # bash/zsh getopt_demo.sh 一堆参数，其前中后均可有 余参数
    # 格式化参数：以'-'开头，必需符合本代码的解析要求
        #             短参数                           长参数
        # 无选项       -a                              --a-long
        # 必有选项     -bss          -b ss             --b-long ss
        #             -b'sds sds'   -b 'sds sds'      --b-long 'sds sds'
        # 可有选项若无  -c                              --c-long
        # 可有选项若有  -css          -c'sds sds'  只可短参数，选项与参数间不得有空格
    # 余参数：不以'-'开头

    local help=false
    local rerun=false
    local fix_seed=false

    # 参数预处理
    TEMP=$(getopt \
        -o      rfh \
        --long  rerun,fix-seed,help \
        -n      '参数解析错误' \
        -- "$@")
    # 写法
        #   -o     短参数 不需要分隔符
        #   --long 长参数 用','分隔
        #   ``无选项  `:`必有选项  `::` 可有选项
    if [ $? != 0 ] ; then echo "格式化的参数解析错误，正在退出" >&2; run --help ; exit 1 ; fi
    eval set -- "$TEMP" # 将$TEMP复制给 $1, $2, ...


    # 处理参数
    while true ; do case "$1" in
        # 无选项
        -h|--help)      help=true; shift ;;
        -r|--rerun)     rerun=true ; shift ;;
        -f|--fix-seed)  fix_seed=true ; shift ;;
        # 处理格式化的参数
        # '--'后是 余参数
        --) shift ; break ;;
        # 处理参数的代码错误
        *) echo "参数处理错误" ; exit 1 ;;
    esac ; done

    local tag="$1"; shift

    if [ "$help" = true ]; then
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

    if [ "$rerun" = true ]; then
        if [ "$(_tag_exist $tag)" = false ]; then echo "$tag not exists"; return; fi # 若tag是未有的，则报错，退出
        git checkout "$tag" && \
        python3 ${project_root}/code/main.py --exper "$tag"
    else
        if [ "$(_tag_exist $tag)" = true ]; then echo "$tag is existing"; return; fi # 若tag是已有的，则报错，退出
        # 生成随机数文件

        local seed_file="${project_root}/code/seed"
        if [ "$fix_seed" = true ]; then
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
