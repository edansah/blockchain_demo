from Block import Block
import time


class Blockchain:
    # difficulty of the Proof of Work algorithm (number of leading zeros)
    difficulty = 3

    def __init__(self):
        self.pending_transactions = []
        self.chain = []
        # genesis block is created whenever a blockchain is instantiated
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Creates the genesis block and appends it to the blockchain.
        """
        genesis_block = Block(0, [], time.time(), '0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def return_last_block(self) -> Block:
        """
        Returns the last (most recent) block in the blockchain.
        """
        return self.chain[-1]

    @staticmethod
    def proof_of_work(block) -> str:
        """
        Proof of Work algorithm that makes it progressively harder to perform the work required to create
        a new block. This method checks for a value (nonce value) that starts with a certain number of leading zeroes
        . The number of leading zeroes is known as the difficulty.
        :param block: <Block> Block instance
        :return: <str> Hash of the block
        """
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    @staticmethod
    def valid_proof(block, block_hash) -> bool:
        """
        Checks whether a block's hash is valid and has the correct number of leading zeroes
        :param block: <Block> Block instance
        :param block_hash: <str> Block's hash
        :return: bool
        """
        return block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash()

    def add_block(self, block, proof) -> bool:
        """
        Checks whether provided argument (Block)'s previous hash is equal to the hash of the last block in the chain
        :param block: <Block> Block instance
        :param proof: <str>
        :return: <bool>
        """
        previous_hash = self.return_last_block.hash
        if previous_hash != block.previous_hash or not Blockchain.valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def add_new_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine(self) -> int:
        """
        Checks whether there is some mining to do (pending transactions list can't be empty).
        If so, creates a new Block, adds the pending transactions to it, does the PoW algorithm,
        adds it to the blockchain and empties the transactions list.
        :return: <int> The index of the new block in the blockchain
        """
        if not self.pending_transactions:
            return False

        last_block = self.return_last_block

        new_block = Block(last_block.index+1, self.pending_transactions, time.time(), last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.pending_transactions = []
        return new_block.index

