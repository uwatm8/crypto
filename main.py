import hashlib
import math
import random
import json


TRANSACTIONS_PER_BLOCK = 10
BLOCK_DIFFICULTY = 2 ** 4  # block difficulty is expressed linearly
BLOCK_REWARD = 100

thisWallet = random.randbytes(16).hex()
print("this wallet: ", thisWallet)


def solveHash(blockData):
    n = random.randint(
        0, 1000000000
    )  # each miner randomizes start point, making expected value linear to hasing power
    zeros = math.log(BLOCK_DIFFICULTY, 2)
    wholeZeros = math.floor(zeros - zeros % 1)
    extraRequired = hex(round(0xF * (zeros % 1)))

    res = hashlib.sha384((blockData + str(n)).encode("utf-8")).hexdigest()
    remainder = 0xF
    while res[:wholeZeros] != "0" * wholeZeros or remainder < extraRequired:
        res = hashlib.sha384((blockData + str(n)).encode("utf-8")).hexdigest()
        n += 1
        remainder = hex(int(res[wholeZeros : wholeZeros + 1], 16))
    return n, res


key = "0"
blockdata = "{ blockNumber: 0, prevBlock: " + str(key) + "}"

blocks = []

ledger = open("ledger.json")

# blocks
for i in range(2):
    nonce, solution = solveHash(str(blockdata))
    key = solution

    transactions = [{"from": 0, "to": thisWallet, "amount": BLOCK_REWARD}]

    blockdata = {
        "blockNumber": i,
        "hash": key,
        "prevBlockHash": blocks[i - 1]["hash"] if i else "0",
        "nonce": nonce,
        "transactions": transactions,
    }

    print(blockdata)
    blocks.append(blockdata)

print(blocks)