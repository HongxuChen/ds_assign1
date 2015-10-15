#!/usr/bin/env python
import os
import conf


def circles_reader(fname):
    assert (os.path.isfile(fname))
    assert (fname.endswith('.circles'))
    with open(fname) as f:
        for line in f:
            id_list = line.split()[1:]
            yield [int(item) for item in id_list]


fname = os.path.join(conf.data_dir, '0.circles')

for id_list in circles_reader(fname):
    print(id_list)
