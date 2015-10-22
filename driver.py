#!/usr/bin/env python

from __future__ import print_function
import time
import json

from graph_info import GraphInfo
from partitioner import Partitioner
import network
import utils

import matplotlib.pyplot as plt
import numpy as np
import pylab

import matplotlib as mpl

from log_helper import init_logger, get_logger

mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.unicode'] = True

markers = '+*.o'
colors = 'rgb'
label = ['Community Detection', 'Metis', 'Random']


def single_locality(p, partition, node_set):
    assert (node_set is not None and len(node_set) != 0)
    return p.locality_percentage(partition, node_set)


@utils.timeit
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

@utils.timeit
def plot1(name, xlist, ylist):
    pylab.grid(True)
    for i in xrange(len(ylist)):
        plt.plot(xlist, ylist[i], colors[i % len(colors)], marker=markers[i % len(markers)])
    plt.legend(label, loc='center right')
    plt.xlim(xlist[0] / 2, xlist[-1] + xlist[0] / 2)
    plt.xlabel('Node Set Percentage')
    plt.ylabel('Locality Percentage')
    plt.title('{}: step={}'.format(name, len(xlist)))
    fname = name + '_exp1.png'
    plt.savefig(utils.get_result_fname(fname))
    plt.clf()

@utils.timeit
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
    plt.savefig(utils.get_result_fname(fname))
    plt.clf()


@utils.timeit
def plot2(name, labels, xlist, ylist):
    pylab.grid(True)
    for i in xrange(len(ylist)):
        plt.plot(xlist, ylist[i], colors[i % len(colors)], marker=markers[i % len(markers)])

    plt.legend(labels, loc='center right')
    plt.xlim(xlist[0] / 2, xlist[-1] + xlist[0] / 2)
    plt.xlabel('Number of Parts')
    plt.ylabel('Locality Percentage')
    plt.title('{}: Average Localities for different Parts'.format(name))
    fname = name + '_exp2.png'
    plt.savefig(utils.get_result_fname(fname))
    plt.clf()


@utils.timeit
def plot2_random_partition(name, xlist, ylist):
    yy = []
    for x, y in zip(xlist, ylist):
        yy.append(x * y)
    plt.plot(xlist, yy)
    plt.xlabel(r'$\textsf{num}$')
    plt.ylabel(r'$\textsf{l}*\textsf{num}$')
    plt.title('{}: Random Partition Locality'.format(name))
    plt.legend(['Parts*Locality'], loc='best')
    plt.ylim([0.5, 1.5])
    pylab.grid(True)
    fname = name + '_exp2_rnd.png'
    plt.savefig(utils.get_result_fname(fname))
    plt.clf()


@utils.timeit
def exp1_impl(name, graph_info, p, partitions, step):
    percentage_list, localities = get_locality_partition_list(graph_info, p, partitions, step)
    plot1(name, percentage_list, localities)
    plot1_bar(name, percentage_list, localities)


def duration(then):
    t = time.time() - then
    get_logger().info('takes {}'.format(t))
    return t


@utils.timeit
def exp1(name, step):
    exp1_info = {}
    gzip_fname = utils.get_gzip_fname(name)
    s = network.Network.from_combined(name, gzip_fname)
    graph = s.graph
    p = Partitioner(s.graph)
    cd_s = time.time()
    cd_partition = p.community_detection()
    exp1_info['community_detection'] = duration(cd_s)
    parts = len(cd_partition)
    exp1_info['parts'] = parts
    metis_s = time.time()
    metis_partition = p.metis_partition(parts)
    exp1_info['metis'] = duration(metis_s)
    random_s = time.time()
    rnd_partition = p.random_partition(parts)
    exp1_info['rnd'] = duration(random_s)
    graph_info = GraphInfo(graph)
    partitions = [cd_partition, metis_partition, rnd_partition]
    exp1_impl(name, graph_info, p, partitions, step)
    return exp1_info


@utils.timeit
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
    plot2(name, labels, parts_num, ylist)
    plot2_random_partition(name, parts_num, ylist[1])


@utils.timeit
def exp2(name, step, max_partition):
    gzip_fname = utils.get_gzip_fname(name)
    s = network.Network.from_combined(name, gzip_fname)
    graph = s.graph
    graph_info = GraphInfo(graph)
    p = Partitioner(graph)
    exp2_impl(name, graph_info, p, max_partition, step)

if __name__ == '__main__':
    init_logger()
    info_dict = {}
    data_list = ['facebook', 'dblp']
    for name in data_list:
        info = exp1(name, 10)
        info_dict[name] = info
    with open('exp1_info.json', 'w') as jsdata:
        json.dump(info_dict, jsdata, indent=2)
    for name in data_list:
        exp2(name, 5, 16)
