#!/usr/bin/env python
"""
Compute some network properties for the lollipop graph.
http://mathworld.wolfram.com/LollipopGraph.html
"""
from networkx import *
import matplotlib.pyplot as plt

G = lollipop_graph(4, 6)

pathlengths = []

print("source vertex {target:length, }")
for v in G.nodes():
    spl = single_source_shortest_path_length(G, v)
    print('%s %s' % (v, spl))
    for p in spl.values():
        pathlengths.append(p)

print('')
print("average shortest path length %s" % (sum(pathlengths) / len(pathlengths)))

# histogram of path lengths 
dist = {}
for p in pathlengths:
    if p in dist:
        dist[p] += 1
    else:
        dist[p] = 1

print('')
print("length #paths")
verts = dist.keys()
for d in sorted(verts):
    print('%s %d' % (d, dist[d]))

print("radius: %d" % radius(G))
print("diameter: %d" % diameter(G))
print("eccentricity: %s" % eccentricity(G))
print("center: %s" % center(G))
print("periphery: %s" % periphery(G))
print("density: %s" % density(G))

pos = spring_layout(G)
draw_networkx(G, pos)
plt.show()
