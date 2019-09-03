#!/usr/bin/env bash

if [ "$1" = 'help' ] || [ "$1" = '--help' ] || [ "$1" = '-h' ]; then
    echo "Usage:"
    echo "gpuid [n,m,...] run.sh [experiment_name]         : commit a new experiment and tag it with its name"
    echo "gpuid [n,m,...] run.sh --rerun(-r) [experiment_name] : git checkout old tag and rerun the experiment"
elif [ "$1" = '--rerun' ] || [ "$1" = '-r' ]; then
    git checkout "$2" && \
    python3 main.py --exper "$2"
else
    git add -A ../ && \
    git commit -m "experiment" && \
    git tag -a "$1" -m "experiment" && \
    python3 main.py --exper "$1"
fi