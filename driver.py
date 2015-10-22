#!/usr/bin/env python

from __future__ import print_function

from graph_info import GraphInfo
from partitioner import Partitioner
import network
import utils


def get_locality(p, partitions, node_set):
    assert (node_set is not None and len(node_set) != 0)
    locality = [p.locality_percentage(partition, node_set) for partition in partitions]
    return locality


def dump_locality(p, partitions, node_set):
    locality = get_locality(p, partitions, node_set)
    s = [str(l) for l in locality]
    print(', '.join(s))


def locality_with_ego(name, p, partitions):
    ego_set = utils.collect_ego_set(name)
    if ego_set is not None:
        print('ego_set', end='\t')
        dump_locality(p, partitions, ego_set)


def locality_with_degrees(graph, p, partitions, step):
    percentage_list = [float(i) / step for i in xrange(1, step + 1)]
    graph_info = GraphInfo(graph)
    node_num = len(graph.nodes())
    sorted_degree = graph_info.sorted_degree
    for percent in percentage_list:
        number = int(node_num * percent)
        print('percentage={} nodes={}'.format(percent, number), end='\t')
        sliced_nodes = sorted_degree[:number]
        node_set = set()
        for n, d in sliced_nodes:
            node_set.add(n)
        dump_locality(p, partitions, node_set)


def experiment1(name, step):
    gzip_fname = utils.get_gzip_fname(name)
    s = network.Network.from_combined(name, gzip_fname)
    p = Partitioner(s.graph)
    cd_partition = p.community_detection()
    parts = len(cd_partition)
    print('community parts: {}'.format(parts))
    metis_partition = p.metis_partition(parts)
    rnd_partition = p.random_partition(parts)

    partitions = [cd_partition, metis_partition, rnd_partition]
    locality_with_ego(name, p, partitions)
    locality_with_degrees(s.graph, p, partitions, step)


def experiment2(name, step, max_partition):
    gzip_fname = utils.get_gzip_fname(name)
    s = network.Network.from_combined(name, gzip_fname)
    graph = s.graph
    p = Partitioner(graph)

    for parts in range(2, max_partition):
        print('\nparts={}'.format(parts))
        metis_partition = p.metis_partition(parts)
        rnd_partition = p.random_partition(parts)
        partitions = [metis_partition, rnd_partition]
        locality_with_degrees(graph, p, partitions, step)


if __name__ == '__main__':
    # experiment1('facebook', 5)
    experiment2('dblp', 5, 8)
