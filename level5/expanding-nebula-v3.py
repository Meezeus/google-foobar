from __future__ import print_function
import cProfile

# You've escaped Commander Lambda's exploding space station along with numerous
# escape pods full of bunnies. But - oh no! - one of the escape pods has flown
# into a nearby nebula, causing you to lose track of it. You start monitoring
# the nebula, but unfortunately, just a moment too late to find where the pod
# went. However, you do find that the gas of the steadily expanding nebula
# follows a simple pattern, meaning that you should be able to determine the
# previous state of the gas and narrow down where you might find the pod.
#
# From the scans of the nebula, you have found that it is very flat and
# distributed in distinct patches, so you can model it as a 2D grid. You find
# that the current existence of gas in a cell of the grid is determined exactly
# by its 4 nearby cells, specifically, (1) that cell, (2) the cell below it, (3)
# the cell to the right of it, and (4) the cell below and to the right of it.
# If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas,
# then it will also have gas in the next state. Otherwise, the cell will be
# empty in the next state.
#
# For example, let's say the previous state of the grid (p) was:

# .O..
# ..O.
# ...O
# O...

# To see how this grid will change to become the current grid (c) over the next
# time step, consider the 2x2 blocks of cells around each cell. Of the 2x2 block
# of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which
# means this 2x2 block would become cell c[0][0] with gas in the next time step:

# .O -> O
# ..

# Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2],
# p[1][1], p[1][2]], two of the containing cells have gas, so in the next state
# of the grid, c[0][1] will NOT have gas:

# O. -> .
# .O

# Following this pattern to its conclusion, from the previous state p, the
# current state of the grid c will be:

# O.O
# .O.
# O.O

# Note that the resulting output will have 1 fewer row and column, since the
# bottom and rightmost cells do not have a cell below and to the right of them,
# respectively.
#
# Write a function solution(g) where g is an array of array of bools saying
# whether there is gas in each cell (the current scan of the nebula), and return
# an int with the number of possible previous states that could have resulted in
# that grid after 1 time step. For instance, if the function were given the
# current state c above, it would deduce that the possible previous states were
# p (given above) as well as its horizontal and vertical reflections, and would
# return 4. The width of the grid will be between 3 and 50 inclusive, and the
# height of the grid will be between 3 and 9 inclusive. The answer will always
# be less than one billion (10^9).

class Pattern:

    value_to_string = {True: "O", False: "."}

    def __init__(self, values):
        self.TL = values[0]
        self.TR = values[1]
        self.BL = values[2]
        self.BR = values[3]

    def __repr__(self):
        return "\n{}{}\n{}{}\n".format(Pattern.value_to_string[self.TL], Pattern.value_to_string[self.TR], Pattern.value_to_string[self.BL], Pattern.value_to_string[self.BR])

GAS_PATTERNS = [Pattern([True, False, False, False]), Pattern([False, True, False, False]), Pattern([False, False, True, False]), Pattern([False, False, False, True])]

SPACE_PATTERNS = [Pattern([False, False, False, False]), Pattern([True, True, True, True]),
                  Pattern([True, True, False, False]), Pattern([False, False, True, True]), Pattern([True, False, True, False]), Pattern([False, True, False, True]), Pattern([True, False, False, True]), Pattern([False, True, True, False]),
                  Pattern([False, True, True, True]), Pattern([True, False, True, True]), Pattern([True, True, False, True]), Pattern([True, True, True, False])]

