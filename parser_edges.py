#!/usr/bin/env python
import os
import conf


def edges_reader(fname):
    assert (os.path.isfile(fname))
    assert (fname.endswith('.edges'))
    edge_list = []
    with open(fname) as f:
        for line in f:
            node_list = [int(elem) for elem in line.split()]
            edge_list.append(tuple(node_list))
    return edge_list


if __name__ == '__main__':
    fname = os.path.join(conf.data_dir, '0.edges')
    for edge in edges_reader(fname):
        print(edge)
