import hashlib, json
from time import time
from uuid import uuid4
from textwrap import dedent

from flask import Flask, jsonify, request

import requests

from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.nodes = set()

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

    
    def register_node(self, address):
        """
        Add a new node to the list of nodes

        Args:       
            address (str): address of node eg "http://192.168.0.5:5000'

        Returns:
            return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        Args:
            chain (list): a blockshain

        Returns:
            bool: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n----------\n")

            # check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is the Consensus Algo, it resolves conflicts by prelacing the chain with the longest one in the network.

        Returns:
            bool: True if our chain was replaced ,False if not
        """
        
        neighbours = self.nodes
        new_chain = None

        # only looking for chains longer than ours
        max_len = len(self.chain)

        # grab and verify the chains from all the nodes in our network 
        for node in neighbours:

            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # check if the length is longer and the chain is valid
                if length > max_len and self.valid_chain(chain):
                    max_len = length
                    new_chain = chain

        # replace our chain if discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        
        return False

# Instantiate our Node
app = Flask(__name__)

# generate a golobably unique address for this node
node_identifier = str(uuid4()).replace("-", '')

# instantiate the blockchain
blockchain = Blockchain()

@app.route("/mine", methods = ['GET'])
def mine():
    # we run the proof of work algo to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # we must receive a reward for finding the proof
    # the sender is "0" to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check that the required fields are in the posted data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to the Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': "New nodes have been added",
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response),201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': "Our chain was replaced",
            'new chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=input("enter port: "))
