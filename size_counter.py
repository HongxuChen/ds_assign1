#!/usr/bin/env python
from __future__ import print_function

import os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'facebook'))

ext_list = ['circles', 'edges', 'egofeat', 'feat', 'featnames']

for f in os.listdir(data_dir):
    if f.endswith('.circles'):
        base = os.path.splitext(f)[0]
        for ext in ext_list:
            fname = base + '.' + ext
            fpath = os.path.join(data_dir, fname)
            assert os.path.isfile(fpath)
            statinfo = os.stat(fpath)
            print('{:20s} {}'.format(fname, statinfo.st_size))
