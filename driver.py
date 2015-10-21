#!/usr/bin/env python
import conf
from graph_info import GraphInfo
from partitioner import Partitioner
import social
import utils


def run_once(p, partitions, node_set):
    locality = [p.locality_percentage(partition, node_set) for partition in partitions]
    print(locality)


def run(step):
    s = social.Social.from_combined(conf.gzip_file)
    p = Partitioner(s.graph)
    graph_info = GraphInfo(s.graph)
    cd_partition = p.community_detection()
    parts = len(cd_partition)
    metis_partition = p.metis_partition(parts)
    rnd_partition = p.random_partition(parts)
    partitions = [cd_partition, metis_partition, rnd_partition]

    ego_set = utils.collect_ego_set()
    print('for ego_set')
    run_once(p, partitions, ego_set)

    percentage_list = [float(i) / step for i in xrange(1, step + 1)]
    node_num = len(s.graph.nodes())
    sorted_degree = graph_info.sorted_degree
    for percent in percentage_list:
        number = int(node_num * percent)
        print('for percentage={} nodes={}'.format(percent, number))
        sliced_nodes = sorted_degree[:number]
        node_set = set()
        for n, d in sliced_nodes:
            node_set.add(n)
        run_once(p, partitions, node_set)


if __name__ == '__main__':
    run(5)
