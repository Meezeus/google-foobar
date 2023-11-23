# The time for the mass escape has come, and you need to distract the guards so
# that the bunny prisoners can make it out! Unfortunately for you, they're
# watching the bunnies closely. Fortunately, this means they haven't realized
# yet that the space station is about to explode due to the destruction of the
# LAMBCHOP doomsday device. Also fortunately, all that time you spent working as
# first a minion and then a henchman means that you know the guards are fond of
# bananas. And gambling. And thumb wrestling.
#
# The guards, being bored, readily accept your suggestion to play the Banana
# Games.
#
# You will set up simultaneous thumb wrestling matches. In each match, two
# guards will pair off to thumb wrestle. The guard with fewer bananas will bet
# all their bananas, and the other guard will match the bet. The winner will
# receive all of the bet bananas. You don't pair off guards with the same number
# of bananas (you will see why, shortly). You know enough guard psychology to
# know that the one who has more bananas always gets over-confident and loses.
# Once a match begins, the pair of guards will continue to thumb wrestle and
# exchange bananas, until both of them have the same number of bananas. Once
# that happens, both of them will lose interest and go back to guarding the
# prisoners, and you don't want THAT to happen!
#
# For example, if the two guards that were paired started with 3 and 5 bananas,
# after the first round of thumb wrestling they will have 6 and 2 (the one with
# 3 bananas wins and gets 3 bananas from the loser). After the second round,
# they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point
# they stop and get back to guarding.
#
# How is all this useful to distract the guards? Notice that if the guards had
# started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 ->
# 4, 1 -> 3, 2 -> 1, 4 and so on.
#
# Now your plan is clear. You must pair up the guards in such a way that the
# maximum number of guards go into an infinite thumb wrestling loop!
#
# Write a function solution(banana_list) which, given a list of positive
# integers depicting the amount of bananas the each guard starts with, returns
# the fewest possible number of guards that will be left to watch the prisoners.
# Element i of the list will be the number of bananas that guard i (counting
# from 0) starts with.
#
# The number of guards will be at least 1 and not more than 100, and the number
# of bananas each guard starts with will be a positive integer no more than
# 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

# Useful website for Edmond's Blossom algorithm:
# https://algorithms.discrete.ma.tum.de/graph-algorithms/matchings-blossom-algorithm/index_en.html
#
# Edmond's Blossom code taken from: https://github.com/yorkyer/edmonds-blossom

class Node:
    index = 0

    def __init__(self):
        self.neighbours = []
        self.visited = False
        self.parent = None
        self.mate = None
        self.index = Node.index
        Node.index += 1

    def __repr__(self):
        return str(self.index)

class SuperNode(Node):

    def __init__(self):
        Node.__init__(self)
        self.original_nodes = []
        self.original_edges = []

class Path:

    def __init__(self):
        self.nodes = []

    def __repr__(self):
        return str(self.nodes)
    
    def replace(self, super_node):
        index = self.nodes.index(super_node)
        previous_nodes = self.nodes[:index]
        # Find the link between the outer node and the inner node.
        current_node = previous_nodes[-1]
        for inner_node, outer_node in super_node.original_edges:
            if outer_node == current_node:
                current_node = inner_node
                break
        # Add the inner nodes to the path.
        inner_nodes = []
        while current_node.parent != super_node.parent:
            inner_nodes.append(current_node)
            inner_nodes.append(current_node.mate)
            for neighbour_node in current_node.mate.neighbours:
                if neighbour_node != current_node and neighbour_node in super_node.original_nodes:
                    current_node = neighbour_node
                    break
        inner_nodes.append(current_node)
        # Combine the paths.
        self.nodes = previous_nodes + inner_nodes + self.nodes[index+1:]

    def invert(self):
        assert len(self.nodes) % 2 == 0
        for i in range(0, len(self.nodes), 2):
            self.nodes[i].mate = self.nodes[i+1]
            self.nodes[i+1].mate = self.nodes[i]
    
