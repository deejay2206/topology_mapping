# Some tests of the Matrix class

from matrix import Matrix
from operator import mul, add
from mergers import *

print 'Filling ----------------------------------------------------------------'

fred = Matrix(['Alpha', 'Beta', 'Gamma'], 'Omega')
print
print fred

fred.set_cell('Beta', 'Alpha', 'Zeta')
print
print fred

fred.fill([1, 2, 3, 4, 5, 6, 7, 8, 9])
print
print fred
print

print 'Extracting -------------------------------------------------------------'

print
print fred.get_headings()
print
print fred.get_contents()
print

print 'Assigning versus copying -----------------------------------------------'

original_matrix = Matrix(['a', 'b', 'c'], 'O')
an_alias = original_matrix
a_copy = original_matrix.copy()

original_matrix.set_cell('b', 'b', 'X') # change the original

print
print an_alias # the alias should also be changed
print
print a_copy # but the copy is unaffected
print

print 'Addition of numerical matrices -----------------------------------------'

numbers_a = Matrix(['a', 'b', 'c', 'd'], 2)
numbers_b = Matrix(['A', 'B', 'C', 'D'])
numbers_a.set_cell('b', 'c', 200)
numbers_b.fill(range(16))
print
print numbers_a
print
print numbers_b
numbers_a.add_matrix(numbers_b)
print
print numbers_a
print

print 'Addition of string matrices --------------------------------------------'

strings_a = Matrix(['a', 'b', 'c', 'd'])
strings_a.fill(list('Sixteen letters!'))
strings_b = Matrix(['A', 'B', 'C', 'D'], 'o')
strings_a.set_cell('b', 'd', 'AAA')
print
print strings_a
print
print strings_b
strings_a.add_matrix(strings_b, protocol_union)
print
print strings_a
print

print 'Multiplication ---------------------------------------------------------'

multiplicand = Matrix(['One', 'Two', 'Three'])
multiplicand.fill([1, -3, -1,
                   0,  3,  2,
                   4, -4,  5])
print
print multiplicand

multiplier = Matrix(['A', 'B', 'C'])
multiplier.fill([-2,  1,  6,
                 -1,  0,  3,
                  2, -3,  4])
print
print multiplier

multiplicand.multiply_matrices(multiplier)
print
print multiplicand
print

## Correct answer:
##     |  One|  Two|Three|
##  One|   -1|    4|   -7|
##  Two|    1|   -6|   17|
##Three|    6|  -11|   32|

# http://www.bluebit.gr/matrix-calculator/multiply.aspx

print 'Joining disjoint matrices ----------------------------------------------'

numbers = Matrix(['One', 'Two', 'Three'])
numbers.fill(range(9, 0, -1))
print
print numbers
print

letters = Matrix(['AAA', 'BBB', 'CCC'])
letters.fill(['a', 'b', 'c',
              'd', 'e', 'f',
              'g', 'h', 'i'])
print letters
print

numbers.join_disjoint_matrices(letters, '.')
print numbers
print

print 'Joining overlapping matrices -------------------------------------------'

matrix_one = Matrix(['AA', 'BB', 'CC', 'DD'])
matrix_one.fill(list('abcdefghijklmnop'))
print
print matrix_one
print

matrix_two = Matrix(['CC', 'DD', 'EE', 'FF'])
matrix_two.fill(list('ZYXWVUTSRQPONMLK'))
print matrix_two
print

matrix_one.join_matrices(matrix_two, default = '.')
print matrix_one
print

matrix_three = Matrix(['FF', 'GG', 'HH'])
matrix_three.fill(list('123456789'))
print matrix_three
print

matrix_one.join_matrices(matrix_three, default = '.')
print matrix_one
print

print 'Closure with numbers ---------------------------------------------------'

a_graph = Matrix(['Node A', 'Node B', 'Node C', 'Node D'])
a_graph.fill([0, 1, 0, 0,
              0, 0, 0, 1,
              0, 0, 0, 0,
              1, 0, 1, 0])

print
print a_graph

a_graph.closure()

