#!/usr/bin/env python
import os

import conf


def collect_ego_list():
    ego_list = []
    data_dir = conf.data_dir
    for f in os.listdir(data_dir):
        if f.endswith('.circles'):
            base = os.path.splitext(f)[0]
            ego_list.append(int(base))
    return ego_list


def collect_ego_set():
    return set(collect_ego_list())


def size_counter():
    for f in os.listdir(conf.data_dir):
        if f.endswith('.circles'):
            base = os.path.splitext(f)[0]
            for ext in conf.ext_list:
                fname = base + '.' + ext
                fpath = os.path.join(conf.data_dir, fname)
                assert os.path.isfile(fpath)
                statinfo = os.stat(fpath)
                print('{:20s} {}'.format(fname, statinfo.st_size))
