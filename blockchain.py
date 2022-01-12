# <Importing the Various Modukes and Libraries>
import sys

import hashlib
import json #json 데이터를 처리하기 위해서 사용

from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

import requests

from urllib.parse import urlparse

# <Declaring the Class named Blockchain>
class Blockchain(object):# with two methods

    difficulty_target = "0000"

    def hash_block(self, block):
        block_encoded = json.dumps(block, sort_keys = True).encode()# 블록을 바이트 배열로 ecode 하고
        return hashlib.sha256(block_encoded).hexdigest()#해시로 변환하여 반환
    #class의 생성자
    def __init__(self):# self = 인스턴스 자체
        self.nodes = set()
        #전체 블록체인의 모든 블록을 저장
        self.chain = []#list
        #현재 블록에 대한 트랜잭션을 임시로 저장
        self.current_transactions = []

        # 인덱스 0으로 시작하는 이전 블록인 genesis block의 fixed hash로
        # create the genesis block

        genesis_hash = self.hash_block("genesis_block")
        self.append_block(
            hash_of_previous_block = genesis_hash,
            nonce = self.proof_of_work(0, genesis_hash, [])
            )
    
    # <nonce값 찾기>
    # use PoW to find the nonce for the current block
    def proof_of_work(self, index, hash_of_previous_block, transactions):
        #try with nonce = 0
        nonce = 0
        #유효할때까지 이전 블록의 해시에 nonce를 해시하기
        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:#해시한 nonce가 difficulty와 맞지 않는다면
            nonce +=1#1만큼 증가 시키고 다시 해시
    
        return nonce

    #check to see if the block's hash meets the difficulty target 기능을 하는 함수
    def valid_proof(self, index, hash_of_previous_block, transactions, nonce):
        #nonce를 포함하여 이전블록의 해시와 내용을 포함하는 문자열 생성
        content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()
        #sha256 해시함수 사용
        content_hash = hashlib.sha256(content).hexdigest()

        return content_hash[:len(self.difficulty_target)] == self.difficulty_target#check

    # <Appending the Block to the Blockchain>
    # 새로운 블록을 생성하고 블록체인에 추가하는 기능을 하는 함수
    def append_block(self, nonce, hash_of_previous_block):
        block = {
            'index': len(self.chain),
            'timestamp': time(),#블록체인에 블록에 추가될때 현재 timestamp 또한 블록에 추가된다
            'transactions': self.current_transactions,
            'nonce': nonce,
            'hash_of_previous_block': hash_of_previous_block
            }
        
        self.current_transactions = [] #현재 트랜잭션 리스트를 reset
        self.chain.append(block)#새로운 블록을 블록체인에 추가

        return block
        
    # <Adding Transactions>
    # 트랜잭션을 추가하는 함수
    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'amount': amount,
            'recipient': recipient,
            'sender': sender,
            })
        return self.last_block['index'] + 1 #이전 블록의 index에 1추가
    
    #블록체인의 마지막 블록을 얻기 위해서는 define a property called last_block in the Blockchain class
    @property
    def last_block(self):
        #마지막 블록을 return
        return self.chain[-1]
    # 노드 목록에 새 노드 추가
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        print(parsed_url.netloc)
    # 주어진 블록체인이 유효한지 확인
    def valid_chain(self, chain):
        last_block = chain[0] #제네시스 블록
        current_index = 1 #두번재 블록부터 시작

        while current_index < len(chain):
            block = chain[current_index] #현재 블록 받아오기
            #이전 블록의 해시가 올바른지 확인하고 기록된 현재 블록의 이전 해시인지 확인
            if block['hash_of_previous_block'] != self.hash_block(last_block):
                return False
            #올바른 nonce인지 확인
            if not self.valid_proof(
                current_index,
                block['hash_of_previous_block'],
                block['transactions'],
                block['nonce']):
                return False

            # 블록체인의 다음 블록으로 이동
            last_bock = block
            current_index += 1
        return True #유효한 블록체인이라면
    def update_blockchain(self):
        #등록된 우리 주변 노드들을 가져옴
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)#for simplicity, 우리보다 더 긴 체인 찾기
        #우리 네트워크에서 모든 노드를 확인
        for node in neighbours:
            #get the blockchain from the other nodes
            response = requests.get(f'http://{node}/blockchain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
            #길이가 더 길고 체인이 유효한지 확인
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain
        #유효하고 더 긴 체인이 발견된다면, 체인을 replace
        if new_chain:
            self.chain = new_chain
            return True
        return False

# <Exposing the Blockchain Class as a REST API>
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '') #이 노드에 고유한 주소를 생성

