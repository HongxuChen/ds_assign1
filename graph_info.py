#!/usr/bin/env python
from __future__ import print_function

import operator

import networkx as nx
import conf
import social
import utils


class GraphInfo(object):
    def __init__(self, graph):
        self.graph = graph

    def separation(self):
        pass

    def clustering(self):
        return nx.average_clustering(self.graph)

    def shortest_paths(self):
        # diameter
        shortest_path_dict_dict = nx.all_pairs_shortest_path_length(self.graph)
        diameter = 0
        for shortest_path_dict in shortest_path_dict_dict.values():
            current_shortest = sorted(shortest_path_dict.values(), reverse=True)[0]
            if diameter < current_shortest:
                diameter = current_shortest
        return diameter

    def connected_component(self):
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

    def triangles(self):
        triangles_dict = nx.triangles(self.graph)
        print('triangles: {}'.format(sum([v for v in triangles_dict.values()])))

    def info(self):
        print('nodes: {}'.format(len(self.graph.nodes())))
        print('edges: {}'.format(len(self.graph.edges())))
        print('diameter: {}'.format(self.shortest_paths()))
        print('Average clustering coefficient {}'.format(self.clustering()))
        print('degrees\n{}'.format(self.degrees()))

    def degrees(self, ego_set=None):
        degree_dict = self.graph.degree()
        sorted_degrees = sorted(degree_dict.items(), key=operator.itemgetter(1), reverse=True)
        if ego_set is None:
            return sorted_degrees
        filtered = []
        for e in sorted_degrees:
            if e[0] in ego_set:
                filtered.append(e)
        return filtered


if __name__ == '__main__':
    s = social.Social.from_combined(conf.gzip_file)
    ego_set = utils.collect_ego_set()
    g_info = GraphInfo(s.graph)
    print(g_info.degrees(ego_set))
