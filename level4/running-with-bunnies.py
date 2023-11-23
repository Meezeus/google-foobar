from __future__ import print_function
import copy

# You and your rescued bunny prisoners need to get out of this collapsing death
# trap of a space station - and fast! Unfortunately, some of the bunnies have
# been weakened by their long imprisonment and can't run very fast. Their
# friends are trying to help them, but this escape would go a lot faster if you
# also pitched in. The defensive bulkhead doors have begun to close, and if you
# don't make it through in time, you'll be trapped! You need to grab as many
# bunnies as you can and get through the bulkheads before they close.
#
# The time it takes to move from your starting point to all of the bunnies and
# to the bulkhead will be given to you in a square matrix of integers. Each row
# will tell you the time it takes to get to the start, first bunny, second
# bunny, ..., last bunny, and the bulkhead in that order. The order of the rows
# follows the same pattern (start, each bunny, bulkhead). The bunnies can jump
# into your arms, so picking them up is instantaneous, and arriving at the
# bulkhead at the same time as it seals still allows for a successful, if
# dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to
# escape with you since they no longer have to carry the ones you did pick up.)
# You can revisit different spots if you wish, and moving to the bulkhead
# doesn't mean you have to immediately leave - you can move to and from the
# bulkhead to pick up additional bunnies if time permits.
#
# In addition to spending time traveling between bunnies, some paths interact
# with the space station's security checkpoints and add time back to the clock.
# Adding time to the clock will delay the closing of the bulkhead doors, and if
# the time goes back up to 0 or a positive number after the doors have already
# closed, it triggers the bulkhead to reopen. Therefore, it might be possible to
# walk in a circle and keep gaining time: that is, each time a path is
# traversed, the same amount of time is used or added.
#
# Write a function of the form solution(times, time_limit) to calculate the most
# bunnies you can pick up and which bunnies they are, while still escaping
# through the bulkhead before the doors close for good. If there are multiple
# sets of bunnies of the same size, return the set of bunnies with the lowest
# prisoner IDs (as indexes) in sorted order. The bunnies are represented as a
# sorted list by prisoner ID, with the first bunny being 0. There are at most 5
# bunnies, and time_limit is a non-negative integer that is at most 999.
#
# For instance, in the case of

# [
#     [0, 2, 2, 2, -1],  # 0 = Start
#     [9, 0, 2, 2, -1],  # 1 = Bunny 0
#     [9, 3, 0, 2, -1],  # 2 = Bunny 1
#     [9, 3, 2, 0, -1],  # 3 = Bunny 2
#     [9, 3, 2, 2,  0],  # 4 = Bulkhead
# ]

# and a time limit of 1, the five inner array rows designate the starting point,
# bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could
# take the path:

# Start End Delta Time Status
#     -   0     -    1 Bulkhead initially open
#     0   4    -1    2
#     4   2     2    0
#     2   4    -1    1
#     4   3     2   -1 Bulkhead closes
#     3   4    -1    0 Bulkhead reopens; you and the bunnies exit

# With this solution, you would pick up bunnies 1 and 2. This is the best
# combination for this space station hallway, so the answer is [1, 2].

def initialise(nodes, s, parents, distances):
    distances[s] = 0
    parents[s] = None
    for node in [node for node in nodes if node != s]:
        distances[node] = float("inf")
        parents[node] = None

def relax(edge, weights, parents, distances):
    (u,v) = edge
    if (distances[v] > distances[u] + weights[(u,v)]):
        distances[v] = distances[u] + weights[(u,v)]
        parents[v] = u

def bellman_ford(nodes, edges, weights, s):
    parents = {}
    distances = {}
    initialise(nodes, s, parents, distances)

    for i in range(len(nodes) - 1):
        for edge in edges:
            relax(edge, weights, parents, distances)

    for edge in edges:
        (u,v) = edge
        if (distances[v] > distances[u] + weights[(u,v)]):
            return (nodes, None, None)

    return (nodes, parents, distances)

def johnson(nodes, edges, weights):
    parents = {}
    distances = {}

    nodes_prime = nodes[:]
    nodes_prime.append("s_prime")
    edges_prime = edges[:]
    weights_prime = weights.copy()
    for node in nodes:
        edges_prime.append(("s_prime", node))
        weights_prime[("s_prime", node)] = 0

    (_, _, h_values) = bellman_ford(nodes_prime, edges_prime, weights_prime, "s_prime")
    if (not h_values):
        return None
    
    weights_hat = {}
    for (u, v) in edges:
        weights_hat[(u,v)] = weights[(u,v)] + h_values[u] - h_values[v]
    
    for source_node in nodes:
        (_, parents_prime, distances_prime) = bellman_ford(nodes, edges, weights_hat, source_node)
        for node in nodes:
            parents[(source_node, node)] = parents_prime[node]
            distances[(source_node, node)] = distances_prime[node] - h_values[source_node] + h_values[node]
    
    return (nodes, parents, distances)

