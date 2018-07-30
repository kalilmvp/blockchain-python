import hashlib as hl
import json

def hash_string_256(value):
    return hl.sha256(value.encode()).hexdigest()


def hash_block(block):
    return hash_string_256(json.dumps(block, sort_keys=True))