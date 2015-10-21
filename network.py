#!/usr/bin/env python

from __future__ import print_function
import gzip

import networkx as nx

import ego
import graph_info
import log_helper
import utils


# noinspection PyPep8Naming
class Network(object):
    def __init__(self, graph):
        self.graph = graph

    @classmethod
    def from_combined(cls, name, gzip_file):
        if utils.graph_directness[name]:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        with gzip.open(gzip_file, 'r') as gzip_data:
            for l in gzip_data:
                edges = [int(e) for e in l.split()]
                assert (len(edges) == 2)
                G.add_edge(*edges)
        return cls(G)

    @classmethod
    def from_ego(cls, name, ego_list):
        if utils.graph_directness[name]:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        for ego_id in ego_list:
            ego_graph = ego.Ego(name, ego_id)
            ego_graph.graph_generator()
            graph = ego_graph.graph
            G.add_nodes_from(graph.nodes())
            G.add_edges_from(graph.edges())
        return cls(G)


if __name__ == '__main__':
    log_helper.init_logger()
    name = 'facebook'
    ego_list = utils.collect_ego_list(name)
    gzip_fname = utils.get_gzip_fname(name)
    social = Network.from_combined(name, gzip_fname)
    g_info = graph_info.GraphInfo(social.graph)
