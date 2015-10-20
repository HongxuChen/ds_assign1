#!/usr/bin/env python

import networkx as nx

import ego


class Social(object):
    def __init__(self, ego_list):
        self.ego_list = ego_list
        self.graph = nx.Graph()

    def generate_from_ego(self):
        for ego_id in self.ego_list:
            ego_graph = ego.Ego(ego_id)
            graph = ego_graph.graph_generator()
            self.graph.add_nodes_from(graph)
            self.graph.add_edges_from(graph)
            