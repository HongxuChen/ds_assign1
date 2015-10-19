#!/usr/bin/env python
from __future__ import print_function
import os
import conf
import networkx as nx
import matplotlib.pyplot as plt


class Graph(object):
    def __init__(self, node_id):
        self.node_id = str(node_id)
        self.dir = conf.data_dir
        self.graph = nx.Graph()

    def get_fname(self, ext):
        fname = self.node_id + '.' + ext
        return os.path.join(self.dir, fname)

    def circles_reader(self):
        fname = self.get_fname('circles')
        assert (os.path.isfile(fname))
        with open(fname) as f:
            for line in f:
                id_list = line.split()[1:]
                yield [int(item) for item in id_list]

    def info(self):
        pass
        # print(sum(1 for _ in nx.find_cliques(self.graph)))
        # print(len(list(nx.find_cliques(self.graph))))
        # print(nx.clustering(self.graph))
        # print(nx.max_clique(self.graph))

    def graph_generator(self):
        edges = self.edges_reader()
        self.graph.add_edges_from(edges)
        for n in self.graph.nodes():
            self.graph.add_edge(self.node_id, n)

    def save_figure(self, fmt='pdf'):
        pos = nx.spectral_layout(self.graph)
        nx.draw_networkx(self.graph, pos)
        fname = self.get_fname(fmt)
        plt.savefig(fname)

    def edges_reader(self):
        fname = self.get_fname('edges')
        assert (os.path.isfile(fname))
        edge_list = []
        with open(fname) as f:
            for line in f:
                node_list = [int(elem) for elem in line.split()]
                edge_list.append(tuple(node_list))
        return edge_list

    def feat_reader(self):
        fname = self.get_fname('feat')
        assert (os.path.isfile(fname))
        with open(fname) as f:
            for line in f:
                digit_str_list = line.split()
                digits = [int(elem) for elem in digit_str_list][1:]
                yield digits


if __name__ == '__main__':
    g = Graph(0)
    graph = g.graph
    g.graph_generator()
    l = len(graph.nodes())
    # l = len(g.graph.edges())
    # print(l)
    g.info()
    # g.save_figure()
