#
# Merge cell functions for use with the Matrix class
#
# These functions are for use with Matrix functions such as
# "closure" which need to know how to merge the contents of
# matrix cells.  For numerical matrices the "mul" and "add"
# functions from Python's operator module can be used for this
# purpose.  The functions below allow for non-numerical matrices.
#
# It is assumed "paths" consist of the sets of "protocols" appearing
# on that path.  In this version the order in which the protocols
# appear in the path is not preserved, and any duplicate protocols
# and paths in a set are omitted.
#

# Constants
EMPTY_PATHS = ''

# Merge two sets of protocols.  Duplicate protocols are omitted.
# The order of protocols is not preserved.
def protocol_union(protocols1, protocols2, protocol_separator = ','):
    # Split the protocols on the separator
    set1 = protocols1.split(protocol_separator)
    set2 = protocols2.split(protocol_separator)
    # Merge the two sets, discarding duplicates
    result = list(set(set1 + set2))
    # Sort the result for neatness
    result.sort()
    # Rejoin to form the new path
    return protocol_separator.join(result)

# Merge two sets of paths (i.e., sets of protocols).  Duplicate paths are omitted.
# The order of paths is not preserved.
def path_union(paths1, paths2, path_separator = '&'):
    # Split the path sets on the separator
    set1 = paths1.split(path_separator)
    set2 = paths2.split(path_separator)
    # Merge the two sets, discarding duplicates
    result = list(set(set1 + set2))
    # Sort the result for neatness
    result.sort()
    # Rejoin to form the new path
    return path_separator.join(result)

# Give two sets of paths, join them end-to-end in all combinations.
# Duplicate resulting paths are omitted.
def conjoin_paths(paths1, paths2, protocol_separator = ',', path_separator = '&'):
    # Separate the first set of paths
    old_paths1 = paths1.split(path_separator)
    # Separate the second set of paths
    old_paths2 = paths2.split(path_separator)
    # Create all combinations of paths from the first set being
    # joined to paths from the second
    joined_paths = []
    for path1 in old_paths1:
        for path2 in old_paths2:
            joined_paths.append(protocol_union(path1, path2, protocol_separator))
    # Remove any duplicate paths created
    joined_paths = list(set(joined_paths))
    # Rejoin to form the new set of paths
    return path_separator.join(joined_paths)   
