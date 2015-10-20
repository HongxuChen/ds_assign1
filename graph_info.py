#!/usr/bin/env python
from __future__ import print_function

import networkx as nx


class GraphInfo(object):
    def __init__(self, graph):
        self.graph = graph

    def info(self):
        print('nodes: {:>50}'.format(len(self.graph.nodes())))
        print('edges: {:>50}'.format(len(self.graph.edges())))
        print('Average clustering coefficient {:>50}'.format(nx.average_clustering(self.graph)))
        # print(nx.clustering(self.graph))
        # diameter
        # shortest_path_dict_dict = nx.all_pairs_shortest_path_length(self.graph)
        # diameter = 0
        # for shortest_path_dict in shortest_path_dict_dict.values():
        #     current_shortest = sorted(shortest_path_dict.values(), reverse=True)[0]
        #     if diameter < current_shortest:
        #         diameter = current_shortest
        # print('diameter: {}'.format(diameter))
        # triangles
        triangles_dict = nx.triangles(self.graph)
        print('triangles: {}'.format(sum([v for v in triangles_dict.values()])))

        if self.graph.is_directed():
            edges_in_wcc = set()
            nodes_in_wcc = set()
            wcc_counter = 0
            for wcc in nx.weakly_connected_components(self.graph):
                wcc_counter += 1
                print(type(wcc))
                nodes_in_wcc.add(wcc.nodes())
                edges_in_wcc.add(wcc.edges())
