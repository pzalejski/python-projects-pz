import hashlib, json
from time import time
from uuid import uuid4
from textwrap import dedent

from flask import Flask, jsonify, request

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
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        # returns the last block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm
        - Find a number p' such that has(pp') cointains 4 leading zeroes, where p is the previous p'
        -p is the prvious proof, and p' is the new proof

        Args:
            last_proof: (int)

        Returns:
            return: (int)
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
            
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) cointain 4 leading zeroes?


        Args:
            last_proof (int): Previous Proof
            proof (int): Current Proof

        Returns:
            return: (bool) True if correct, False if not
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash =  hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
        
# Instantiate our Node
app = Flask(__name__)

# generate a golobably unique address for this node
node_identifier = str(uuid4()).replace("-", '')

# instantiate the blockchain
blockchain = Blockchain()

@app.route("/mine", methods = ['GET'])
def mine():
    return "We'll mine a new block"

@app.route('/transactions/new', methods=['Post'])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    