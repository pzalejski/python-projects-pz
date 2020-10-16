import hashlib, json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # create the starting block
        self.new_block(previous_hash=1, proof=100)
        

    def new_block(self, proof, previous_hash=None):
       '''Create a new block in the blockchain

       Parameters
       -----------
       proof: (int)
            the proof given by the proof of work algorithm


       previous_hash:(optional) (str)
            hash of previous block
       
       Returns
       -----------
       return: (dict) 
            New block '''
       
       block = {
           'index': len(self.chain) + 1,
           'timestamp': time(),
           'transactions': self.current_transactions,
           'proof': proof,
           'previous_hash': previous_hash or self.hash(self.chain[-1])
       }

       # reset the current list of transactions
       self.current_transactions = []
       
       self.chain.append(block)
       return block


    def new_transaction(self, sender, recipient, amount):
        '''
        Creates a new transaction to go into the next mined block

        Parameters
        -----------
        sender: (str)
            Address of the Sender


        recipient: (str)
            Address of the Recipient


        amount: (int)
            Amount

        Returns
        -----------

        return: (int)
            The index of the block that will hold this transaction
        '''

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        '''creates a SHA-256 hash of a block
        
        Parameters
       -----------
       block: (dict)
            block

       Returns
       -----------
        return: (str) '''
        
        # we must make sure that the dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dump(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        # returns the last block in the chain
        pass