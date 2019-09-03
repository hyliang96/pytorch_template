#!/usr/bin/env bash

git add -A .
git commit -m "experiment"
git tag -a "$1"
python3 main.py --exper "$1"