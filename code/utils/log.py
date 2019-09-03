#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import time
import tqdm as tq
# from tqdm import tqdm

# 支持在python2、3下调用本文件


class Log(object):

# 用例
# 从log = Log('test_data')开始，print会向文件'test_data'与屏幕输出（双向输出）
# 包括：
#   - 凡print函数皆双向输出
#     - 此处代码中的print
#     - 被调用的函数中有print
#     - 被import的文件中有print
#   - 支持输出到文件、屏幕的flush()
#   - 不支持'\r'输出到文件（vim下'\r'会显示为^M），支持'\r'输出到文件，故进度条只能在屏幕上显示
# 直到log.close()，print才变为只输出到屏幕

# 可配合tqdm使用，tqdm 在屏幕上清屏进度条，则输出到log文件也清屏进度条

    def __init__(self, filename='', mode='w'):
        # filename =
         # time.strftime("%m-%d_%H:%M:%S", time.localtime())+filename
        self.f = open(filename, mode)
        sys.stdout = self
        print('====== log start ======',
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            # 格式化成2016-03-20 11:45:39形式
            '======')

    def write(self, data):
        self.f.write(data)
        sys.__stdout__.write(data)

    def flush(self):
        # 例
        #   print("xxxx", end='')
        #   log.flush()
        # 可使"xxxx"立即输出到屏幕和文件；
        # 若不"log.flush()"，则要等到之后有换行的 print("xxxx")
        self.f.flush()
        sys.__stdout__.flush()

    def close(self):
        print('======= log end =======',
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            '======')
        self.flush()
        self.f.close()
        sys.stdout=sys.__stdout__

def cursor_back(func):
    # 光标回到所在行首，且只输出到屏幕，不输出到别处
        # 因为在屏幕是上，'\r'可令光标返回行首，但本行已输出的字符不会删除
        # 但在文件中，'\r'显示为"^M" 或 "<0x0d>"，不能返回光标到行首
    def func_with_cursor_back(*args, **kw):
        # 以防之前stdout修改，如"屏幕、文件双向输出"功能
        original = sys.stdout
        sys.stdout = sys.__stdout__
        # 光标回到所在行首
        result = func(*args, **kw)
        print("\r",end="")
        sys.stdout.flush()
        # 还原sys.stdout
        sys.stdout.flush()
        sys.stdout = original

        return result
    return func_with_cursor_back


