from functools import reduce
import hashlib as hl
import json
import pickle
from utils.hash_util import hash_block
from utils.verification import Verification
from collections import OrderedDict
from block import Block
from transaction import Transaction
from wallet import Wallet

# Initializing 
MINING_REWARD = 10

class Blockchain:

    def __init__(self, public_key, port):
        self.chain = [Block(0, '', [], 100, 0)]
        self.__open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.port = port
        self.load_data()

    
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


    @property
    def chain(self):
        return self.__chain[:]

    
    @chain.setter
    def chain(self, val):
        self.__chain = val


    def get_open_transactions(self):
        """Returns a copy of the open transactions list."""
        return self.__open_transactions[:]


    def load_data(self):
        try:
            with open('blockchain-{}.p'.format(self.port), mode='rb') as f:
                file_content = pickle.loads(f.read())
                if len(file_content) > 0: 
                    updated_blockchain = []
                    for block in file_content['chain']:
                        updated_blockchain.append(block)
                    self.chain = updated_blockchain
                    self.__open_transactions = file_content['ot']
                    self.__peer_nodes = set(file_content['peer_nodes'])
        except (IOError, IndexError):
            print('File not Found')
        finally:
            print('Cleanup')


    def save_data(self):
        try:
            with open('blockchain.p-{}'.format(self.port), mode='wb') as file:
                # file.write(json.dumps(blockchain))
                # file.write('\n')
                # file.write(json.dumps(open_transactions))
                save_data = {
                    'chain': self.__chain,
                    'ot': self.__open_transactions,
                    'peer_nodes': list(self.__peer_nodes)
                }
                file.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed')
        


    def get_last_blockchain_value(self):
        """ Getting last blockchain value """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def add_transaction(self, recipient, sender, signature, amount=1.0):
        
        """ Adding value to the blockchain
        
            Arguments:
                :sender: The sender of the coins.
                :recipient: The recipient of the coins.
                :amount: The amount of coins sent. Default 1.0.
        
        """
        
        transaction = Transaction(sender, recipient,  signature, amount)
    
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()

            return True

        return False


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0

        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1

        return proof


    def get_balance(self):
        if self.public_key == None:
            return None
        participant = self.public_key
        return self.get_amount_from_participant('recipient', participant) - self.get_amount_from_participant('sender', participant)


    def get_amount_from_participant(self, participantType, participant):
        if participantType == 'sender':
            amount_transactions = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
            open_tx = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
            amount_transactions.append(open_tx)
        else:
            amount_transactions = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        
        return reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, amount_transactions, 0)


    def mine_block(self):
        if self.check_hosting_node() == False:
            return None

        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        
        proof = self.proof_of_work()

        reward_transaction = Transaction('MINING', self.public_key, '', MINING_REWARD)
        
        copied_transactions = self.__open_transactions[:]

        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                print('Transaction verified and did not pass')
                return None
            else:
                print('Transaction verified')   

        copied_transactions.append(reward_transaction)
        
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()

        return block

    
    def check_hosting_node(self):
        if self.public_key == None:
            return False
    

    def add_peer_node(self, node):
        """ Adds a new node

            Arguments:
                :node: the node URL that will be added
        """
        self.__peer_nodes.add(node)
        self.save_data()

    
    def remove_peer_node(self, node):
        """ Removes a node

            Arguments:
                :node: the node URL that will be removed
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    
    def get_peer_nodes(self):
        """ Get all peer nodes """
        return list(self.__peer_nodes)