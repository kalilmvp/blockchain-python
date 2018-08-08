from time import time

class Block:
    
    def __init__(self, index, previous_hash, transactions, proof, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.time = time() if timestamp is None else timestamp

    def __repr__(self):
        return 'index: {} / previous_hash: {} / transactions: {} / proof: {} / timestamp: {}'.format(self.index, self.previous_hash, self.transactions, self.proof, self.time)
        