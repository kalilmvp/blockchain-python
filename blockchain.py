from functools import reduce
import hashlib as hl
import json
import pickle
from hash_util import hash_block
from collections import OrderedDict
from block import Block
from transaction import Transaction
from verification import Verification

blockchain = []
open_transactions = []

# Initializing 
MINING_REWARD = 10
owner = 'Kalil'

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
    try:
        global blockchain
        global open_transactions
        
        with open('blockchain.p', mode='rb') as f:
            file_content = pickle.loads(f.read())
            if len(file_content) > 0: 
                updated_blockchain = []
                for block in file_content['chain']:
                    updated_blockchain.append(block)
                blockchain = updated_blockchain
                open_transactions = file_content['ot']
    except (IOError, IndexError) as error:
        blockchain = [Block(0, '', [], 100, 0)]
        open_transactions = []
        print('File not Found')
    finally:
        print('Cleanup')


load_data()


def save_data():
    try:
        with open('blockchain.p', mode='wb') as file:
            # file.write(json.dumps(blockchain))
            # file.write('\n')
            # file.write(json.dumps(open_transactions))
            save_data = {
                'chain': blockchain,
                'ot': open_transactions
            }
            file.write(pickle.dumps(save_data))
    except IOError as identifier:
        print('Saving failed')
    


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

    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        
        save_data()

        return True

    return False


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0

    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1

    return proof


def get_balance(participant):
    return get_amount_from_participant('recipient', participant) - get_amount_from_participant('sender', participant)


def get_amount_from_participant(participantType, participant):
    if participantType == 'sender':
        amount_transactions = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
        open_tx = [tx.amount for tx in open_transactions if tx.sender == participant]
        amount_transactions.append(open_tx)
    else:
        amount_transactions = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    
    #print(amount_transactions)    

    #print(amount_transactions)

    return reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, amount_transactions, 0)

    # amount = 0
    # for tx in amount_transactions:
    #     if (len(tx) > 0):
    #         amount += tx[0]
    
    # return amount


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    
    proof = proof_of_work()

    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    blockchain.append(Block(len(blockchain), hashed_block, copied_transactions, proof))

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


waiting_for_quit = True


while waiting_for_quit:
    print('Please choose')
    print('1 - Add a new transaction value')
    print('2 - Mine block')
    print('3 - Output the blockchain blocks')
    print('4 - Check validaty of transactions')
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
        verifier = Verification()
        if verifier.verify_transactions(open_transactions, get_balance):
            print('All transactions are valid')
        else:
            print('Invalid transaction')

    elif user_choice == 'q':
        print('Done')
        waiting_for_quit = False
    else:   
        print('Input invalid, please choose other.')
    
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
         output_blocks()
         print('Invalid blockchain')
         break

    print('Balance of {}: {:6.2f} '.format('Kalil', get_balance('Kalil')))
else:
    print('User left')