#!/usr/bin/env bash

# get absoltae path to the dir this is in, work in bash, zsh
# if you want transfer symbolic link to true path, just change `pwd` to `pwd -P`
project_root=$(cd "$(dirname "${BASH_SOURCE[0]-$0}")"/..; pwd)
project_venv="$project_root/code/venv"

. ${project_root}/code/utils/statistic/source.sh


if ! [ -d "$project_venv" ]; then
    echo 'there is no virtualenv at'"$project_venv" >&2
    echo 'install it by running `install_venv`'
else
    source "$project_venv/bin/activate"
fi

install_venv() {
    ( ! [ -d "$project_venv" ] ) && \
        virtualenv --no-site-packages -p python3 $project_venv
    source "$project_venv/bin/activate"
    python -m pip install -r $project_root/code/requirements.txt
    python -m pretty_errors -s -p
    ln -sf $project_root/code/utils/pretty_errors.pth  $(py -m pretty_errors -f | grep pretty_errors.pth)
}

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
    local continue=''
    local fix_seed=false

    # 参数预处理
    TEMP=$(getopt \
        -o      rfch \
        --long  rerun,fix-seed,continue,help \
        -n      'arg parse error' \
        -- "$@")
    # 写法
        #   -o     短参数 不需要分隔符
        #   --long 长参数 用','分隔
        #   ``无选项  `:`必有选项  `::` 可有选项
    if [ $? != 0 ] ; then echo "exiting for arg parse error\n" >&2;  run --help ; return ; fi
    eval set -- "$TEMP" # 将$TEMP复制给 $1, $2, ...


    # 处理参数
    while true ; do case "$1" in
        # 无选项
        -h|--help)      help=true; shift ;;
        -r|--rerun)     rerun=true ; shift ;;
        -c|--continue)  continue='--continue_train' ; shift ;;
        -f|--fix-seed)  fix_seed=true ; shift ;;
        # 处理格式化的参数
        # '--'后是 余参数
        --) shift ; break ;;
        # 处理参数的代码错误
        *) echo "arg parse error" ; return ;;
    esac ; done

    if [ "$help" = true ]; then
        echo "Usage: only usable under a git commited status"
        echo "gpuid [n,m,...] run  -r|--rerun     <experiment_tag>   : git checkout an old experiment with tag and rerun it"
        echo "gpuid [n,m,...] run [-f|--fix-seed] <experiment_tag>   : git tag and run a new experiment"
        echo "   -f|--fix-seed  : fix the random seed as file \`./code/seed\` has. If the file does not exist, write 0 into it."
        return
    fi

    if [ $# -ne 1 ]; then echo 'arg parse error: no <experiment_tag> input\n' >&2 ; run --help ; return ; fi
    local tag="$1"; shift

    # 若当前没有commit，则不可run
    if ! [[ "$(cd ${project_root} && git status)" =~ 'nothing to commit, working directory clean' ]]; then
        echo 'Please commit or stash before run experiment'
        return
    fi

    if [ "$rerun" = true ] || [ "$continue" != '' ]; then
        if [ "$(_tag_exist $tag)" = false ]; then echo "$tag not exists"; return; fi # 若tag是未有的，则报错，退出
        git checkout "$tag" && \
        python3 ${project_root}/code/main.py --exper "$tag" $continue
    else
        if [ "$(_tag_exist $tag)" = true ]; then echo "$tag is existing"; return; fi # 若tag是已有的，则报错，退出
        # 生成随机数文件

        local seed_file="${project_root}/code/seed"
        if [ "$fix_seed" = true ]; then
            ( ! [ -f "$seed_file" ] ) &&  echo 0 > $seed_file
        else
            echo $RANDOM > $seed_file
        fi
        # 若随机数文件变动，则commit一版
        if ! [[ "$(cd ${project_root} && git status)" =~ 'nothing to commit, working directory clean' ]]; then
            git add -A ${project_root} &&
            git commit -m "run"
        fi
        # 加标签 运行
        git tag -a "$tag" -m "run" && \
        python3 ${project_root}/code/main.py --exper "$tag"
    fi
}


alias rerun='run --rerun'
alias re='rerun'
alias continue='run --continue'
alias con='continue'

expls()
{
    echo $project_root/__result__
    local epxertag
    if [ $# -eq 0 ]; then
        ls $project_root/__result__
    elif [ "$1" = '-r' ]; then
        for epxertag in $(ls $project_root/__result__); do
            echo -n "    $epxertag:  "
            ls $project_root/__result__/$epxertag
        done
    else
        for epxertag in "$@"; do
            echo -n "    $epxertag:  "
            ls $project_root/__result__/$epxertag
        done
    fi
}


# if [ -n "$ZSH_VERSION" ]; then
#     ls_itb() { : }
#     compdef _ls ls_itb
#     alias itb="ls_itb ${project_root}/__result__"
# fi

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
            local dir_path="${project_root}/__result__/$exper_name"
        fi
        local dir_arg="${dir_arg}${exper_name}:${dir_path},"
    done
    dir_arg="${dir_arg:0:-1}"

    tensorboard $dir_arg $@
}


# release this variable in the end of file
# unset -v here
