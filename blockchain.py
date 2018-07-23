# Initializing 
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Kalil'


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
    
    open_transactions.append(
        {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
    )

def mine_block():
    last_block = blockchain[-1]
    hashed_block = '-'.join([str(last_block[key]) for key in last_block])

    print(hashed_block)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }

    blockchain.append(block)

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
    # block_index = 0
    # is_valid = True

    # for block_index in range(len(blockchain)):
    #     #print(blockchain[block_index][0])
    #     if block_index == 0:
    #         continue
    #     elif blockchain[block_index][0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False

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

    # return is_valid


waiting_for_quit = True


while waiting_for_quit:
    print('Please choose')
    print('1 - Add a new transaction value')
    print('2 - Mine block')
    print('3 - Output the blockchain blocks')
    print('h - Manipulate chain')
    print('q - To quit')

    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        
        recipient, amount = tx_data

        add_transaction(recipient, amount=amount)

        # print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        output_blocks()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        print('Done')
        waiting_for_quit = False
    else:
        print('Input invalid, please choose other.')
    
    # if not verify_chain():
    #     output_blocks()
    #     print('Invalid blockchain')
    #     break
else:
    print('User left')