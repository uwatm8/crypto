import hashlib
import math
import random
import json

TRANSACTIONS_PER_BLOCK = 10
BLOCK_DIFFICULTY = 2 ** 6  # block difficulty is expressed linearly
BLOCK_REWARD = 100

thisWallet= random.randint(0,2**31)
print("this wallet: ", thisWallet)

def get_ledger_data():
    with open('ledger.json') as json_file:
        return json.load(json_file)

ledger = get_ledger_data()
blocks = [] if not len(ledger) else ledger

def solve_hash(blockData):
    n = random.randint(0, 1000000000)  # each miner randomizes start point, making expected value linear to hashing power regardless of computational power per client
    zeros = math.log(BLOCK_DIFFICULTY, 2)
    wholeZeros = math.floor(zeros - zeros % 1)
    extraRequired = hex(round(0xF * (zeros % 1)))
    start_n = n

    res = hashlib.sha384((blockData + str(n)).encode("utf-8")).hexdigest()
    remainder = 0xF
    while res[:wholeZeros] != "0" * wholeZeros or remainder < extraRequired:
        res = hashlib.sha384((blockData + str(n)).encode("utf-8")).hexdigest()
        n += 1
        remainder = hex(int(res[wholeZeros : wholeZeros + 1], 16))

        if not (n-start_n) % 100000:
            current_public_ledger = get_ledger_data()
            if len(blocks) != len(current_public_ledger): # Another client found hash before, abondon
                return -1, -1
                
    print(f"found solution after {n-start_n} iterations")
    return n, res

key = "0" if not len(ledger) else str(ledger[len(ledger)-1]["blockNumber"])
blockdata = "{ blockNumber: " + str(int(key) + 1) + ", prevBlock: " + str(key) + "}"
ledger = open("ledger.json")

# blocks
for i in range(10):
    nonce, solution = solve_hash(str(blockdata))
    if nonce == -1:
        print("ANOTHER CLINET FOUND BLOCK, SEARCHING FOR NEXT BLOCK")
        blocks = get_ledger_data()
        continue

    key = solution
    transactions = [{"from": 0, "to": thisWallet, "amount": BLOCK_REWARD}]
    blockdata = {
        "blockNumber": len(blocks),
        "hash": key,
        "prevBlockHash": blocks[i - 1]["hash"] if len(blocks) else "0",
        "nonce": nonce,
        "transactions": transactions,
    }

    blocks.append(blockdata)
    json_object = json.dumps(blocks, indent=4)
    with open("ledger.json", "w") as outfile:
        outfile.write(json_object)
