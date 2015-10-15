#!/usr/bin/env python
from __future__ import print_function

import os
import conf

for f in os.listdir(conf.data_dir):
    if f.endswith('.circles'):
        base = os.path.splitext(f)[0]
        for ext in conf.ext_list:
            fname = base + '.' + ext
            fpath = os.path.join(conf.data_dir, fname)
            assert os.path.isfile(fpath)
            statinfo = os.stat(fpath)
            print('{:20s} {}'.format(fname, statinfo.st_size))
