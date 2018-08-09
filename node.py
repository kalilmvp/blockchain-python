from blockchain import Blockchain
from utils.verification import Verification
from uuid import uuid4

class Node:

    def __init__(self):
        #self.id = str(uuid4())
        self.id = "MAX"
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        """ Getting user input to be added to the blockchain"""
        tx_recipient = input('The recipient: ')
        tx_amount = float(input('Your transaction amount: '))
        return (tx_recipient, tx_amount)


    def get_user_choice(self):
        return input('Your choice: ')


    def output_blocks(self):
        for block in self.blockchain.chain:
            print('Block: ')
            print(block)
        else:
            print('-' * 40)


    def listen_for_input(self):
        waiting_for_quit = True

        while waiting_for_quit:
            print('Please choose')
            print('1 - Add a new transaction value')
            print('2 - Mine block')
            print('3 - Output the blockchain blocks')
            print('4 - Check validaty of transactions')
            print('q - To quit')

            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                
                recipient, amount = tx_data

                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print('Transaction added')
                else:
                    print('Failed to add, balance does not match')

                # print(open_transactions)
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.output_blocks()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('Invalid transaction')

            elif user_choice == 'q':
                print('Done')
                waiting_for_quit = False
            else:   
                print('Input invalid, please choose other.')
            
            verifier = Verification()
            if not Verification.verify_chain(self.blockchain.chain):
                self.output_blocks()
                print('Invalid blockchain')
                break

            print('Balance of {}: {:6.2f} '.format(self.id, self.blockchain.get_balance()))
        else:
            print('User left')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()