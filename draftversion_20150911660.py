t__author__ = 'n7404808'

from matrix import Matrix
from networkx import nx
import sys
import csv

# orig_stdout = sys.stdout
# f = file('flux_capacitor.csv', 'w')
# sys.stdout = f



print 'two nodes --------------------------------------------------------'
# output everything to file
# e = open('flux_capacitor20150827200.csv','w')
f = open('this_graph_20150910226.csv','w')
g = open('flux_capacitor20150910226.csv','w')
# h = open('flux_capacitor201508271040.csv','w')
# i = open('flux_capacitor20150827127.csv','w')

headers = ['A', 'B', 'C', 'D']
flux_capacitor = Matrix(headers)

# f.write(str(headers))
# f.write('\n')

# now do all combinations of graphs
# start with four nodes
for node_1 in xrange(len(headers)*len(headers)):
    for node_2 in xrange(len(headers)*len(headers)):
        for node_3 in xrange(len(headers)*len(headers)):
            for node_4 in xrange(len(headers)*len(headers)):
                this_graph = []
                for x_index in xrange(len(headers)*len(headers)):
                    if x_index == node_1 or x_index == node_2 or x_index == node_3 or x_index == node_4:
                        this_graph.append(1)
                    else:
                        this_graph.append(0)
                        # print this_graph

                        f.write(str(this_graph))
                        f.write('\n\n')

                flux_capacitor.fill(this_graph)
                g.write(str(flux_capacitor))
                g.write('\n\n')
                # print
                # print flux_capacitor
                # print
G = nx.Graph()
G.add_nodes_from (self.get_headings())
for row in self.get_headings():
    for col in self.get_headings():
        if self.get_cell(row, col) == 1:
            G.add_edge(row, col)
                # print 'What A may see:'
                # print flux_capacitor.may_see(['A'])
                # print
                #
                # h.write(str(flux_capacitor.may_see))
                # h.write('\n')
                #
#
# f.close()



# Find LOGICAL topology visible to observer A
# print 'What A can see:'
# print flux_capacitor.can_see(['A'])
# print

# # Find LOGICAL topology visible to observer B
# print 'What B can see:'
# print flux_capacitor.can_see(['B'])
# print
