import hashlib
import json
import time


class Block:
    def __init__(self, index, sender, receiver, amount, category, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.category = category
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Creates a unique fingerprint of this block.
        If ANY field changes, the hash changes completely.
        """
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "category": self.category,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "category": self.category,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        """First block ever — has no previous hash."""
        genesis = Block(
            index=0,
            sender="SYSTEM",
            receiver="SYSTEM",
            amount=0,
            category="Genesis",
            previous_hash="0"
        )
        self.chain.append(genesis)

    def add_block(self, sender, receiver, amount, category="General"):
        """Adds a new transaction block linked to the previous one."""
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            sender=sender,
            receiver=receiver,
            amount=amount,
            category=category,
            previous_hash=previous_block.hash  # ← This is the chain link!
        )
        self.chain.append(new_block)
        return new_block.to_dict()

    def get_chain(self):
        return [block.to_dict() for block in self.chain]

    def verify_integrity(self):
        """
        Walk the entire chain and verify every hash.
        Returns which block was tampered with, if any.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Re-calculate the hash and compare
            if current.hash != current.calculate_hash():
                return {
                    "valid": False,
                    "broken_at_block": i,
                    "reason": f"Block {i} data was tampered — hash mismatch"
                }

            # Check the chain link
            if current.previous_hash != previous.hash:
                return {
                    "valid": False,
                    "broken_at_block": i,
                    "reason": f"Block {i} is not linked to block {i - 1} — chain broken"
                }

        return {"valid": True, "total_blocks": len(self.chain), "message": "Chain is intact"}

    def get_stats(self):
        """Analytics: summary of the whole chain."""
        blocks = self.get_chain()[1:]  # skip genesis block
        if not blocks:
            return {
                "total_blocks": 0,
                "total_amount": 0,
                "suspicious_count": 0,
                "categories": {}
            }

        from detector import is_suspicious

        total_amount = sum(b["amount"] for b in blocks)
        suspicious_count = sum(1 for b in blocks if is_suspicious(b["amount"], [], b["sender"])["flagged"])

        # Count by category
        categories = {}
        for b in blocks:
            cat = b["category"]
            categories[cat] = categories.get(cat, 0) + b["amount"]

        # Top sender and receiver
        senders = {}
        receivers = {}
        for b in blocks:
            senders[b["sender"]] = senders.get(b["sender"], 0) + b["amount"]
            receivers[b["receiver"]] = receivers.get(b["receiver"], 0) + b["amount"]

        return {
            "total_blocks": len(blocks),
            "total_amount": round(total_amount, 2),
            "suspicious_count": suspicious_count,
            "categories": categories,
            "top_sender": max(senders, key=senders.get) if senders else None,
            "top_receiver": max(receivers, key=receivers.get) if receivers else None
        }