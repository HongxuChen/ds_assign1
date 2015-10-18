#!/usr/bin/env python
"""
Read and write graphs.
"""

import sys

from networkx import grid_2d_graph, write_adjlist, write_edgelist, read_edgelist

G = grid_2d_graph(5, 5)  # 5x5 grid
try:  # Python 2.6+
    write_adjlist(G, sys.stdout)  # write adjacency list to screen
except TypeError:  # Python 3.x
    write_adjlist(G, sys.stdout.buffer)  # write adjacency list to screen
# write edgelist to grid.edgelist
write_edgelist(G, path="grid.edgelist", delimiter=":")
# read edgelist from grid.edgelist
H = read_edgelist(path="grid.edgelist", delimiter=":")
