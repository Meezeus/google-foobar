# Commander Lambda uses an automated algorithm to assign minions randomly to
# tasks, in order to keep her minions on their toes. But you've noticed a flaw
# in the algorithm - it eventually loops back on itself, so that instead of
# assigning new minions as it iterates, it gets stuck in a cycle of values so
# that the same minions end up doing the same tasks over and over again. You
# think proving this to Commander Lambda will help you make a case for your next
# promotion. 
#
# You have worked out that the algorithm has the following process: 
#
#   1. Start with a random minion ID n, which is a nonnegative integer of length
#      k in base b
#   2. Define x and y as integers of length k.  x has the digits of n in
#      descending order, and y has the digits of n in ascending order
#   3. Define z = x - y.  Add leading zeros to z to maintain length k if
#      necessary
#   4. Assign n = z to get the next minion ID, and go back to step 2
#
# For example, given minion ID n = 1211, k = 4, b = 10, then x = 2111, y = 1112
# and z = 2111 - 1112 = 0999. Then the next minion ID will be n = 0999 and the
# algorithm iterates again: x = 9990, y = 0999 and z = 9990 - 0999 = 8991, and
# so on.
#
# Depending on the values of n, k (derived from n), and b, at some point the
# algorithm reaches a cycle, such as by reaching a constant value. For example,
# starting with n = 210022, k = 6, b = 3, the algorithm will reach the cycle of
# values [210111, 122221, 102212] and it will stay in this cycle no matter how
# many times it continues iterating. Starting with n = 1211, the routine will
# reach the integer 6174, and since 7641 - 1467 is 6174, it will stay as that
# value no matter how many times it iterates.
#
# Given a minion ID as a string n representing a nonnegative integer of length k
# in base b, where 2 <= k <= 9 and 2 <= b <= 10, write a function solution(n, b)
# which returns the length of the ending cycle of the algorithm above starting
# with n. For instance, in the example above, solution(210022, 3) would return
# 3, since iterating on 102212 would return to 210111 when done in base 3. If
# the algorithm reaches a constant, such as 0, then the length is 1.

def solution(n, b):
    debug = False
    cycle = False
    n_list = [n]
    while not cycle:
        next_n = calculate_next_n(n, b)
        if next_n in n_list:
            cycle = True
            if debug:
                print(n_list)
        n_list.append(next_n)
        n = next_n

    cycle_list = n_list[n_list.index(n):]
    if debug:
        print(cycle_list)
    cycle_length = len(cycle_list)-1
    if debug:
        print(cycle_length)
    return(cycle_length)

def calculate_next_n(n, b, debug=False):    
    k = len(n)

    digits = [int(d) for d in n]
    x = sorted(digits, reverse=True)
    y = sorted(digits)
    if debug:
        print(x)
        print(y)

    num_x = 0
    num_y = 0
    for i in range(k):
        num_x += (b**i) * x[k-i-1]
        num_y += (b**i) * y[k-i-1]
    if debug:
        print(num_x)
        print(num_y)

    num_z = num_x - num_y
    z = []
    for i in range(k-1, -1, -1):
        quotient = int(num_z / (b**i))
        z.append(str(quotient))
        num_z -= (b**i) * quotient
    if debug:
        print(z)

    new_n = "".join(z)
    if debug:
        print(new_n)
        print("")
    return new_n

# Test Cases
failed = False

expected = 1
actual = solution("1211", 10)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 3
actual = solution("210022", 3)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more test cases failed!")
