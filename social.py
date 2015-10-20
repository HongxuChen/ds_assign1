#!/usr/bin/env python

from __future__ import print_function
import os

import networkx as nx
import conf

import ego
from graph_info import GraphInfo
import log_helper


class Social(object):
    def __init__(self, ego_list):
        self.ego_list = ego_list
        self.graph = nx.Graph()
        self.generate_from_ego()

    def generate_from_ego(self):
        for ego_id in self.ego_list:
            ego_graph = ego.Ego(ego_id)
            ego_graph.graph_generator()
            graph = ego_graph.graph
            self.graph.add_nodes_from(graph.nodes())
            self.graph.add_edges_from(graph.edges())

    @staticmethod
    def collect_ego_list():
        ego_list = []
        data_dir = conf.data_dir
        for f in os.listdir(data_dir):
            if f.endswith('.circles'):
                base = os.path.splitext(f)[0]
                ego_list.append(int(base))
        return sorted(ego_list)


if __name__ == '__main__':
    log_helper.init_logger()
    ego_list = Social.collect_ego_list()
    social = Social(ego_list)
    g_info = GraphInfo(social.graph)
    g_info.info()
