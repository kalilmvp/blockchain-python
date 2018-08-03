from functools import reduce
import hashlib as hl
import json
import pickle
from collections import OrderedDict

from hash_util import hash_string_256, hash_block

# Initializing 
MINING_REWARD = 10
GENESIS_BLOCK = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [GENESIS_BLOCK]
open_transactions = []
owner = 'Kalil'
participants = { owner }

hack_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [
        {
            'sender': 'Anyone',
            'recipient': 'Anyone 1',
            'amount': 1.0
        }]
}


def load_data():
    with open('blockchain.p', mode='rb') as f:
        file_content = pickle.loads(f.read())
        print(file_content)
        if len(file_content) > 0: 
             global blockchain
             blockchain = file_content['chain']
             global open_transactions    
             open_transactions = file_content['ot']


load_data()


def save_data():
    with open('blockchain.p', mode='wb') as file:
        # file.write(json.dumps(blockchain))
        # file.write('\n')
        # file.write(json.dumps(open_transactions))
        save_data = {
            'chain': blockchain,
            'ot': open_transactions
        }
        file.write(pickle.dumps(save_data))


def get_last_blockchain_value():
    """ Getting last blockchain value """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    
    """ Adding value to the blockchain
    
        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent. Default 1.0.
    
     """
    
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }

    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
        
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)

        save_data()

        return True

    return False


def valid_proof(transactions, last_hash, proof):
    guess = str(transactions) + str(last_hash) +  str(proof)
    guess_hash = hash_string_256(guess)

    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0

    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1

    return proof


def get_balance(participant):
    return get_amount_from_participant('recipient', participant) - get_amount_from_participant('sender', participant)


def get_amount_from_participant(participantType, participant):
    amount_transactions = [[tx['amount'] for tx in block['transactions'] if tx[participantType] == participant] for block in blockchain]
    
    #print(amount_transactions)
    if participantType == 'sender':
        open_tx = [tx['amount'] for tx in open_transactions if tx[participantType] == participant]
        amount_transactions.append(open_tx)

    #print(amount_transactions)

    return reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, amount_transactions, 0)

    # amount = 0
    # for tx in amount_transactions:
    #     if (len(tx) > 0):
    #         amount += tx[0]
    
    # return amount


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    
    proof = proof_of_work()

    reward_transaction = OrderedDict([('sender', 'MINING'),('recipient', owner),('amount', MINING_REWARD)])

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }

    blockchain.append(block)
    return True


def get_transaction_value():
    """ Getting user input to be added to the blockchain"""
    tx_recipient = input('The recipient: ')
    tx_amount = float(input('Your transaction amount: '))
    return (tx_recipient, tx_amount)


def get_user_choice():
    return input('Your choice: ')


def output_blocks():
    #print('Complete blockchain: ' + repr(blockchain))
    for block in blockchain:
        print('Block: ')
        print(block)
    else:
        print('-' * 40)


def verify_chain():
    """ Verify the current blockchain and return True if it's valid """

    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        #validating proof of work, minus the reward transaction
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work invalid')
            return False
        
    return True


waiting_for_quit = True


while waiting_for_quit:
    print('Please choose')
    print('1 - Add a new transaction value')
    print('2 - Mine block')
    print('3 - Output the blockchain blocks')
    print('4 - Output participants')
    print('5 - Check validaty of transactions')
    print('h - Manipulate chain')
    print('q - To quit')

    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        
        recipient, amount = tx_data

        if add_transaction(recipient, amount=amount):
            print('Transaction added')
        else:
            print('Failed to add, balance does not match')

        # print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        output_blocks()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('Invalid transaction')

    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = hack_block
    elif user_choice == 'q':
        print('Done')
        waiting_for_quit = False
    else:   
        print('Input invalid, please choose other.')
    
    if not verify_chain():
         output_blocks()
         print('Invalid blockchain')
         break

    print('Balance of {}: {:6.2f} '.format('Kalil', get_balance('Kalil')))
else:
    print('User left')