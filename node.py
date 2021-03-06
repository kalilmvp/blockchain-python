from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from wallet import Wallet

from blockchain import Blockchain

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/network', methods=['GET'])
def get_network():
    return send_from_directory('ui', 'network.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'message': 'Keys added',
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding Keys failed'
        }

        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'message': 'Load keys',
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Load Keys failed'
        }

        return jsonify(response), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Balance get',
            'funds': balance
        }

        return jsonify(response), 500
    else:
        response = {
            'message': 'Getting balance failed',
            'wallet_set_up': wallet.public_key != None
        }

        return jsonify(response), 500


@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = blockchain.get_open_transactions()

    dict_open_transactions = [tx.__dict__.copy() for tx in transactions]

    response = {
        'message': 'Fetched transactions successfully',
        'transactions': dict_open_transactions
    }

    return jsonify(response), 200


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'No wallet set-up'
        }
        return jsonify(response), 400

    values = request.get_json()

    if not values:
        response = {
            'message': 'No data found', 
        }
        return jsonify(response), 400
    
    required_fields = ['recipient', 'amount']
    if not all(fields in values for fields in required_fields):
        response = {
            'message': 'Required data is needed', 
        }
        return jsonify(response), 400
    
    recipient = values['recipient']
    amount = values['amount']
    
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)

    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)

    if success:
        response = {
            'message': 'Transaction added',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Error when creating transaction'
        }
        return jsonify(response), 500

@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    
    if block != None:
        block_dict = block.__dict__.copy()
        block_dict['transactions'] = [tx.__dict__.copy() for tx in block_dict['transactions']]

        response = {
            'message': 'Block added',
            'block': block_dict,
            'funds': blockchain.get_balance(),
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = blockchain.chain
    block_dict = [block.__dict__.copy() for block in chain]
    for block in block_dict:
        block['transactions'] = [tx.__dict__.copy() for tx in block['transactions']]
    return jsonify(block_dict), 200 


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data attached'
        }
        return jsonify(response), 400

    if 'node' not in values:
        response = {
            'message': 'No node data found'
        }
        return jsonify(response), 400
    
    blockchain.add_peer_node(values['node'])

    response = {
        'message': 'Node added',
        'all_nodes': blockchain.get_peer_nodes()
    }

    return jsonify(response), 201


@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'No node found'
        }
        return jsonify(response), 400
    
    blockchain.remove_peer_node(node_url)

    response = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_peer_nodes()
    }

    return jsonify(response), 200


@app.route('/nodes', methods=['GET'])
def get_nodes():
    response = {
        'message': 'Nodes fetched', 
        'nodes': blockchain.get_peer_nodes(),
    }

    return jsonify(response), 200

    
if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)

    args = parser.parse_args()
    print('Args: {}'.format(args))
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)
