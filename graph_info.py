#!/usr/bin/env python
from __future__ import print_function

import operator

import networkx as nx

import network
import utils
from utils import timeit


class GraphInfo(object):
    def __init__(self, graph):
        self.graph = graph
        self.init()

    @timeit
    def _clustering(self):
        return nx.average_clustering(self.graph)

    @timeit
    def _diameter(self):
        shortest_path_dict_dict = nx.all_pairs_shortest_path_length(self.graph)
        diameter = 0
        for shortest_path_dict in shortest_path_dict_dict.values():
            current_shortest = sorted(shortest_path_dict.values(), reverse=True)[0]
            if diameter < current_shortest:
                diameter = current_shortest
        return diameter

    def _connected_component(self):
        if self.graph.is_directed():
            edges_in_wcc = set()
            nodes_in_wcc = set()
            wcc_counter = 0
            for wcc in nx.weakly_connected_components(self.graph):
                wcc_counter += 1
                print(type(wcc))
                nodes_in_wcc.add(wcc.nodes())
                edges_in_wcc.add(wcc.edges())
        else:  # undirected
            scc_counter = 0
            for scc in nx.strongly_connected_components(self.graph):
                scc_counter += 0
                print(type(scc))

    def _triangles(self):
        triangles_dict = nx.triangles(self.graph)
        return sum([v for v in triangles_dict.values()])

    @timeit
    def _sorted_degrees(self, ego_set=None):
        degree_dict = self.graph.degree()
        sorted_degrees = sorted(degree_dict.items(), key=operator.itemgetter(1), reverse=True)
        if ego_set is None:
            return sorted_degrees
        filtered = []
        for e in sorted_degrees:
            if e[0] in ego_set:
                filtered.append(e)
        return filtered

    # noinspection PyAttributeOutsideInit
    def init(self):
        self.node_num = len(self.graph.nodes())
        self.edge_num = len(self.graph.edges())
        self.sorted_degree = self._sorted_degrees()

    # noinspection PyAttributeOutsideInit
    def dump_info(self):
        self.diameter = self._diameter()
        self.clustering_efficient = self._clustering()
        print('nodes: {}'.format(self.node_num))
        print('edges: {}'.format(self.edge_num))
        print('diameter: {}'.format(self.diameter))
        print('Average clustering coefficient {}'.format(self.clustering_efficient))


if __name__ == '__main__':
    name = 'facebook'
    gzip_file = utils.get_gzip_fname(name)
    s = network.Network.from_combined(name, gzip_file)
    ego_set = utils.collect_ego_set(name)
    g_info = GraphInfo(s.graph)
    g_info.dump_info()