blockchain = Blockchain()#블록체인 인스턴스화
# <Obtaining the full blockchain>
#retrun the entire blockchain
@app.route('/blockchain', methods = ['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200
# <Performing Mining>
#채굴자가 블록을 채굴할 수 있는 경로를 만들어서 블록을 추가할 수 있도록 함
@app.route('/mine', methods = ['GET'])
def mine_block():
    # miner는 이 노드가 새로운 코인을 채굴했음을 나타내기 위해 보낸 사람이 0 
    #이라는 증거를 찾는데에 대한 보상을 받아야함
    blockchain.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    #블록체인의 마지막 블록의 hash obtain
    last_block_hash = blockchain.hash_block(blockchain.last_block)
    #Pow를 사용하여 블록체인에 추가할 새로운 블록의 nonce값 찾기
    index = len(blockchain.chain)
    nonce = blockchain.proof_of_work(index, last_block_hash, blockchain.current_transactions)
    #마지막 블록의 해시와 현재 nonce값을 이용하여 새로운 블록을 블록체인에 추가하기
    block = blockchain.append_block(nonce, last_block_hash)
    response = {
        'message': "New Block Mined",
        'index': block['index'], 
        'hash_of_previous_block': block['hash_of_previous_block'],
        'nonce': block['nonce'],
        'transactions': block['transactions'],
    }
    return jsonify(response), 200
# <Adding Transactions>
@app.route('/transactions/new', methods = ['POST'])
def new_transaction():
    values = request.get_json()#클라이언트에서 전달된 값을 가져옴
    #필수 필드가 POST 데이터에 있는지 확인
    required_fields = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required_fields):
        return ('Missing fields', 400)
    #새로운 트랜잭션 생성
    index = blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
        )
    response = {'message': f'Transaction will be added to Block {index}'}

    return (jsonify(response), 201)

@app.route('/nodes/add_nodes', methods=['POST'])
def add_nodes():
    #클라이언트에서 전달된 노드 가져오기
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Missing node(s) info", 400

    for node in nodes:
        blockchain.add_node(node)
        
    response = {
        'message': 'New nodes added',
        'nodes': list(blockchain.nodes),
        }

    return jsonify(response), 201

@app.route('/nodes/sync', methods=['GET'])
def sync():
    updated = blockchain.update_blockchain()
    if updated:
        response = {
            'message':
            'The blockchain has been updated to the latest',
            'blockchain': blockchain.chain
            }
    else:
        response = {
            'message': 'Our blockchain is the latest',
            'blockchain': blockchain.chain}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))


#블록에 트랜잭션을 추가하는 명령어: 
# curl -X POST -H "Content-Type: application/json" -d "{\"sender\": \"04d0988bfa799f7d7ef9ab3de97ef481\", \"recipient\": \"cd0f75d2367ad456607647edde665d6f\",\"amount\": 5}" "http://localhost:5000/transactions/new"

# curl -H "Content-type: application/json" -d '{"nodes" :["http://127.0.0.1:5000"]}' -X POST http://localhost:5001/nodes/add_nodes
# 파일 위치: C:\Users\thdms\blockchain