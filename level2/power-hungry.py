# Commander Lambda's space station is HUGE. And huge space stations take a LOT
# of power. Huge space stations with doomsday devices take even more power. To
# help meet the station's power needs, Commander Lambda has installed solar
# panels on the station's outer surface. But the station sits in the middle of a
# quasar quantum flux field, which wreaks havoc on the solar panels. You and
# your team of henchmen has been assigned to repair the solar panels, but you
# can't take them all down at once without shutting down the space station (and
# all those pesky life support systems!).
#
# You need to figure out which sets of panels in any given array you can take
# offline to repair while still maintaining the maximum amount of power output
# per array, and to do THAT, you'll first need to figure out what the maximum
# output of each array actually is. Write a function solution(xs) that takes a
# list of integers representing the power output levels of each panel in an
# array, and returns the maximum product of some non-empty subset of those
# numbers. So for example, if an array contained panels with power output levels
# of [2, -3, 1, 0, -5], then the maximum product would be found by taking the
# subset: xs[0] = 2, xs[1] = -3, xs[4] = -5, giving the product 2*(-3)*(-5) =
# 30. So answer([2,-3,1,0,-5]) will be "30".
#
# Each array of solar panels contains at least 1 and no more than 50 panels, and
# each panel will have a power output level whose absolute value is no greater
# than 1000 (some panels are malfunctioning so badly that they're draining
# energy, but you know a trick with the panels' wave stabilizer that lets you
# combine two negative-output panels to produce the positive output of the
# multiple of their power values). The final products may be very large, so give
# the answer as a string representation of the number.

def solution(xs):
    if len(xs) == 1:
        return str(xs[0])
    
    product = 1
    smallest_negative = -float("inf")
    num_of_negatives = 0
    num_of_positives = 0
    for x in xs:
        if x < 0:
            product *= x
            num_of_negatives += 1
            if x > smallest_negative:
                smallest_negative = x
        elif x > 0:
            product *= x
            num_of_positives += 1

    if (num_of_negatives > 0) and (num_of_negatives % 2 != 0):
        product /= smallest_negative
    
    if num_of_positives == 0 and num_of_negatives < 2:
        product = 0
    
    return str(product)

# Test Cases
failed = False

expected = "8"
actual = solution([2, 0, 2, 2, 0])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = "60"
actual = solution([-2, -3, 4, -5])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more test cases failed!")

# Custom Test Cases
failed = False

expected = "-10"
actual = solution([-10])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = "0"
actual = solution([0])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = "10"
actual = solution([10])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = "0"
actual = solution([0, 0])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = "0"
actual = solution([0, -10])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = "100"
actual = solution([0, -10, -10])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = "10"
actual = solution([10, -10])
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more custom test cases failed!")
