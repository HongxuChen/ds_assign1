#!/usr/bin/env python
from __future__ import print_function
import os
import time

curdir = os.path.abspath(os.path.dirname(__file__))
combined_fname = 'combined.gz'
ext_list = ['circles', 'edges', 'egofeat', 'feat', 'featnames']

graph_directness = {
    'facebook': False,
    'dblp': False,
    'twitter': True
}


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('- {:40} took {:2.6f}s'.format(method.__name__, te - ts))
        return result

    return timed


def get_data_dir(name):
    return os.path.join(curdir, name)


def get_gzip_fname(name):
    data_dir = get_data_dir(name)
    return os.path.join(data_dir, combined_fname)


def collect_ego_list(name):
    ego_list = []
    data_dir = get_data_dir(name)
    for f in os.listdir(data_dir):
        if f.endswith('.circles'):
            base = os.path.splitext(f)[0]
            ego_list.append(int(base))
    return ego_list


def collect_ego_set(name):
    l = collect_ego_list(name)
    if l is None or len(l) == 0:
        return None
    return l


def size_counter(name):
    data_dir = get_data_dir(name)
    for f in os.listdir(data_dir):
        if f.endswith('.circles'):
            base = os.path.splitext(f)[0]
            for ext in ext_list:
                fname = base + '.' + ext
                fpath = os.path.join(data_dir, fname)
                assert os.path.isfile(fpath)
                statinfo = os.stat(fpath)
                print('{:20s} {}'.format(fname, statinfo.st_size))
