import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse
import random
import string
import hashlib
from flask import Flask, jsonify, request
from uuid import uuid4

class Account:
    def __init__(self, name, address, balance):
        self.name = name
        self.address = address
        self.balance = balance

class Blockchain(object):
    def __init__(self, num_validators):
        self.chain = []
        self.nodes = set()
        self.transactions = []
        self.validators = self.generate_validators(num_validators)

        self.new_block(previous_hash=1)
    
    def new_block(self, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.chain.append(block)
        self.transactions = []
        return block
    
    def new_transaction(self, sender, recipient, amount, balance):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'balance': balance,
        })
        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def generate_random_address(self):
        letters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(letters) for i in range(32))
        return random_string

    def generate_validators(self, num_validators):
        validators = []
        for i in range(num_validators):
            name = f"Account{i}"
            address = self.generate_random_address()+str(i)
            balance = random.randint(1, 100)
            validators.append(Account(name, address, balance))
        return validators

    def proof_of_stake(self):
        total_stake = sum([v.balance for v in self.validators])
        rand = random.uniform(0, total_stake)
        selected_validator = None
        for validator in self.validators:
            if validator.balance == 0:
                validator.balance = 1
            if rand < validator.balance:
                selected_validator = validator
                validator.balance -= 1
                break
            rand -= validator.balance
        selected_validator.balance += 42
        return selected_validator

    def register_node(self, address):
        self.nodes.add((urlparse(address)).netloc)
    
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(last_block)
            print(block)
            if block['previous hash'] != self.hash(last_block):
                return False
            last_block = block
            current_index += 1
        return True
    
    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            if block.validator.address == address:
                balance += 1
        return balance
    
    def solve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.valid_chain(chain):
                    new_chain = chain
                    max_length = length
        if new_chain is not None:
            self.chain = new_chain
            return True
        else:
            return False
        
app = Flask(__name__)

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    if not all(item in values for item in ['sender', 'recipient', 'amount', 'balance']):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'], values['balance'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    selected=(blockchain.proof_of_stake())
    blockchain.new_transaction(
        sender="0",
        recipient=selected.address,
        amount=42,
        balance=selected.balance
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'timestamp': block['timestamp'],
        'transactions': block['transactions'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/chain', methods = ['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length':len(blockchain.chain)
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
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.solve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is still valid',
            'new_chain': blockchain.chain
        }
    return jsonify(response), 200

if __name__ == '__main__':
    print("Introduce Port:")
    port_i = int(input())
    print("\nIntroduce number of accounts:")
    number_acc = int(input())
    blockchain = Blockchain(number_acc)
    app.run(host='0.0.0.0', port = port_i)