print
print a_graph
print

# Correct answer:
#     1, 1, 1, 1,
#     1, 1, 1, 1,
#     0, 0, 0, 0,
#     1, 1, 1, 1

print 'Closure with strings ---------------------------------------------------'

#   A -w-> B
#    ^     |
#     \    x
#      y   |
#       \  |
#        \ v
#   C <-z- D

a_graph = Matrix(['Node A', 'Node B', 'Node C', 'Node D'])
a_graph.fill(['',  'w',  '',  '',
              '',   '',  '', 'x',
              '',   '',  '',  '',
              'y',  '', 'z',  ''])

print
print a_graph

a_graph.closure(add_alt_path = path_union,
                join_hops = conjoin_paths,
                empty_cell = '')

print
print a_graph
print

print 'A more complex closure with strings ------------------------------------'

#   A  -w-> B
#    ^ \    |
#     \ \   x
#      y u  |
#       \ \ |
#        \ vv
#   C <-z-- D


a_graph = Matrix(['Node A', 'Node B', 'Node C', 'Node D'])
a_graph.fill(['',  'w',  '', 'u',
              '',   '',  '', 'x',
              '',   '',  '',  '',
              'y',  '', 'z',  ''])

print
print a_graph

a_graph.closure(add_alt_path = path_union,
                join_hops = conjoin_paths,
                empty_cell = '')

print
print a_graph
print


print 'A simpler closure with strings -----------------------------------------'

a_graph = Matrix(['Node A', 'Node B', 'Node C', 'Node D'])
a_graph.fill(['',  'w',  '', 'u',
              '',   '',  '', 'x',
              '',   '',  '',  '',
              'y',  '', 'z',  ''])

print
print a_graph

a_graph.closure(add_alt_path = path_union,
                join_hops = conjoin_paths,
                empty_cell = '')

print
print a_graph
print

print 'Reachability with numbers ----------------------------------------------'

# Example: A->B, B->D, D->C and C->B

a_graph = Matrix(['Node A', 'Node B', 'Node C', 'Node D'])
# It's a small matrix, so we'll fill every cell
a_graph.fill([0, 1, 0, 0,
              0, 0, 0, 1,
              0, 1, 0, 0,
              0, 0, 1, 0])

print
print 'Reachable from A:', a_graph.reachable_from('Node A')
print 'Reachable from B:', a_graph.reachable_from('Node B')
print 'Reachable from C:', a_graph.reachable_from('Node C')
print 'Reachable from D:', a_graph.reachable_from('Node D')

print
print 'Can reach A:', a_graph.can_reach('Node A')
print 'Can reach B:', a_graph.can_reach('Node B')
print 'Can reach C:', a_graph.can_reach('Node C')
print 'Can reach D:', a_graph.can_reach('Node D')
print

print 'Reachability with strings ----------------------------------------------'

# Example: K->J, K->M, L->N, M->N, M->L

a_graph = Matrix(['K', 'J', 'L', 'M', 'N'], 'O')
# It's a sparse matrix, so we'll set individual cells rather than filling
a_graph.set_cell('K', 'J', 'X')
a_graph.set_cell('K', 'M', 'X')
a_graph.set_cell('L', 'N', 'X')
a_graph.set_cell('M', 'N', 'X')
a_graph.set_cell('M', 'L', 'X')

print
print 'Reachable from K:', a_graph.reachable_from('K', 'O')
print 'Reachable from J:', a_graph.reachable_from('J', 'O')
print 'Reachable from L:', a_graph.reachable_from('L', 'O')
print 'Reachable from M:', a_graph.reachable_from('M', 'O')
print 'Reachable from N:', a_graph.reachable_from('N', 'O')

print
print 'Can reach K:', a_graph.can_reach('K', 'O')
print 'Can reach J:', a_graph.can_reach('J', 'O')
print 'Can reach L:', a_graph.can_reach('L', 'O')
print 'Can reach M:', a_graph.can_reach('M', 'O')
print 'Can reach N:', a_graph.can_reach('N', 'O')
