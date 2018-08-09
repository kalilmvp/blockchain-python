from time import time

from utils.printable import Printable

class Block(Printable):
    
    def __init__(self, index, previous_hash, transactions, proof, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.time = time() if timestamp is None else timestamp 
        