#!/usr/bin/env python
from __future__ import print_function

import networkx as nx


class GraphInfo(object):
    def __init__(self, graph):
        self.graph = graph

    def info(self):
        print(len(self.graph.nodes()))
        print(len(self.graph.edges()))
        # print(nx.clustering(self.graph))
        print(nx.average_clustering(self.graph))
        print(sum(1 for _ in nx.find_cliques(self.graph)))