class EdmondsBlossom:

    def __init__(self, vertices, edges):
        Node.index = 0
        self.nodes = [Node() for vertex in vertices]
        for i, j in edges:
            self.nodes[i].neighbours.append(self.nodes[j])
        self.free_nodes = []
        for node in self.nodes:
            self.free_nodes.append(node)
        self.super_nodes = []
        self.DEBUG = False

    def find_ancestors(self, node):
        ancestors = [node]
        while node.parent != None:
            node = node.parent
            ancestors.append(node)
        return ancestors

    def find_cycle(self, node1, node2):
        ancestors1 = self.find_ancestors(node1)
        ancestors2 = self.find_ancestors(node2)
        # The nodes will have common ancestors until a certain point, at which they
        # will diverge.
        i = len(ancestors1) - 1
        j = len(ancestors2) - 1
        while ancestors1[i] == ancestors2[j]:
            i -= 1
            j -= 1
        cycle = ancestors1[:i+1] + ancestors2[j+1::-1]
        return cycle

    def contract_blossom(self, blossom):
        super_node = SuperNode()
        for blossom_node in blossom:
            super_node.original_nodes.append(blossom_node)
            for neighbour_node in blossom_node.neighbours:
                if neighbour_node not in blossom:
                    super_node.original_edges.append((blossom_node, neighbour_node))
                    if neighbour_node.parent in blossom:
                        neighbour_node.parent = super_node
        
        for inner_node, outer_node in super_node.original_edges:
            inner_node.neighbours.remove(outer_node)
            outer_node.neighbours.remove(inner_node)
            super_node.neighbours.append(outer_node)
            outer_node.neighbours.append(super_node)

        if self.DEBUG:
            print("Contracted blossom consisting of nodes: {}".format(super_node.original_nodes))

        return super_node
    
    def expand_super_node(self, super_node):
        assert isinstance(super_node, SuperNode)
        for inner_node, outer_node in super_node.original_edges:
            inner_node.neighbours.append(outer_node)
            outer_node.neighbours.append(inner_node)
            super_node.neighbours.remove(outer_node)
            outer_node.neighbours.remove(super_node)
    
    def construct_augmenting_path(self, node):
        # Create the initial path. All paths will have at least the node itself
        # and its parent.
        path = Path()
        path.nodes.append(node)
        node = node.parent
        path.nodes.append(node)
        # Keep adding parent nodes until you get to the root (inclusive).
        while node.mate != None:
            node = node.parent
            path.nodes.append(node)
        # The path includes super nodes. These need to be expanded.
        while len(self.super_nodes) > 0:
            super_node = self.super_nodes.pop()
            self.expand_super_node(super_node)
            path.replace(super_node)
        return path
    
    def find_augmenting_path(self, root):
        queue = [root]
        while len(queue) > 0:
            current_node = queue.pop(0)
            current_node.visited = True
            if self.DEBUG:
                print("Searching, current node = {}".format(current_node))

            for neighbour_node in current_node.neighbours:
                # Ignore the neighbour if it is the parent of the current node.
                if neighbour_node == current_node.parent:
                    continue

                # If the neighbour has already been visited, we have a cycle.
                elif neighbour_node.visited: 
                    cycle = self.find_cycle(current_node, neighbour_node)
                    # If the cycle length is odd, we must contract the blossom.
                    if len(cycle) % 2 == 1:
                        # Contract blossom
                        super_node = self.contract_blossom(cycle)
                        self.super_nodes.append(super_node)
                        # Remove inner nodes from queue
                        for node in cycle:
                            if node in queue:
                                queue.remove(node)
                        # Find blossom root
                        blossom_root = neighbour_node
                        while blossom_root.parent in cycle:
                            blossom_root = blossom_root.parent
                        super_node.parent = blossom_root.parent
                        super_node.mate = blossom_root.mate
                        # Add super node to queue
                        super_node.visited = True
                        queue.insert(0, super_node)
                        break
                    
                # If the neighbour is unmatched, we have found an augmenting
                # path.
                elif neighbour_node.mate == None:
                    neighbour_node.parent = current_node
                    return self.construct_augmenting_path(neighbour_node)
                
                # If the neighbour is matched, continue searching.
                elif neighbour_node.mate != current_node:
                    neighbour_node.visited = True
                    neighbour_node.parent = current_node
                    neighbour_node.mate.visited = True
                    neighbour_node.mate.parent = neighbour_node
                    queue.append(neighbour_node.mate)
        return None
    
    def edmonds_blossom(self):
        if self.DEBUG:
            print("\n##########\nStarting Edmond's Blossom\n##########")
            
        while len(self.free_nodes) > 1:
            if self.DEBUG:
                print("\nRemaining free nodes: {}".format(self.free_nodes))
            for root_node in self.free_nodes:
                if self.DEBUG:
                    print("Searching with {} as root".format(root_node))
                # Reset nodes
                for node in self.nodes:
                    node.visited = False
                    node.parent = None
                # Search for an augmenting path.
                path = self.find_augmenting_path(root_node)
                if path:
                    if self.DEBUG:
                        print("Found augmenting path: {}".format(path))
                    path.invert()
                    self.free_nodes.remove(path.nodes[0])
                    self.free_nodes.remove(path.nodes[-1])
                    break
            else:
                # For loop executed without breaking: cannot find an augmenting
                # path. Break out of the while loop.
                break

            for node in self.nodes:
                if node.mate:
                    assert node.mate.mate == node
        
        matching = {}
        for node in self.nodes:
            if node.mate:
                matching[node] = node.mate
        return matching

