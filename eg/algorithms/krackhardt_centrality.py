#!/usr/bin/env python
"""
Centrality measures of Krackhardt social network.
"""

from networkx import *

G = krackhardt_kite_graph()

print("Betweenness")
b = betweenness_centrality(G)
for v in G.nodes():
    print("%0.2d %5.3f" % (v, b[v]))

print("Degree centrality")
d = degree_centrality(G)
for v in G.nodes():
    print("%0.2d %5.3f" % (v, d[v]))

print("Closeness centrality")
c = closeness_centrality(G)
for v in G.nodes():
    print("%0.2d %5.3f" % (v, c[v]))
