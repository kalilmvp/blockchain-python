# Initializing 
cgenesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
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
    participants.add(sender)
    participants.add(recipient)


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    return get_amount_from_participant('recipient', participant) - get_amount_from_participant('sender', participant)


def get_amount_from_participant(participantType, participant):
    amount_transactions = [[tx['amount'] for tx in block['transactions'] if tx[participantType] == participant] for block in blockchain]
    
    amount = 0
    for tx in amount_transactions:
        if (len(tx) > 0):
            amount += tx[0]

    return amount


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    # print(hashed_block)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
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
    """ Verify the current blockchain and return True if it´s valid """

    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        
    return True


waiting_for_quit = True


while waiting_for_quit:
    print('Please choose')
    print('1 - Add a new transaction value')
    print('2 - Mine block')
    print('3 - Output the blockchain blocks')
    print('4 - Output participants')
    print('h - Manipulate chain')
    print('q - To quit')

    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        
        recipient, amount = tx_data

        add_transaction(recipient, amount=amount)

        # print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        output_blocks()
    elif user_choice == '4':
        print(participants)
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

    print('Balance: ' + repr(get_balance('Kalil')))
else:
    print('User left')