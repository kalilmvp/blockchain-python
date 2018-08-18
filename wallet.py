from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256  
import Crypto.Random
import binascii

class Wallet:
    def __init__(self, port):
        self.private_key = None
        self.public_key = None
        self.port = port
    

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key


    def save_keys(self):
        if self.private_key != None and self.public_key != None:
            try:
                with open('wallet.txt-{}'.format(self.port), mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                return True
            except(IOError, IndexError):
                print('Saving wallet failed')
                return False


    def load_keys(self):
        try:
            with open('wallet.txt-{}'.format(self.port), mode='r') as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
            return True
        except(IOError, IndexError):
            print('Loading wallet failed')
            return False


    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), 
                binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    
    def sign_transaction(self, sender, recipient, amount):
        signer = PKCS1_PSS.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')


    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_PSS.new(public_key)

        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))

        return verifier.verify(h, binascii.unhexlify(transaction.signature))

