#!/usr/bin/env python

from __future__ import print_function

from graph_info import GraphInfo
from partitioner import Partitioner
import network
import utils

import matplotlib.pyplot as plt
import numpy as np
import pylab
from matplotlib.font_manager import FontProperties

markers = '+*.o'
colors = 'rgb'
label = ['Community Detection', 'Metis', 'Random']


def single_locality(p, partition, node_set):
    assert (node_set is not None and len(node_set) != 0)
    return p.locality_percentage(partition, node_set)


def plot1(name, xlist, ylist):
    pylab.grid(True)
    for i in xrange(len(ylist)):
        plt.plot(xlist, ylist[i], colors[i % len(colors)], marker=markers[i % len(markers)])
    plt.legend(label, loc='center right')
    plt.xlim(xlist[0] / 2, xlist[-1] + xlist[0] / 2)
    plt.xlabel('Node Set Percentage')
    plt.ylabel('Locality Percentage')
    plt.title('{}: step={}'.format(name, len(xlist)))
    fname = name + '_exp1'
    plt.savefig('{}.png'.format(fname))


def plot2(name, labels, xlist, ylist):
    pylab.grid(True)
    for i in xrange(len(ylist)):
        plt.plot(xlist, ylist[i], colors[i % len(colors)], marker=markers[i % len(markers)])

    plt.legend(labels, loc='center right')
    plt.xlim(xlist[0] / 2, xlist[-1] + xlist[0] / 2)
    plt.xlabel('Number of Parts')
    plt.ylabel('Locality Percentage')
    plt.title('{}: Average Localities for different Parts'.format(name))
    fname = name + '_exp2'
    plt.savefig('{}.png'.format(fname))


def plot1_bar(name, xlist, ylist):
    pylab.grid(True)
    width = 0.15
    ind = np.arange(len(xlist))
    fig, ax = plt.subplots()
    for i in xrange(len(ylist)):
        ax.bar(ind + i * width, ylist[i], width, color=colors[i % 3])
    ax.set_xticks(ind + width)
    ax.set_xticklabels(xlist)
    ax.legend(label, loc='center')
    plt.title('{}: step={}'.format(name, len(xlist)))
    fname = name + '_exp1_bar.png'
    plt.savefig(fname)


def plot2_random_partition(name, xlist, ylist):
    yy = []
    for x, y in zip(xlist, ylist):
        yy.append(x * y)
    print(yy)
    plt.plot(xlist, yy)
    plt.xlabel('Parts')
    plt.ylabel('Locality * Parts')
    plt.title('{}: Random Partition Locality'.format(name))
    plt.ylim([0.5, 1.5])
    pylab.grid(True)
    fname = name + '_rnd.png'
    plt.savefig(fname)


def get_locality_partition_list(graph_info, p, partitions, step):
    graph = graph_info.graph
    node_num = len(graph.nodes())
    sorted_degree = graph_info.sorted_degree
    percentage_list = [float(i) / step for i in xrange(1, step + 1)]
    num_list = [int(percent * node_num) for percent in percentage_list]
    localities = []
    for partition in partitions:
        locality_for_partition = []
        for num in num_list:
            sliced_nodes = sorted_degree[:num]
            node_set = set()
            for n, d in sliced_nodes:
                node_set.add(n)
            locality = single_locality(p, partition, node_set)
            locality_for_partition.append(locality)
        localities.append(locality_for_partition)
    return percentage_list, localities


def exp1_impl(name, graph_info, p, partitions, step):
    percentage_list, localities = get_locality_partition_list(graph_info, p, partitions, step)
    plot1(name, percentage_list, localities)
    plot1_bar(name, percentage_list, localities)


def exp1(name, step):
    gzip_fname = utils.get_gzip_fname(name)
    s = network.Network.from_combined(name, gzip_fname)
    graph = s.graph
    p = Partitioner(s.graph)
    cd_partition = p.community_detection()
    parts = len(cd_partition)
    print('community parts: {}'.format(parts))
    metis_partition = p.metis_partition(parts)
    rnd_partition = p.random_partition(parts)
    graph_info = GraphInfo(graph)
    partitions = [cd_partition, metis_partition, rnd_partition]
    exp1_impl(name, graph_info, p, partitions, step)


# step fixed
def exp2_impl(name, graph_info, p, max_partition, step):
    parts_num = range(2, max_partition + 1)
    locality_parts_list = []
    for part in parts_num:
        partitions = [p.metis_partition(part), p.random_partition(part)]
        localities = get_locality_partition_list(graph_info, p, partitions, step)[1]  # length = len(partitions)
        locality_average = []  # lengh = len(partitions)
        for locality in localities:
            locality_average.append(sum(locality) / len(locality))
        locality_parts_list.append(locality_average)
    ylist = zip(*locality_parts_list)
    labels = ['Metis', 'Random']
    # plot2(name, labels, parts_num, ylist)
    plot2_random_partition(name, parts_num, ylist[1])


def exp2(name, step, max_partition):
    gzip_fname = utils.get_gzip_fname(name)
    s = network.Network.from_combined(name, gzip_fname)
    graph = s.graph
    graph_info = GraphInfo(graph)
    p = Partitioner(graph)
    exp2_impl(name, graph_info, p, max_partition, step)


if __name__ == '__main__':
    # exp1('facebook', 10)
    exp2('facebook', 5, 16)
