import hashlib as hl
import json

def hash_string_256(value):
    return hl.sha256(value.encode()).hexdigest()


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """

    hashed_block = block.__dict__.copy()

    hashed_block['transactions'] = [tx.to_ordered_dict() for tx in hashed_block['transactions']]

    return hash_string_256(json.dumps(hashed_block, sort_keys=True))