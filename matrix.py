

# Matrix - A class for square matrices with arbitrary types for
# indices and arbitrary types for cells.  Matrix objects are
# mutable so operations are performed in place.
class Matrix:

    # Functions corresponding to arithmetic primitives
    from operator import add, mul

    # Constructor - creates the matrix and fills all cells with a default value
    def __init__(self, headings = ['default'], default_content = 0):
        # Check uniqueness of headings
        for heading in headings:
            assert headings.count(heading) == 1, "Duplicate heading:" + str(heading)
        # Map headings to indices
        self.headings = headings
        # Initialise the matrix
        # (Note that [[default_content] * len(headings)] * len(headings) aliases the
        #  mutable list rows!)
        self.contents = [[default_content for row in headings] for column in headings]

    # Setter - populates the matrix from a single-dimension list of contents
    def fill(self, contents):
        # Confirm that sufficient contents have been provided
        assert len(contents) == len(self.headings) ** 2, "Number of cells does not match matrix size in 'fill'"
        # Copy the list of contents into the matrix
        position = 0
        for row in self.headings:
            for column in self.headings:
                self.set_cell(row, column, contents[position])
                position += 1

    # Setter - updates a particular cell
    def set_cell(self, row = 'default', column = 'default', content = 0):
        self.contents[self.headings.index(row)][self.headings.index(column)] = content        

    # Getter - returns (an alias to?) a particular cell's contents
    def get_cell(self, row = 'default', column = 'default'):
        return self.contents[self.headings.index(row)][self.headings.index(column)]

    # Getter - returns the square matrix's dimension
    def get_size(self):
        return len(self.headings)

    # Getter - returns a copy of the row/column headings
    def get_headings(self):
        return list(self.headings)

    # Getter - returns a copy of the matrix's contents as a single-dimension list
    def get_contents(self):
        return list(sum(self.contents, []))

    # Create a copy of the current matrix (because Matrix objects are
    # mutable the assignment "new_matrix = old_matrix" creates an
    # alias, not a copy, so you need "new_matrix = old_matrix.copy()" to
    # create a separate copy)
    def copy(self):
        new_copy = Matrix(self.get_headings())
        new_copy.fill(self.get_contents())
        return new_copy

    # "Add" corresponding cells from another equal-sized matrix,
    # using an arbitrary binary function to "add" the cells
    def add_matrix(self, summand, operation = add):
        # Check type correctness of parameter
        assert isinstance(summand, Matrix), "Summand is not a matrix in 'add_matrix'"
        assert summand.get_size() == self.get_size(), "Different size matrices in 'add_matrix'"
        # Create a mapping between this matrix's headings and those of the summand
        summand_headings = summand.get_headings()
        mapping = dict([(self.get_headings()[index], summand_headings[index]) for index in range(self.get_size())])
        # "Add" corresponding cells using the given operator
        for row in self.get_headings():
            for column in self.get_headings():
                self.set_cell(row, column,
                              operation(self.get_cell(row, column),
                                        summand.get_cell(mapping[row], mapping[column])))        

    # Multiply this matrix (the multiplicand) by another equal-sized
    # matrix, using arbitrary "addition" and "multiplication" operators.
    # Recall that a cell's value in the result, given a row "a, b, c" from
    # the multiplicand and column "x, y, z" from the multiplier equals
    # "a*x + b*y + c*z".
    def multiply_matrices(self, multiplier, addition = add, multiplication = mul, zero_value = 0):
        # Check type correctness of parameter
        assert isinstance(multiplier, Matrix), "Multiplier is not a matrix in 'multiply_matrices'"
        assert multiplier.get_size() == self.get_size(), "Different size matrices in 'multiply_matrices'"
        # Create a mapping between this matrix's headings and those of the summand
        multiplier_headings = multiplier.get_headings()
        mapping = dict([(self.get_headings()[index], multiplier_headings[index]) for index in range(self.get_size())])
        # Create a new matrix to hold the result
        result = Matrix(self.get_headings(), zero_value)
        # "Multiply" the matrices using the given operators
        for rowA in self.get_headings():
            for columnB in self.get_headings():
                for rowB in self.get_headings():
                    result.set_cell(rowA, columnB,
                                    addition(result.get_cell(rowA, columnB),
                                             multiplication(self.get_cell(rowA, rowB),
                                                            multiplier.get_cell(mapping[rowB], mapping[columnB]))))
        # Replace this matrix's contents with the result
        self.fill(result.get_contents())

    # "Join" this matrix to another to create a larger matrix, assuming the
    # headings of the two matrices are disjoint.
    # For instance, if this matrix is of size M and the other matrix
    # is of size N, the result will be a matrix of size M + N.  Cells from
    # the original matrices are copied into the new one, and newly-created
    # cells are filled with a default value.
    def join_disjoint_matrices(self, other_matrix, default = 0):
        # Check type correctness of parameter
        assert isinstance(other_matrix, Matrix), "Parameter is not a matrix in 'join_disjoint_matrices'"
        for heading in self.get_headings():
            assert not (heading in other_matrix.get_headings()), "Headings must be disjoint in 'join_disjoint_matrices'"
        # Create a new matrix full of default values
        result = Matrix(self.get_headings() + other_matrix.headings, default)
        # Insert the original cells from this matrix
        for row in self.get_headings():
            for column in self.get_headings():
                result.set_cell(row, column, self.get_cell(row, column))
        # Insert the original cells from the other matrix
        for row in other_matrix.get_headings():
            for column in other_matrix.get_headings():
                result.set_cell(row, column, other_matrix.get_cell(row, column))                              
        # Replace this matrix's guts with the result
        self.headings = result.get_headings()
        self.contents = [['dummy' for row in self.get_headings()] for column in self.get_headings()]
        self.fill(result.get_contents())

    # "Join" this matrix to another to create a larger matrix; headings do
    # not need to be disjoint, but a function needs to be provided for
    # merging cells that appear in both matrices.
    def join_matrices(self, other_matrix, merger = add, default = 0):
        # Check type correctness of parameter
        assert isinstance(other_matrix, Matrix), "Parameter is not a matrix in 'join_matrices'"
        # Create the new heading list, preserving the original order of
        # the headings
        new_headings = self.get_headings()
        for heading in other_matrix.get_headings():
            if not heading in new_headings:
                new_headings += [heading]
        # Create a new matrix full of default values
        result = Matrix(new_headings, default)
        # Insert the original cells that only appear in this matrix
        for row in self.get_headings():
            for column in self.get_headings():
                if not (row in other_matrix.get_headings() and column in other_matrix.get_headings()):
                    result.set_cell(row, column, self.get_cell(row, column))
        # Insert the original cells that only appear in the other matrix
        for row in other_matrix.get_headings():
            for column in other_matrix.get_headings():
                if not (row in self.get_headings() and column in self.get_headings()):
                    result.set_cell(row, column, other_matrix.get_cell(row, column))                              
        # Merge the cells that appear in both matrices
        for row in self.get_headings():
            for column in self.get_headings():
                if row in other_matrix.get_headings() and column in other_matrix.get_headings():
                    result.set_cell(row, column, merger(self.get_cell(row, column), other_matrix.get_cell(row, column)))                              
        # Replace this matrix's guts with the result
        self.headings = result.get_headings()
        self.contents = [['dummy' for row in new_headings] for column in new_headings]
        self.fill(result.get_contents())

    # Calculate the transitive closure of this matrix, assuming that there
    # are distinguished empty cells and that populated cells can be "added".
    # Warshall's algorithm is adapted without any attempt to improve
    # its dreadful time efficiency of O(N^3).  Whereas a standard transitive
    # closure calculation doesn't distinguish a direct link between nodes i
    # j and an indirect one via node k, here we provide two distinct node
    # "addition" operators so that we can see the difference.
    def closure(self, add_alt_path = max, join_hops = max, empty_cell = 0):
        # Create a new matrix to hold the previous result
        previous = self.copy()
        # Create a new matrix to hold the next result
        next_matrix = self.copy()       
        # Create k successive hops in the closure (extend k if you want longer cycles
        # to appear in the cells, although this won't populate more cells)
        for k in self.get_headings():
            previous_matrix = next_matrix.copy()
            for i in self.get_headings():
                for j in self.get_headings():
                    # Insert existing direct paths from i to j
                    if previous_matrix.get_cell(i, j) != empty_cell:
                        next_matrix.set_cell(i, j, previous_matrix.get_cell(i, j))
                    # Add indirect paths from i to j via k
                    if previous_matrix.get_cell(i, k) != empty_cell and previous_matrix.get_cell(k, j) != empty_cell:
                        if next_matrix.get_cell(i, j) != empty_cell:
                            # There is more than one path between i and j
                            next_matrix.set_cell(i, j, add_alt_path(next_matrix.get_cell(i, j),
                                                                    join_hops(previous_matrix.get_cell(i, k), previous_matrix.get_cell(k, j))))
                        else:
                            # This is the first path found between i and j
                            next_matrix.set_cell(i, j, join_hops(previous_matrix.get_cell(i, k), previous_matrix.get_cell(k, j)))
        # Replace this matrix's contents with the result
        self.fill(next_matrix.get_contents())


    # Assuming this matrix M represents a digraph, and given the name
    # of a particular node N, return a list of all other nodes
    # reachable in M from N, either directly or indirectly.  It is
    # assumed that any cell (X, Y) with contents not equal to the
    # "empty" value means there is a link from node X to Y.
    def reachable_from(self, source, empty_cell = 0):
        # Confirm that the source node exists
        assert source in self.get_headings(), 'Node ' + str(source) + 'does not exist in method "reachable_from"' 
        # Create a copy of this matrix, so that we can mess about with
        # the graph without corrupting this one
        new_graph = self.copy()
        # Calculate the transitive closure
        new_graph.closure(empty_cell = empty_cell)
        # Accumulate the list of reachable nodes
        reachable = []
        for destination in self.get_headings():
            if destination != source:
                if new_graph.get_cell(source, destination) != empty_cell:
                    reachable += [destination]
        # Return the result      
        return reachable


    # Assuming this matrix M represents a digraph, and given the name
    # of a particular node N, return a list of all other nodes
    # in M that can reach N, either directly or indirectly.  It is
    # assumed that any cell (X, Y) with contents not equal to the
    # "empty" value means there is a link from node X to Y.
    def can_reach(self, destination, empty_cell = 0):
        # Confirm that the destination node exists
        assert destination in self.get_headings(), 'Node ' + str(destination) + 'does not exist in method "reachable_from"' 
        # Create a copy of this matrix, so that we can mess about with
        # the graph without corrupting this one
        new_graph = self.copy()
        # Calculate the transitive closure
        new_graph.closure(empty_cell = empty_cell)
        # Accumulate the list of nodes that can reach the destination
        reaches = []
        for source in self.get_headings():
            if source != destination:
                if new_graph.get_cell(source, destination) != empty_cell:
                    reaches += [source]
        # Return the result      
        return reaches   


    # Assuming this matrix is a digraph representing the physical topology of
    # a network, and given a list of "observer" nodes, return a matrix
    # representing the logical topology potentially visible by these
    # observers (assuming all nodes send messsages to all other nodes while
    # the observers are watching).
    #
    # THIS DRAFT VERSION IS LIMITED TO NUMERICAL INPUT MATRICES ONLY!
    #
    def should_see(self, observers, empty_cell = 0):
        # Confirm that all the observers actually exist
        for observer in observers:
            assert observer in self.get_headings(), 'Observer ' + str(observer) + ' nonexistent in "can_see"'
        # Create a new matrix to hold the result
        visible = Matrix(self.get_headings())
        # Calculate who can send to each observer and add it to the result
        for observer in observers:
            sources = self.can_reach(observer)
            # Create a matrix in which each source leads to the observer
            sends_to_observer = Matrix(self.get_headings())
            for source in sources:
                sends_to_observer.set_cell(source, observer, 1)
            # Add this matrix to the result
            visible.add_matrix(sends_to_observer, max)
        # Calculate who each observer can send to and add it to the result
        for observer in observers:
            destinations = self.reachable_from(observer)
            # Create a matrix in which the observer sends to each source
            observer_sends_to = Matrix(self.get_headings())
            for destination in destinations:
                observer_sends_to.set_cell(observer, destination, 1)
            # Add this matrix to the result
            visible.add_matrix(observer_sends_to, max)
        # Calculate who can send to someone else via each observer and add it to the result
        for observer in observers:
            # Create the closure of the current physical topology
            # excluding the observer
            no_observer = self.copy()
            for row in no_observer.get_headings():
                for column in no_observer.get_headings():
                    no_observer.set_cell(row, observer, empty_cell)
                    no_observer.set_cell(observer, column, empty_cell)
            no_observer.closure()
            # Create a matrix to hold links that go via the observer
            goes_via_observer = Matrix(self.get_headings())
            # Add direct links between sources and destinations that
            # could be routed via the observer
            for source in self.can_reach(observer):
                for destination in self.reachable_from(observer):
                    # Exclude the observer itself as an endpoint
                    if (source != observer) and (destination != observer):
                        # Exclude nodes indirectly sending to themselves
                        if source != destination:
                            # Only add a link via the observer if there is
                            # no other way to get from the source to the
                            # destination in the original graph [and there
                            # is no link between the source and destination in
                            # the graph under construction?]  <---- INCOMPLETE!!!!
                            if not (destination in no_observer.reachable_from(source)):
