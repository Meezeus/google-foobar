# There's some unrest in the minion ranks: minions with ID numbers like "1",
# "42", and other "good" numbers have been lording it over the poor minions who
# are stuck with more boring IDs. To quell the unrest, Commander Lambda has
# tasked you with reassigning everyone new, random IDs based on her Completely
# Foolproof Scheme.
#
# She's concatenated the prime numbers in a single long string:
# "2357111317192329...". Now every minion must draw a number from a hat. That
# number is the starting index in that string of primes, and the minion's new ID
# number will be the next five digits in the string. So if a minion draws "3",
# their ID number will be "71113".
#
# Help the Commander assign these IDs by writing a function solution(n) which
# takes in the starting index n of Lambda's string of all primes, and returns
# the next five digits in the string. Commander Lambda has a lot of minions, so
# the value of n will always be between 0 and 10000.

# This method uses the Sieve of Eratosthenes to find prime numbers. For more
# information, see https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
def solution(i):
    primes = []
    prime_str = ""
    current_number = 2
    while len(prime_str) < i + 5:
        # Check if current number is a multiple of any found primes.
        prime_factors = [prime for prime in primes if current_number % prime == 0]
        # If not, current number is a new prime.
        if len(prime_factors) == 0:
            primes.append(current_number)
            prime_str += str(current_number)
        current_number += 1    
    return prime_str[i:i+5]

# Test Cases
failed = False

expected = "23571"
actual = solution(0)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

expected = "71113"
actual = solution(3)
if actual != expected:
    print("Expected {}, actual {}".format(expected, actual))
    failed = True

if failed:
    raise Exception("One or more test cases failed!")
