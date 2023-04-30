from flask import Flask, jsonify, request
import hashlib
import datetime
import random
import json

class Validator:
    def __init__(self, name, address, balance, stake):
        self.name = name
        self.address = address
        self.balance = balance
        self.stake = stake
        
    def __repr__(self):
        return f"{self.name} ({self.address})"
    
    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "balance": self.balance,
            "stake": self.stake
        }

class Block:
    def __init__(self, transactions, prev_block_hash, validator):
        self.transactions = transactions
        self.timestamp = datetime.datetime.now()
        self.prev_block_hash = prev_block_hash
        self.validator = validator
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_contents = str(self.timestamp) + str(self.prev_block_hash) + str(self.transactions) + str(self.validator.address)
        return hashlib.sha256(block_contents.encode()).hexdigest()
        
    def __repr__(self):
        return f"Block({self.hash}, {self.prev_block_hash}, {self.transactions}, {self.validator})"
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "prev_block_hash": self.prev_block_hash,
            "transactions": self.transactions,
            "validator": self.validator.to_dict(),
            "hash": self.hash
        }

class Blockchain:
    def __init__(self, genesis_block, num_validators):
        self.chain = [genesis_block]
        self.validators = self.generate_validators(num_validators)
        
    def add_block(self, transactions):
        prev_block = self.chain[-1]
        validator = self.select_validator()
        new_block = Block(transactions, prev_block.hash, validator)
        self.chain.append(new_block)
        return new_block
    
    def generate_validators(self, num_validators):
        validators = []
        for i in range(num_validators):
            name = f"Validator{i}"
            address = f"address{i}"
            balance = 1000
            stake = random.randint(1, 100)
            validators.append(Validator(name, address, balance, stake))
        return validators
    
    def select_validator(self):
        total_stake = sum([v.stake for v in self.validators])
        target = random.uniform(0, total_stake)
        cum_stake = 0
        for validator in self.validators:
            cum_stake += validator.stake
            if cum_stake > target:
                return validator
    
    def validate(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i-1]
            if curr_block.prev_block_hash != prev_block.hash:
                return False
            if curr_block.hash != curr_block.calculate_hash():
                return False
        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            if block.validator.address == address:
                balance += 1
        return balance
    
    def __repr__(self):
        return f"Blockchain({self.chain})"
    
    def to_dict(self):
        return {
            "chain": [block.to_dict() for block in self.chain],
            "validators": [validator.to_dict() for validator in self.validators]
        }

# Create blockchain
genesis_block = Block([], "0", Validator("Alice", "address1", 100, 50))
blockchain = Blockchain(genesis_block, 5)

# Create Flask app
app = Flask(__name__)

# Custom JSON encoder class to serialize Block and Validator objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Block):
            return obj.to_dict()
        
        if isinstance(obj, Validator):
            return obj.to_dict()
        
        return super().default(obj)

# Set the JSON encoder for the app
app.json_encoder = CustomJSONEncoder

# POST request to add transaction
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
        
    transactions = [f"Transaction {blockchain.chain[-1]}-1", f"Transaction {blockchain.chain[-1]}-2"]
    block = blockchain.add_block(transactions)
    response = {'message': f'Transaction will be added to Block {block.hash}'}
    return jsonify(response), 201

# GET request to mine a new block
@app.route('/mine', methods=['GET'])
def mine():
    transactions = [f"Transaction {blockchain.chain[-1]}-1", f"Transaction {blockchain.chain[-1]}-2"]
    block = blockchain.add_block(transactions)
    response = {
        'message': "New Block Forged",
        'index': len(blockchain.chain),
        'transactions': block.transactions,
        'prev_block_hash': block.prev_block_hash,
        'validator': block.validator,
        'hash': block.hash,
    }
    return jsonify(response), 200

# GET request to get the full blockchain
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# Run the app
if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=500, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)