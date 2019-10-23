# get absoltae path to the dir this is in, work in bash, zsh
# if you want transfer symbolic link to true path, just change `pwd` to `pwd -P`
statistic_source=$(cd "$(dirname "${BASH_SOURCE[0]-$0}")"; pwd)


alias record="python $statistic_source/add_to_record.py"


# release this variable in the end of file
unset -v statistic_source