##                                and \
##                               (visible.get_cell(source, destination) == empty_cell and \
##                                goes_via_observer.get_cell(source, destination) == empty_cell):
                                goes_via_observer.set_cell(source, destination, 1)
            # Add this matrix to the result
            visible.add_matrix(goes_via_observer, max)
        # Return the result
        return visible


    # Assuming this matrix is a digraph representing the physical topology of
    # a network, and given a list of "observer" nodes, return a matrix
    # representing the logical topology that inevitably must be visible
    # to these observers.  This consists of all paths between sources and
    # destinations that must go via an observer.  This produces the
    # smallest possible logical topology.
    #
    # THIS FUNCTION IS LIMITED TO NUMERICAL INPUT MATRICES ONLY!
    #
    def must_see(self, observers, empty_cell = 0):
        # Confirm that all the observers actually exist
        for observer in observers:
            assert observer in self.get_headings(), 'Observer ' + str(observer) + ' nonexistent in "can_see"'
        # Create a new matrix to hold the result
        visible = Matrix(self.get_headings())
        # Do the calculation
        pass
        # Return the result
        return visible    


    # Assuming this matrix is a digraph representing the physical topology of
    # a network, and given a list of "observer" nodes, return a matrix
    # representing the entire logical topology potentially visible by these
    # observers.  It assumed that if a message COULD be sent via an
    # observer then it will be, no matter how convoluted the path.  This
    # will produce the largest possible logical topology.
    #
    # THIS FUNCTION IS LIMITED TO NUMERICAL INPUT MATRICES ONLY!
    #
    def may_see(self, observers, empty_cell = 0):
        # Confirm that all the observers actually exist
        for observer in observers:
            assert observer in self.get_headings(), 'Observer ' + str(observer) + ' nonexistent in "can_see"'
        # Create a new matrix to hold the result
        visible = Matrix(self.get_headings())
        # Calculate who can send to each observer and add it to the result
        for observer in observers:
            sources = self.can_reach(observer)
            # Create a matrix in which each source leads to the observer
            sends_to_observer = Matrix(self.get_headings())
            for source in sources:
                sends_to_observer.set_cell(source, observer, 1)
            # Add this matrix to the result
            visible.add_matrix(sends_to_observer, max)
        # Calculate who each observer can send to and add it to the result
        for observer in observers:
            destinations = self.reachable_from(observer)
            # Create a matrix in which the observer sends to each source
            observer_sends_to = Matrix(self.get_headings())
            for destination in destinations:
                observer_sends_to.set_cell(observer, destination, 1)
            # Add this matrix to the result
            visible.add_matrix(observer_sends_to, max)
        # Calculate who can send to someone else via each observer and add it to the result
        for observer in observers:
            # Create a matrix to hold links that go via the observer
            goes_via_observer = Matrix(self.get_headings())
            # Add direct links between sources and destinations that
            # could be routed via the observer
            for source in self.can_reach(observer):
                for destination in self.reachable_from(observer):
                    # Exclude the observer itself as an endpoint 
                    if (source != observer) and (destination != observer):
                        # Exclude nodes indirectly sending to themselves <- ASSUMPTION!
                        if source != destination:
                            goes_via_observer.set_cell(source, destination, 1)
            # Add this matrix to the result
            visible.add_matrix(goes_via_observer, max)
        # Return the result
        return visible
        
    
    # Return a printable representation of the matrix, with fixed-width
    # columns
    def __str__(self):
        # Width of columns when matrix is printed (change for wider/narrower columns)
        COLUMN_WIDTH = 12 
        # Create the string representation of this matrix
        to_print = '' 
        # Create column heading
        to_print += ' ' * COLUMN_WIDTH + '|'
        for heading in self.headings:
            # Format the column label to fit the column width
            column_label = str(heading)
            formatted_label = column_label[max(len(column_label) - COLUMN_WIDTH, 0):] 
            to_print += formatted_label.rjust(COLUMN_WIDTH) + '|'
        to_print += '\n'
        # Create each row
        for row in self.headings:
            # Format the row label to fit the column width
            row_label = str(row)
            formatted_label = row_label[max(len(row_label) - COLUMN_WIDTH, 0):] 
            to_print += formatted_label.rjust(COLUMN_WIDTH) + '|'
            # Format each cell in the row to fit the column width
            for column in self.headings:
                cell_contents = str(self.get_cell(row, column))
                formatted_cell = cell_contents[max(len(cell_contents) - COLUMN_WIDTH, 0):] 
                to_print += formatted_cell.rjust(COLUMN_WIDTH) + '|'
            to_print += '\n'            
        # Return the string to display (dropping the last newline char)
        return to_print[:-1]