def compute_compatible_patterns():
    compatible_patterns_gas = {}
    compatible_patterns_space = {}
    for gas in [True, False]:
        compatible_patterns = compatible_patterns_gas if gas else compatible_patterns_space
        patterns = GAS_PATTERNS if gas else SPACE_PATTERNS
        for top_pattern in GAS_PATTERNS + SPACE_PATTERNS + [None]:
            for left_pattern in GAS_PATTERNS + SPACE_PATTERNS + [None]:
                compatible_patterns[top_pattern, left_pattern] = []
                for pattern in patterns:
                    if left_pattern == None:
                        if top_pattern == None:
                            # First column and first row, no need to check left or up.
                            compatible_patterns[top_pattern, left_pattern] = compatible_patterns[top_pattern, left_pattern] + [pattern]
                        else:
                            # First column, need to check up but not left.
                            if top_pattern.BL == pattern.TL and top_pattern.BR == pattern.TR:
                                compatible_patterns[top_pattern, left_pattern] = compatible_patterns[top_pattern, left_pattern] + [pattern]
                    else:
                        if top_pattern == None:
                            # First row, need to check left but not up.
                            if left_pattern.TR == pattern.TL and left_pattern.BR == pattern.BL:
                                compatible_patterns[top_pattern, left_pattern] = compatible_patterns[top_pattern, left_pattern] + [pattern]
                        else:
                            # Inner cell, need to check left and up.
                            if left_pattern.TR == pattern.TL and left_pattern.BR == pattern.BL and top_pattern.BL == pattern.TL and top_pattern.BR == pattern.TR:
                                compatible_patterns[top_pattern, left_pattern] = compatible_patterns[top_pattern, left_pattern] + [pattern]
    return compatible_patterns_gas, compatible_patterns_space

class Solution:

    def __init__(self, height):
        self.height = height
        self.previous_col = []
        self.active_col = []

    def __repr__(self):
        str = ""
        for height_index in range(self.height):
            str += "?? "
            if height_index < len(self.previous_col):
                previous_pattern = self.previous_col[height_index]
                str += Pattern.value_to_string[previous_pattern.TL] + Pattern.value_to_string[previous_pattern.TR] + " "
            else:
                str += "-- "
            if height_index < len(self.active_col):
                active_pattern = self.active_col[height_index]
                str += Pattern.value_to_string[active_pattern.TL] + Pattern.value_to_string[active_pattern.TR] + " "
            else:
                str += "-- "
            str += "\n"
            
            str += "?? "
            if height_index < len(self.previous_col):
                previous_pattern = self.previous_col[height_index]
                str += Pattern.value_to_string[previous_pattern.BL] + Pattern.value_to_string[previous_pattern.BR] + " "
            else:
                str += "-- "            
            if height_index < len(self.active_col):
                active_pattern = self.active_col[height_index]
                str += Pattern.value_to_string[active_pattern.BL] + Pattern.value_to_string[active_pattern.BR] + " "
            else:
                str += "-- "
            str += "\n\n"
        return str
    
    def extend(self, pattern):
        new_solution = Solution(self.height)
        if len(self.active_col) + 1 == self.height:
            new_solution.previous_col = self.active_col + [pattern]
        elif len(self.active_col) + 1 < self.height:
            new_solution.previous_col = self.previous_col
            new_solution.active_col = self.active_col + [pattern]
        return new_solution

def solution(g, debug=False):
    compatible_patterns_gas, compatible_patterns_space = compute_compatible_patterns()
    compatible_patterns = None
    height = len(g)
    width = len(g[0])
    solutions = [Solution(height)]
    new_solutions = []
    top_pattern = None
    left_pattern = None
    patterns = []

    for width_index in range(width):
        for height_index in range(height):
            compatible_patterns = compatible_patterns_gas if g[height_index][width_index] else compatible_patterns_space
            new_solutions = []

            # Extend the existing solution(s).
            for solution in solutions:
                if height_index < len(solution.previous_col):
                    left_pattern = solution.previous_col[height_index]
                else:
                    left_pattern = None
                if len(solution.active_col) > 0:
                    top_pattern = solution.active_col[-1]
                else:
                    top_pattern = None
                    
                patterns = compatible_patterns[top_pattern, left_pattern]
                for pattern in patterns:
                    new_solutions.append(solution.extend(pattern))
        
            solutions = new_solutions
            # for solution in solutions:
            #     print(solution)
            if debug:
                print("Number of solutions = {}".format(len(solutions)))

    return len(solutions)

# Test Cases
failed = False

expected = 11567
actual = solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
cProfile.run("solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])")
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 4
actual = solution([[True, False, True], [False, True, False], [True, False, True]])
cProfile.run("assert solution([[True, False, True], [False, True, False], [True, False, True]]) == 4")
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 254
actual = solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
cProfile.run("assert solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]) == 254")
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more test cases failed!")
