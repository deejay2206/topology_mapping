# Tests of the observability algorithm, "may", "must"
# and "should" see.

from matrix import Matrix

# Basic examples from Ken's notes ------------------------------------

# This is the PHYSICAL topology
flux_capacitor = Matrix(['A', 'B', 'C', 'D'])
flux_capacitor.fill([0, 0, 1, 0,
                     0, 0, 1, 0,
                     1, 1, 0, 1,
                     0, 0, 1, 0])

print 'Physical topology:'
print flux_capacitor
print

# Find LOGICAL topology visible to observer A
print 'What A may see:'
print flux_capacitor.may_see(['A'])
print

# Find LOGICAL topology visible to observer B
print 'What B may see:'
print flux_capacitor.may_see(['B'])
print

# Find LOGICAL topology visible to both observers A and B
print 'What A and B may see:'
print flux_capacitor.may_see(['A', 'B'])
print

# Find LOGICAL topology visible to observer C
print 'What C may see:'
print flux_capacitor.may_see(['C'])
print

# This is the PHYSICAL topology
box = Matrix(['W', 'X', 'Y', 'Z'])
box.fill([0, 1, 1, 0,
          1, 0, 0, 1,
          1, 0, 0, 1,
          0, 1, 1, 0])

print 'Physical topology:'
print box
print

print 'What W may see:'
print box.may_see(['W'])
print

print 'What W and Z may see:'
print box.may_see(['W', 'Z'])
print

# This is the PHYSICAL topology
cul_de_sacs = Matrix(['A', 'B', 'C', 'D', 'E'])
cul_de_sacs.fill([0, 0, 0, 0, 0,
                  1, 0, 1, 1, 0,
                  0, 1, 0, 0, 0,
                  0, 0, 0, 0, 1,
                  0, 0, 0, 1, 0])

print 'Physical topology:'
print cul_de_sacs
print

# Find LOGICAL topology visible to observer C
print 'What C may see:'
print cul_de_sacs.may_see(['C'])
print
