# Initializing 
blockchain = []


def get_last_blockchain_value():
    """ Getting last blockchain value """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction=[1]):
    """ Adding value to the blockchain
    
        Arguments:
            :transaction_amoun: The amount to be added at the end
            :last_transaction: The last transaction should be always added to create the chaining
    
     """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    """ Getting user input to be added to the blockchain"""
    return float(input('Your transaction amount: '))


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
    # block_index = 0
    is_valid = True

    for block_index in range(len(blockchain)):
        #print(blockchain[block_index][0])
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False

    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     elif block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
        
    #     block_index += 1

    return is_valid


waiting_for_quit = True


while waiting_for_quit:
    print('Please choose')
    print('1 - Add a new transaction value')
    print('2 - Output the blockchain blocks')
    print('h - Manipulate chain')
    print('q - To quit')

    user_choice = get_user_choice()

    if user_choice == '1':
        add_transaction(get_transaction_value(), get_last_blockchain_value())
    elif user_choice == '2':
        output_blocks()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        print('Done')
        waiting_for_quit = False
    else:
        print('Input invalid, please choose other.')
    
    if not verify_chain():
        output_blocks()
        print('Invalid blockchain')
        break
else:
    print('User left')