# Initializing 
blockchain = []


def get_last_blockchain_value():
    """ Getting last blockchain value """
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    """ Adding value to the blockchain
    
        Arguments:
            :transaction_amoun: The amount to be added at the end
            :last_transaction: The last transaction should be always added to create the chaining
    
     """
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    """ Getting user input to be added to the blockchain"""
    return float(input('Your transaction amount: '))


add_value(get_user_input())
add_value(get_user_input(), get_last_blockchain_value())
add_value(get_user_input(), get_last_blockchain_value())


print(blockchain)
