# You're almost ready to make your move to destroy the LAMBCHOP doomsday device,
# but the security checkpoints that guard the underlying systems of the LAMBCHOP
# are going to be a problem. You were able to take one down without tripping any
# alarms, which is great! Except that as Commander Lambda's assistant, you've
# learned that the checkpoints are about to come under automated review, which
# means that your sabotage will be discovered and your cover blown - unless you
# can trick the automated review system.
#
# To trick the system, you'll need to write a program to return the same
# security checksum that the guards would have after they would have checked all
# the workers through. Fortunately, Commander Lambda's desire for efficiency
# won't allow for hours-long lines, so the checkpoint guards have found ways to
# quicken the pass-through rate. Instead of checking each and every worker
# coming through, the guards instead go over everyone in line while noting their
# security IDs, then allow the line to fill back up. Once they've done that they
# go over the line again, this time leaving off the last worker. They continue
# doing this, leaving off one more worker from the line each time but recording
# the security IDs of those they do check, until they skip the entire line, at
# which point they XOR the IDs of all the workers they noted into a checksum and
# then take off for lunch. Fortunately, the workers' orderly nature causes them
# to always line up in numerical order without any gaps.
#
# For example, if the first worker in line has ID 0 and the security checkpoint
# line holds three workers, the process would look like this:

# 0 1 2 /
# 3 4 / 5
# 6 / 7 8

# where the guards' XOR (^) checksum is 0^1^2^3^4^6 == 2.
#
# Likewise, if the first worker has ID 17 and the checkpoint holds four workers,
# the process would look like:

# 17 18 19 20 /
# 21 22 23 / 24
# 25 26 / 27 28
# 29 / 30 31 32

# which produces the checksum 17^18^19^20^21^22^23^25^26^29 == 14.
#
# All worker IDs (including the first worker) are between 0 and 2000000000
# inclusive, and the checkpoint line will always be at least 1 worker long.
#
# With this information, write a function solution(start, length) that will
# cover for the missing security checkpoint by outputting the same checksum the
# guards would normally submit before lunch. You have just enough time to find
# out the ID of the first worker to be checked (start) and the length of the
# line (length) before the automatic review occurs, so your program must
# generate the proper checksum with just those two values.

def solution(start, length):
    line_ranges = []
    cut_off = length
    while cut_off != 0:
        line_ranges.append((start, start + cut_off - 1))
        start += length
        cut_off -= 1
        
    checksum = 0
    for start, end in line_ranges:
        checksum ^= smart_xor_range(start, end)    
    return checksum

# This method uses the following property to efficiently xor a range of numbers
# starting at start and ending at end:
#     (0 ^ ... ^ start - 1) ^ (0 ^ ... ^ end)
#   = (0 ^ ... ^ start - 1) ^ (0 ^ ... ^ start - 1 ^ start ^ ... ^ end)
#   = start ^ ... ^ end
def smart_xor_range(start, end):
    start_xor = smart_xor(start - 1)
    end_xor = smart_xor(end)
    return start_xor ^ end_xor

# This method efficiently finds the XOR of 0 ^ ... ^ number.
# 
# An even number in binary has the last bit equal to 0. 2n ^ (2n + 1) = 1,
# because all bits are the same except for the last one. We can pair up numbers
# in the sequence as follows:

#   0 ^ 1 (= 1)
#   2 ^ 3 (= 1)
#   4 ^ 5 (= 1)
#   6 ^ 7 (= 1)

# Each pair of pairs will cancel each other out (1 ^ 1 = 0). The number of
# numbers is number + 1, since we include the 0 at the start.
#
# There can be four different cases:
#
#   1. (number + 1) % 4 == 0. We can successfully pair up all numbers and pair
#      up all pairs. The result is 0.
#   2. (number + 1) % 4 == 1. After pairing up numbers and pairing up all pairs,
#      there is one number left. The result is the number.
#   3. (number + 1) % 4 == 2. After pairing up all numbers and pairing up pairs,
#      there is one pair left. The result is 1.
#   4. (number + 1) % 4 == 3. After pairing up numbers and pairing up pairs,
#      there is one pair and one number left. The result is 1 ^ number. However,
#      in this case the number left over is always an even number (if it was
#      odd, it would've been paired up) and 1 ^ 2n == 2n + 1 (it just flips the
#      last bit from 0 to 1). Therefore the result is number + 1.
def smart_xor(number):
    remainder = (number + 1) % 4
    if remainder == 0:
        return 0
    elif remainder == 1:
        return number
    elif remainder == 2:
        return 1
    elif remainder == 3:
        return number + 1
    else:
        print("Error @ smart_xor({})!".format(number))

# Test Cases
failed = False

expected = 2
actual = solution(0, 3)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = 14
actual = solution(17, 4)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more test cases failed!")
