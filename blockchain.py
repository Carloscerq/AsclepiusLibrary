import hashlib
import json
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import requests
from flask import Flask, jsonify, request
from multiprocessing import Process
from client import root

# Só pra facilitar testes
port = 5000


class Blockchain:
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.currentData = []

        # genesis block
        self.new_Block(previous_hash='1', proof=100)

    def register_node(self, adress):
        parsed_url = urlparse(adress)

        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)

    def valid_chain(self, blockchain):
        lastBlock = blockchain[0]

        for block in blockchain:
            if block == lastBlock:
                continue

            print(lastBlock)
            print(block)

            lastBlockHash = self.hash(lastBlock)
            if block['previous_hash'] != lastBlockHash:
                return False

            if not self.valid_proof(lastBlock['proof'], block['proof'], lastBlockHash):
                return False

            lastBlock = block

        return True

    def new_Block(self, proof, previous_hash):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': self.currentData,
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.currentData = []

        self.chain.append(block)
        return block

    def sendNewBlock(self, block):

        neighbours = self.nodes
        content = block['data'][0]

        data = {
            'index': block['index'],
            'DoctorId': content['DoctorId'],
            'data': content['data'],
            'Pacient': content['Pacient'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }

        for node in neighbours:
            requests.post(f'http://{node}/att/chain', data=data)

    def resolve_conflicts(self):

        neighbours = self.nodes
        biggestLen = len(self.chain)
        newChain = None

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > biggestLen and self.valid_chain(chain):
                    biggestLen = length
                    newChain = chain

        if newChain:
            self.chain = newChain
            return True

        return False

    def newData(self, doctorID, Pacient, data):
        self.currentData.append({
            'DoctorId': doctorID,
            'data': data,
            'Pacient': Pacient
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_block):
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof = proof + 1

        return proof

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        guess_hash = hashlib.sha256(
            f'{last_proof}{proof}{last_hash}'.encode()).hexdigest()
        return guess_hash[:4] == "0000"


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])  # OK
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_Block(proof, previous_hash)

    blockchain.sendNewBlock(block)

    return json.dumps({
        'message': 'NEW BLOCK',
        'index': block['index'],
        'data': block['data'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }), 200


@app.route('/att/chain', methods=['POST'])
def newBlockchain():

    index = request.form['index']
    DoctorId = request.form['DoctorId']
    data = request.form['data']
    Pacient = request.form['Pacient']
    proof = request.form['proof']
    previou_hash = request.form['previous_hash']

    blockchain.newData(DoctorId, Pacient, data)
    blockchain.new_Block(proof, previou_hash)

    return jsonify({'a': 'a'})


@app.route('/Data/new', methods=['GET'])  # OK
def new_data():
    DoctorID = request.args.get("Doctorid")
    Data = request.args.get('data')
    Pacient = request.args.get('Pacient')

    blockchain.newData(DoctorID, Pacient, Data)
    print(DoctorID, Data, Pacient)

    response = {'message': 'New Request send',
                'currentData': blockchain.currentData
                }
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])  # OK
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['GET'])
def register():
    newnode = request.args.get('newnode')

    response = {
        'message': 'your node have been added',
        'nodes': list(blockchain.nodes)
    }
    blockchain.register_node(newnode)

    # Só pra testes
    myUrl = 'http://localhost:' + port + '/'
    print(myUrl)
    requests.get(f'{newnode}/nodes/response?newnode={myUrl}')

    return jsonify(response)


@app.route('/nodes/response', methods=['GET'])
def responsenode():
    newnode = newnode = request.args.get('newnode')

    blockchain.register_node(newnode)

    return jsonify({
        'message': 'your node has been added'
    })


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':

    '''from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()

    port = args.port'''

    pr1 = Process(target=lambda: app.run(host='0.0.0.0', port=port))
    pr1.start()
    pr2 = Process(target=root.mainloop())
    pr2.start()