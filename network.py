#!/usr/bin/env python

from __future__ import print_function
import gzip
import os

import networkx as nx
import pickle

import ego
import graph_info
import log_helper
import utils


# noinspection PyPep8Naming
class Network(object):
    _logger = log_helper.get_logger()

    @utils.timeit
    def __init__(self, graph):
        self.graph = graph

    @classmethod
    def from_combined(cls, name, gzip_file):
        if utils.graph_directness[name]:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        pickle_file = os.path.splitext(gzip_file)[0] + '.pickle'
        if os.path.isfile(pickle_file):
            Network._logger.info('pickle {} exists, loading'.format(pickle_file))
            with open(pickle_file, 'rb') as pickle_data:
                G = pickle.load(pickle_data)
        else:
            Network._logger.info('pickle {} not exists, creating'.format(pickle_file))
            with gzip.open(gzip_file, 'r') as gzip_data:
                for l in gzip_data:
                    edges = [int(e) for e in l.split()]
                    assert (len(edges) == 2)
                    G.add_edge(*edges)
            with open(pickle_file, 'wb') as pickle_data:
                pickle.dump(G, pickle_data)
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
