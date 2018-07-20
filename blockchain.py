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


def get_transaction_value():
    """ Getting user input to be added to the blockchain"""
    return float(input('Your transaction amount: '))


def get_user_choice():
    return input('Your choice: ')


def output_blocks():
    for block in blockchain:
        print('Block: ')
        print(block)

add_value(get_transaction_value())

while True:
    print('Please choose')
    print('1 - Add a new transaction value')
    print('2 - Output the blockchain blocks')
    print('q - To quit')

    user_choice = get_user_choice()

    if user_choice == '1':
        add_value(get_transaction_value(), get_last_blockchain_value())
    elif user_choice == '2':
        output_blocks()
    elif user_choice == 'q':
        print('Done')
        break
    else:
        print('Input invalid, please choose other.')