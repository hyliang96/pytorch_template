#!/usr/bin/env bash
if [ "$1" = 'help' ] || [ "$1" = '--help' ] || [ "$1" = '-h' ]; then
    echo "Usage:"
    echo "gpuid [n,m,...] run.sh [experiment_name]"
    echo "gpuid [n,m,...] run.sh --rerun [experiment_name]"
elif [ "$1" = '--rerun' ]; then
    python3 main.py --exper "$2"
else
    git add -A ../ && \
    git commit -m "experiment" && \
    git tag -a "$1" -m "experiment" && \
    python3 main.py --exper "$1"
fi