from collections import OrderedDict
from utils.printable import Printable

class Transaction(Printable):
    """ The transaction which will be added to a block of a blockchain 
    
        Attributes:
            :sender: the sender
            :recipient: the recipient
            :signature: the signature of the transaction
            :amount: the amount of the transaction
    
    """
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])