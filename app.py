import json

from flask import Flask, request, jsonify
import requests
from Blockchain import Blockchain
from Block import Block
import time

app = Flask(__name__)

blockchain = Blockchain()

blockchain.add_new_transaction('Ed sent 96 coins to Corvo Attano.')
blockchain.add_new_transaction('Ed received 400 coins from user17171007.')

prev_block = blockchain.return_last_block
new_block = Block(prev_block.index+1, blockchain.pending_transactions, time.time(), prev_block.hash)
blockchain.add_block(new_block, blockchain.proof_of_work(new_block))


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    response = {
        'chain length': len(chain_data),
        'chain': chain_data
    }

    return json.dumps({'length: ': len(chain_data),
                       'chain: ': chain_data})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
