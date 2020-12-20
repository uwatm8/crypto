import hashlib
import math

# TODO add possibility of having more than a 16th of a 2 exponential in difficulty
def solveHash(difficulty, key):
    n = 0
    zeros = math.log(difficulty, 2)
    wholeZeros = math.floor(zeros - zeros % 1)
    extraRequired = hex(round(0xF * (zeros % 1)))

    res = hashlib.sha384((key + str(n)).encode("utf-8")).hexdigest()

    remainder = 0xF

    while res[:wholeZeros] != "0" * wholeZeros or remainder < extraRequired:
        res = hashlib.sha384((key + str(n)).encode("utf-8")).hexdigest()

        n += 1

        remainder = hex(int(res[wholeZeros : wholeZeros + 1], 16))
    return n


difficulty = 50
sol = solveHash(difficulty, "hey dude")

print("solution ", sol)