def wrestle(banana1, banana2):
    bet = min(banana1, banana2)
    if banana1 == bet:
        banana1 += bet
        banana2 -= bet
    elif banana2 == bet:
        banana2 += bet
        banana1 -= bet
    return banana1, banana2

def find_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def infinite_wrestle(banana1, banana2):
    previous_gcd = 0
    new_gcd = find_gcd(banana1, banana2)
    # If the gcd does not change, the sequence will not terminate.
    while (previous_gcd != new_gcd) and (banana1 != banana2):
        banana1, banana2 = wrestle(banana1, banana2)
        previous_gcd = new_gcd
        new_gcd = find_gcd(banana1, banana2)
    return banana1 != banana2

def construct_graph(banana_list):
    vertices = []
    edges = []
    for index1 in range(len(banana_list)):
        vertices.append(index1)
        for index2 in range(len(banana_list)):
            if infinite_wrestle(banana_list[index1], banana_list[index2]):
                edges.append((index1, index2))
    return vertices, edges

def solution(banana_list):
    vertices, edges = construct_graph(banana_list)
    if len(edges) == 0:
        return len(banana_list)
    else:
        matching = EdmondsBlossom(vertices, edges).edmonds_blossom()
        return len(banana_list) - len(matching)

# Wrestling Test Cases
failed = False

expected = False
actual = infinite_wrestle(1, 1)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = False
actual = infinite_wrestle(1, 3)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = True
actual = infinite_wrestle(1, 5)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = True
actual = infinite_wrestle(2, 4)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = True
actual = infinite_wrestle(3, 7)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = True
actual = infinite_wrestle(2, 16)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = False
actual = infinite_wrestle(5, 5)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = False
actual = infinite_wrestle(100, 100)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = False
actual = infinite_wrestle(5, 11)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more wrestling test cases failed!")

# Edmonds Blossom Test Cases
failed = False

vertices = [0, 1, 2, 3]
edges = [(0, 2), (2, 0),
         (0, 1), (1, 0),
         (2, 1), (1, 2),
         (1, 3), (3, 1)]
matching = EdmondsBlossom(vertices, edges).edmonds_blossom()
expected = 2
actual = len(matching) / 2
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
edges = [(8, 0), (0, 8),
         (0, 1), (1, 0),
         (1, 2), (2, 1),
         (2, 3), (3, 2),
         (3, 4), (4, 3),
         (3, 7), (7, 3),
         (7, 9), (9, 7),
         (4, 5), (5, 4),
         (7, 6), (6, 7),
         (5, 6), (6, 5)]
matching = EdmondsBlossom(vertices, edges).edmonds_blossom()
expected = 5
actual = len(matching) / 2
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
edges = [(5, 3), (3, 5),
         (3, 6), (6, 3),
         (6, 2), (2, 6),
         (2, 1), (1, 2),
         (0, 1), (1, 0),
         (4, 0), (0, 4),
         (4, 5), (5, 4),
         (3, 4), (4, 3),
         (3, 2), (2, 3),
         (0, 7), (7, 0),
         (1, 7), (7, 1),
         (9, 4), (4, 9),
         (9, 8), (8, 9),
         (8, 0), (0, 8),
         (2, 11), (11, 2),
         (11, 10), (10, 11),
         (10, 1), (1, 10)]
matching = EdmondsBlossom(vertices, edges).edmonds_blossom()
expected = 6
actual = len(matching) / 2
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

vertices = [0, 1, 2, 3, 4, 5]
edges = [(0, 1), (1, 0),
         (1, 2), (2, 1),
         (0, 3), (3, 0),
         (3, 1), (1, 3),
         (1, 4), (4, 1),
         (4, 2), (2, 4),
         (3, 4), (4, 3),
         (3, 5), (5, 3),
         (5, 4), (4, 5)]
matching = EdmondsBlossom(vertices, edges).edmonds_blossom()
expected = 3
actual = len(matching) / 2
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more Edmonds Blossom test cases failed!")

# Test Cases
failed = False

expected = 2
actual = solution([1, 1])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 0
actual = solution([1, 7, 3, 21, 13, 19])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more test cases failed!")

# Custom Test Cases
failed = False

expected = 1
actual = solution([2, 7, 7])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 2
actual = solution([1, 1, 1, 2])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 1
actual = solution([2, 3, 4])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 1
actual = solution([1, 3, 11])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 0
actual = solution([2, 2, 4, 4])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 1
actual = solution([2, 2, 1])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 3
actual = solution([1, 1, 1])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 3
actual = solution([2, 2, 2])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 100
actual = solution([1073741824 for _ in range(100)])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 1
actual = solution([1])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more custom test cases failed!")