def pretty_print_all_pairs(title, nodes, parents, distances):
    print ("\n" + title)
    print ("----------------------------------------")
    if (not parents or not distances):
        print ("Negative cycle discovered!")
    else: 
        print("Parent Matrix:")

        # Print the empty space and vertical separator.
        print("{:>3}".format(""), end="")
        print("{:>4}".format("||"), end="")
        # Print the nodes in order.
        for node in nodes:
            print("{:>4}".format(node), end="")
        print("")

        # Print the horizontal separator.
        for i in range(len(nodes) + 2):
            print("{:=>4}".format("="), end="")
        print("")

        # Print the node, a vertical separator and the cell value.
        for source_node in nodes:
            print("{:>3}".format(source_node), end="")
            print("{:>4}".format("||"), end="")
            for node in nodes:
                print("{:>4}".format(parents[(source_node, node)] if parents[(source_node, node)] != None else "-"), end="")
            print("")

        print("\nDistance Matrix:")

        # Print the empty space and vertical separator.
        print("{:>3}".format(""), end="")
        print("{:>4}".format("||"), end="")
        # Print the nodes in order.
        for node in nodes:
            print("{:>4}".format(node), end="")
        print("")

        # Print the horizontal separator.
        for i in range(len(nodes) + 2):
            print("{:=>4}".format("="), end="")
        print("")

        # Print the node, a vertical separator and the cell value.
        for source_node in nodes:
            print("{:>3}".format(source_node), end="")
            print("{:>4}".format("||"), end="")
            for node in nodes:
                print("{:>4}".format(distances[(source_node, node)]), end="")
            print("")

    print("")

def create_graph(times):
    nodes = []
    edges = []
    weights = {}
    for start_index in range(len(times)):
        nodes.append(start_index)
        for end_index in range(len(times[start_index])):
            edges.append((start_index, end_index))
            weights[(start_index, end_index)] = times[start_index][end_index]
    return nodes, edges, weights

def get_intermediate_locations(old_location, new_location, parents):
    intermediate_locations = []
    parent = parents[(old_location, new_location)]
    while parent != old_location:
        intermediate_locations.append(parent)
        parent = parents[(old_location, parent)]
    intermediate_locations.reverse()
    return intermediate_locations

class Solution:

    def __init__(self, num_of_bunnies, times_limit):
        self.location_history = [[0]]
        self.location = 0
        self.bunnies_left = [i for i in range(1, num_of_bunnies + 1)] # Indexes of the bunnies in the times array.
        self.time_history = [times_limit]
        self.time_left = times_limit

    def move(self, new_location, parents, distances):
        path = [self.location] + get_intermediate_locations(self.location, new_location, parents) + [new_location]
        self.location_history.append(path)
        for location in path:
            if location in self.bunnies_left:
                self.bunnies_left.remove(location)
        self.time_left = self.time_left - distances[(self.location, new_location)]
        self.time_history.append(self.time_left)
        self.location = new_location

def solution(times, times_limit, debug=False):
    num_of_bunnies = len(times) - 2
    bulkhead_index = len(times) - 1

    nodes, edges, weights = create_graph(times)
    _, start_parents, start_distances = bellman_ford(nodes, edges, weights, 0)
    if not start_parents or not start_distances:
        if debug:
            print("Found a negative cycle!")
        return [i for i in range(num_of_bunnies)]    
    else:
        _, parents, distances = johnson(nodes, edges, weights)
        if debug:
            pretty_print_all_pairs("Johnson's Algorithm", nodes, parents, distances)
        
        queue = [Solution(num_of_bunnies, times_limit)]
        best_solutions = []
        best_num_of_bunnies_left = num_of_bunnies

        while len(queue) > 0:
            solution = queue.pop(0)
            if debug:
                print("\nCurrent solution history:")
                for path, time_left in zip(solution.location_history, solution.time_history):
                    print(path, time_left)
                print("Bunnies not visited: {}".format(solution.bunnies_left))

            # Check if the current solution is valid.
            time_left = solution.time_left - distances[(solution.location, bulkhead_index)]
            if time_left >= 0:
                # Check if solution is best found so far.
                bunnies_left = solution.bunnies_left[:]
                intermediate_locations = get_intermediate_locations(solution.location, bulkhead_index, parents)
                for location in intermediate_locations:
                    if location in bunnies_left:
                        bunnies_left.remove(location)                
                if len(bunnies_left) < best_num_of_bunnies_left:
                    best_num_of_bunnies_left = len(bunnies_left)
                    best_solutions = []
                    best_solutions.append(solution)
                elif len(bunnies_left) == best_num_of_bunnies_left:
                    best_solutions.append(solution)

                # Extend the solution by visiting a previously unseen bunny.
                for bunny in solution.bunnies_left:
                    copied_solution = copy.deepcopy(solution)
                    copied_solution.move(bunny, parents, distances)
                    queue.append(copied_solution)
        
        bunnies_collected = []
        for best_solution in best_solutions:
            best_solution.move(bulkhead_index, parents, distances)
            bunnies_collected.append([i-1 for i in range(1, bulkhead_index) if i not in best_solution.bunnies_left])
            if debug:
                print("\nBest solution history:")
                for path, time_left in zip(best_solution.location_history, best_solution.time_history):
                    print(path, time_left)
                print("Bunnies not visited: {}".format(best_solution.bunnies_left))
        bunnies_collected.sort()
        return bunnies_collected[0]

# Test Cases
failed = False

expected = [1, 2]
actual = solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = [0, 1]
actual = solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more test cases failed!")
