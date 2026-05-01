import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, sender, receiver, amount, previous_hash, risk_level):
        self.index = index
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.previous_hash = previous_hash
        self.risk_level = risk_level
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index, "timestamp": self.timestamp, "sender": self.sender,
            "receiver": self.receiver, "amount": self.amount, 
            "previous_hash": self.previous_hash, "risk_level": self.risk_level
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "System", "Root", 0, "0", "LOW")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, sender, receiver, amount, risk_level):
        last_block = self.get_last_block()
        new_block = Block(len(self.chain), time.time(), sender, receiver, amount, last_block.hash, risk_level)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash() or current.previous_hash != previous.hash:
                return False
        return True

    def tamper_block(self, index, new_amount):
        if index < len(self.chain):
            self.chain[index].amount = new_amount
            return True
        return False
