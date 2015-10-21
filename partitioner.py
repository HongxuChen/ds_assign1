#!/usr/bin/env python
from __future__ import print_function
from collections import defaultdict
import random

import community

import nxmetis

import network
import utils


class Partitioner(object):
    def __init__(self, graph):
        self.graph = graph

    @utils.timeit
    def community_detection(self):
        partition = community.best_partition(self.graph)
        cd_dict = defaultdict(set)
        for p in partition:
            cd_dict[partition[p]].add(p)
        return cd_dict.values()

    @utils.timeit
    def metis_partition(self, parts):
        edgecuts, metis_list = nxmetis.partition(self.graph, parts)
        metis_set_list = [set(l) for l in metis_list]
        return metis_set_list

    @utils.timeit
    def random_partition(self, parts):
        node_list = self.graph.nodes()
        random.shuffle(node_list)

        def chunks(l, n):
            for i in xrange(0, len(l), n):
                yield set(l[i:i + n])

        rnd_list = list(chunks(node_list, len(node_list) / parts))
        return rnd_list

    def get_neighbor_set(self, node_id):
        neighbor_list = self.graph.neighbors(node_id)
        return set(neighbor_list)

    def get_local_set(self, partition_list, node_id):
        for partition_set in partition_list:
            if node_id in partition_set:
                neighbor_set = self.get_neighbor_set(node_id)
                local_set = neighbor_set.intersection(partition_set)
                return local_set
        assert (False and 'node_id={}'.format(node_id))

    def locality_percentage(self, partition_list, note_set):
        local = 0
        total = 0
        for node_id in note_set:
            local_set_size = self.get_local_set(partition_list, node_id)
            local += len(local_set_size)
            total += len(self.graph.neighbors(node_id))
        return float(local) / float(total)

    @staticmethod
    def dump_partition(partition_list):
        for d in partition_list:
            print(d)


if __name__ == '__main__':
    name = 'facebook'
    gzip_fname = utils.get_gzip_fname('facebook')
    s = network.Network.from_combined(name, gzip_fname)
    p = Partitioner(s.graph)
    cd_partition = p.community_detection()
    parts = len(cd_partition)
    ego_list = utils.collect_ego_list(name)
    print(ego_list)
    cd_locality = p.locality_percentage(cd_partition, ego_list)
    print(cd_locality)
    metis_partition = p.metis_partition(parts)
    metis_locality = p.locality_percentage(metis_partition, ego_list)
    print(metis_locality)
    rnd_partition = p.random_partition(parts)
    rnd_locality = p.locality_percentage(rnd_partition, ego_list)
    print(rnd_locality)
