<<<<<<< HEAD
#We copied and pasted the code from the coin.py file and changed the port number to 5002

#If we add transactions to our blockchain that we implement would get a cryptocurrency or a coin.
#We will copy the chain.py code and edit it to add transactions and a concensus method.

import datetime
import hashlib
import json
from flask import Flask, jsonify
from flask import request
from urllib.parse import urlparse
from uuid import uuid4

# Part 1 - Building a Blockchain

class Blockchain:
    def __init__(self):
        self.chain = []                                     #This will contain all the blocks in the chain
        self.transactions = []                              #This will contain all the transactions to be added to the block before mining, it will become empty after mining    
        self.nodes = set()                                  #This will contain all the nodes in the network, used for concensus and decentralization
                                                            #We will use set because it will not contain any duplicate nodes,it is faster than list and they don't need to be ordered
        self.create_block(proof = 1 , previous_hash = '0')  #This is the genesis block #proof = 1, 1 is arbitrary we can use any number but usually 1 is used. 
                                                            #same with previous_hash

    
    def create_block(self, proof, previous_hash):           #A block contains the proof of work, the previous hash, index of the block, data, timestamp
        block = {'index': len(self.chain) + 1,              #This will be the index of the block, we just took the length of the chain and added 1
                 'timestamp': str(datetime.datetime.now()), #This will be the time the block was created, used str so that no problems occur in json format 
                 'proof': proof,                            #This will be the proof of work, which shows that the block was mined work was done
                 'previous_hash': previous_hash,            #This will be the hash of the previous block, to keep the chain intact
                 'transactions': self.transactions}         #This will be the transactions that will be added to the block before mining 
        self.transactions = []                              #we will make the transactions empty after adding them to the block
        self.chain.append(block)                            #Our function created the block and now we will append it to the chain
        return block                                     #We will return the block so we can use it later                                    #We will return the block so we can use it later
    
    def get_previous_block(self):
        return self.chain[-1]                               #This will return the last block in the chain
    
    def proof_of_work(self, previous_proof):                #This function will be used to find the proof of work that is expected by the create block function
        new_proof = 1                                       #We will start with 1 till we get our desired proof of work, incremented slowly
        check_proof = False                                 #It will check if our proof is desired or not, we incialize it to false because we have not found the proof yet
        while check_proof is False:                         #We will use while loop to itereate over multiple proof til we find the desired proof
            #we will use SHA256 hashing algorithm to find the proof of work. With 4 leading zeros. More the number of zeros more the difficulty.
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            #(new_proof**2 - previous_proof**2) is the equation that will be used to find the proof of work, we can make it even more complex
            #.encode()).hexdigest() it is used for encoding the string into a hexadecimal format. Basically formating purposes
            if hash_operation[:4] == '0000':                #We will check if the first 4 characters of the hash are 0000
                check_proof = True                          #If they are then we will set the check_proof to true and break the loop
            else:
                new_proof += 1                              #If they are not then we will increment the new_proof by 1 and check again
        return new_proof                                    #We will return the new_proof that we have found using the loop and the equation
    
    #We will check if each block in the chain has previous hash same as the hash of the previous block

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()  #We are using jason.dumps because we put our block dictionary into a json format, 
                                                                      #that's how we will make our block a string. sort_keys = True is used to sort the keys in the dictionary
        return hashlib.sha256(encoded_block).hexdigest()              #We will encoded_block in the form of a hexadecimal format
    
    def is_chain_valid(self, chain):         
        previous_block = chain[0]                                   #We will take the first block in the chain and store it in previous_block
        block_index = 1                                             #Each block has an index and they start with 1                 
        while block_index < len(chain):
            #we will check two things 1. if the previous hash of the current block is equal to the hash of the previous block
            #2. if the proof of work of the current block is valid i.e. if the first 4 characters of the hash are 0000
            block = chain[block_index]                              #We will take the current block and store it in block
            if block['previous_hash'] != self.hash(previous_block): #We will check if the previous hash of the current block is equal to the hash of the previous block
                return False                                        #If they are not equal then we will return false
            previous_proof = previous_block['proof']                #We will take the proof of the previous block and store it in previous_proof
            proof = block['proof']                                  #We will take the proof of the current block and store it in proof
            #now we will use our hash function to check if the proof of work of the current block is valid
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':                        #We will check if the first 4 characters of the hash are 0000
                return False                                        #If they are not equal then we will return false
            previous_block = block                                  #We will update the previous_block to the current block to keep going foreward since we initialised it to [0]
            block_index += 1                                        #We will increment the block_index by 1 to go to the next block
        return True                                                 #If all the blocks are valid then we will return true
    
    #Adding a transaction to our transactions list
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 'receiver': receiver, 'amount':amount})       #In a typical transaction we have a sender, receiver and the amount
        previous_block = self.get_previous_block()                                                   #We will take the previous block and store it in previous_block
        return previous_block['index'] + 1                                                           #It will return the index of the next block that will be mined
    
    #Adding a function to add a node to our network for the concensus
    def add_node(self, address):
        parsed_url = urlparse(address)                                                          #It will divide the url into different parts like scheme, netloc, path, params, query, fragment
        self.nodes.add(parsed_url.netloc)                                                       #We will add the netloc part of the url to our nodes set, 127.0.0.1:5000

    #We will create a function to replace the chain with the longest chain in the network
    def replace_chain(self):
        network = self.nodes                                                               #All the nodes in the network will be stored in var network
        longest_chain = None                                                               #Longest chain is initially set to None because we have not found the longest chain yet
        max_length = len(self.chain)                                                       #We will take the length of our current chain and store it in max_length
        for node in network:                                                               #We will iterate over all the nodes in the network
            response = request.get(f'http://{node}/get_chain')                            #We will send a get request to the node to get the chain we have stored (parsed_url.netloc)
            if response.status_code == 200:                                                #If the status code is 200 then we will get the chain
                length = response.json()['length']                                         #We have stored the chain in json format
                chain = response.json()['chain'] 
                if length > max_length and self.is_chain_valid(chain):                     #We will check if the length of the chain is greater than the max_length and if the chain is valid
                    max_length = length                                                    #If the chain is valid then we will update the max_length to the length of the chain
                    longest_chain = chain                                                  #We will update the longest_chain to the chain
        if longest_chain:                                                                  
            self.chain = longest_chain                                                     #If the longest_chain is not None then we will update our chain to the longest_chain
            return True
        return False
    


#We have built architecture of the blockchain, now we will create a web app to interact with the blockchain

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)                                               #We will create a web app using flask, check flask documentation for more info
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# We will create an address for the node on Port 5001 using uuid4 and replace the - with nothing, uuid4() it provides a unique address for anything for our case the node
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain

blockchain = Blockchain()                                           #We will create a blockchain object


#We will edit the mine_block to add the transactions to the block
# Mining a new block
@app.route('/mine_block', methods = ['GET'])                         #We will create a route to mine a new block, we will use the GET method 
def mine_block():                                           
    #we need proof of previous block to find the proof of work for the current block
    previous_block = blockchain.get_previous_block()                 #We will take the previous block and store it in previous_block
    previous_proof = previous_block['proof']                         #We will take the proof of the previous block and store it in previous_proof
    #now we can apply the proof of block function to find the proof of work for the current block
    proof = blockchain.proof_of_work(previous_proof)
    #we need to add the previous hash to the current block
    previous_hash = blockchain.hash(previous_block)                  #We will take the hash of the previous block and store it in previous_hash

    #We will add the transaction function. sender, receiver and the amount to the block in the form of a dictionary
    blockchain.add_transaction(sender = node_address, receiver = 'Jagjit', amount = 5)

    #now we can create the block
    block = blockchain.create_block(proof, previous_hash)            #We will create the block using the create_block function
    response = {'message': 'Congratulations, you just mined a block!', #We will create a response to show the user that the block was mined
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']} 
    return jsonify(response), 200                                    #We will return the response in the form of a json file, 200 is the status code for success

# We now want to add the transactions to the block using the post method
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()                                       #we will get the json file from the url
    transaction_keys = ['sender', 'receiver', 'amount']              #We will create a list of the keys to check if all the keys are present in the json file
    if not all (key in json for key in transaction_keys):            #We will check if all the keys are present in the json file
        return 'Some elements of the transaction are missing', 400   #If not then we will return a message and 400 is the status code for bad request
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount']) #We will get the index by calling our function in our blockchain object.
                                                                                         #The funct of transaction accepts values and not keys so we have to do the same.
    response = {'message': f'This transaction will be added to Block {index}'} #We will create a response to show the user that the transaction was added to the block
    return jsonify(response), 201                                    #We will return the response in the form of a json file, 201 is the status code for created

#We will now connect the different nodes in the network
@app.route('/connect_node', methods = ['POST'])                     #We will create a route to connect the nodes, we will use the POST method
def connect_node():
    json = request.get_json()                                      #we will get the json file from the url
    nodes = json.get('nodes')                                       #We will get the nodes from the json file
    if nodes is None:                                               #We want to check if the nodes have something in them
        return "No node", 400                                       #If not then we will return a message and 400 is the status code for bad request
    for node in nodes:                                              #We will iterate over all the nodes and add them using our class function
        blockchain.add_node(node)                                   #We will add the node to the blockchain object
    response = {'message': 'All the nodes are now connected. The coin now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}              #We will create a response to show the user that the nodes are connected
    return jsonify(response), 201                                    #We will return the response in the form of a json file, 201 is the status code for created

#We will now replace the chain with the longest chain if needed for a particular node
@app.route('/replace_chain', methods = ['GET'])                      #We will create a route to replace the chain, we will use the GET method
def replace_chain():
    is_chain_replaces = blockchain.replace_chain()                   #We will run our class function and it will give us a boolean value
    if is_chain_replaces:                                            #Using the boolean value we will check if the chain was replaced
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}                   #We will create a response to show the user that the chain was replaced'
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200                                     #We will return the response in the form of a json file, 200 is the status code for success

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])                          #We will create a route to get the full blockchain, we will use the GET method
def get_chain():
    response = {'chain': blockchain.chain,                           #We will create a response to show the user the full blockchain
                'length': len(blockchain.chain)}
    return jsonify(response), 200                                    #We will return the response in the form of a json file, 200 is the status code for success


# Last part is running the app
app.run(host = '0.0.0.0', port = 5002)                               #We will run the app on port 5000, we will use

=======
#We copied and pasted the code from the coin.py file and changed the port number to 5002

#If we add transactions to our blockchain that we implement would get a cryptocurrency or a coin.
#We will copy the chain.py code and edit it to add transactions and a concensus method.

import datetime
import hashlib
import json
from flask import Flask, jsonify
from flask import request
from urllib.parse import urlparse
from uuid import uuid4

# Part 1 - Building a Blockchain

class Blockchain:
    def __init__(self):
        self.chain = []                                     #This will contain all the blocks in the chain
        self.transactions = []                              #This will contain all the transactions to be added to the block before mining, it will become empty after mining    
        self.nodes = set()                                  #This will contain all the nodes in the network, used for concensus and decentralization
                                                            #We will use set because it will not contain any duplicate nodes,it is faster than list and they don't need to be ordered
        self.create_block(proof = 1 , previous_hash = '0')  #This is the genesis block #proof = 1, 1 is arbitrary we can use any number but usually 1 is used. 
                                                            #same with previous_hash

    
    def create_block(self, proof, previous_hash):           #A block contains the proof of work, the previous hash, index of the block, data, timestamp
        block = {'index': len(self.chain) + 1,              #This will be the index of the block, we just took the length of the chain and added 1
                 'timestamp': str(datetime.datetime.now()), #This will be the time the block was created, used str so that no problems occur in json format 
                 'proof': proof,                            #This will be the proof of work, which shows that the block was mined work was done
                 'previous_hash': previous_hash,            #This will be the hash of the previous block, to keep the chain intact
                 'transactions': self.transactions}         #This will be the transactions that will be added to the block before mining 
        self.transactions = []                              #we will make the transactions empty after adding them to the block
        self.chain.append(block)                            #Our function created the block and now we will append it to the chain
        return block                                     #We will return the block so we can use it later                                    #We will return the block so we can use it later
    
    def get_previous_block(self):
        return self.chain[-1]                               #This will return the last block in the chain
    
    def proof_of_work(self, previous_proof):                #This function will be used to find the proof of work that is expected by the create block function
        new_proof = 1                                       #We will start with 1 till we get our desired proof of work, incremented slowly
        check_proof = False                                 #It will check if our proof is desired or not, we incialize it to false because we have not found the proof yet
        while check_proof is False:                         #We will use while loop to itereate over multiple proof til we find the desired proof
            #we will use SHA256 hashing algorithm to find the proof of work. With 4 leading zeros. More the number of zeros more the difficulty.
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            #(new_proof**2 - previous_proof**2) is the equation that will be used to find the proof of work, we can make it even more complex
            #.encode()).hexdigest() it is used for encoding the string into a hexadecimal format. Basically formating purposes
            if hash_operation[:4] == '0000':                #We will check if the first 4 characters of the hash are 0000
                check_proof = True                          #If they are then we will set the check_proof to true and break the loop
            else:
                new_proof += 1                              #If they are not then we will increment the new_proof by 1 and check again
        return new_proof                                    #We will return the new_proof that we have found using the loop and the equation
    
    #We will check if each block in the chain has previous hash same as the hash of the previous block

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()  #We are using jason.dumps because we put our block dictionary into a json format, 
                                                                      #that's how we will make our block a string. sort_keys = True is used to sort the keys in the dictionary
        return hashlib.sha256(encoded_block).hexdigest()              #We will encoded_block in the form of a hexadecimal format
    
    def is_chain_valid(self, chain):         
        previous_block = chain[0]                                   #We will take the first block in the chain and store it in previous_block
        block_index = 1                                             #Each block has an index and they start with 1                 
        while block_index < len(chain):
            #we will check two things 1. if the previous hash of the current block is equal to the hash of the previous block
            #2. if the proof of work of the current block is valid i.e. if the first 4 characters of the hash are 0000
            block = chain[block_index]                              #We will take the current block and store it in block
            if block['previous_hash'] != self.hash(previous_block): #We will check if the previous hash of the current block is equal to the hash of the previous block
                return False                                        #If they are not equal then we will return false
            previous_proof = previous_block['proof']                #We will take the proof of the previous block and store it in previous_proof
            proof = block['proof']                                  #We will take the proof of the current block and store it in proof
            #now we will use our hash function to check if the proof of work of the current block is valid
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':                        #We will check if the first 4 characters of the hash are 0000
                return False                                        #If they are not equal then we will return false
            previous_block = block                                  #We will update the previous_block to the current block to keep going foreward since we initialised it to [0]
            block_index += 1                                        #We will increment the block_index by 1 to go to the next block
        return True                                                 #If all the blocks are valid then we will return true
    
    #Adding a transaction to our transactions list
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 'receiver': receiver, 'amount':amount})       #In a typical transaction we have a sender, receiver and the amount
        previous_block = self.get_previous_block()                                                   #We will take the previous block and store it in previous_block
        return previous_block['index'] + 1                                                           #It will return the index of the next block that will be mined
    
    #Adding a function to add a node to our network for the concensus
    def add_node(self, address):
        parsed_url = urlparse(address)                                                          #It will divide the url into different parts like scheme, netloc, path, params, query, fragment
        self.nodes.add(parsed_url.netloc)                                                       #We will add the netloc part of the url to our nodes set, 127.0.0.1:5000

    #We will create a function to replace the chain with the longest chain in the network
    def replace_chain(self):
        network = self.nodes                                                               #All the nodes in the network will be stored in var network
        longest_chain = None                                                               #Longest chain is initially set to None because we have not found the longest chain yet
        max_length = len(self.chain)                                                       #We will take the length of our current chain and store it in max_length
        for node in network:                                                               #We will iterate over all the nodes in the network
            response = request.get(f'http://{node}/get_chain')                            #We will send a get request to the node to get the chain we have stored (parsed_url.netloc)
            if response.status_code == 200:                                                #If the status code is 200 then we will get the chain
                length = response.json()['length']                                         #We have stored the chain in json format
                chain = response.json()['chain'] 
                if length > max_length and self.is_chain_valid(chain):                     #We will check if the length of the chain is greater than the max_length and if the chain is valid
                    max_length = length                                                    #If the chain is valid then we will update the max_length to the length of the chain
                    longest_chain = chain                                                  #We will update the longest_chain to the chain
        if longest_chain:                                                                  
            self.chain = longest_chain                                                     #If the longest_chain is not None then we will update our chain to the longest_chain
            return True
        return False
    


#We have built architecture of the blockchain, now we will create a web app to interact with the blockchain

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)                                               #We will create a web app using flask, check flask documentation for more info
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# We will create an address for the node on Port 5001 using uuid4 and replace the - with nothing, uuid4() it provides a unique address for anything for our case the node
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain

blockchain = Blockchain()                                           #We will create a blockchain object


#We will edit the mine_block to add the transactions to the block
# Mining a new block
@app.route('/mine_block', methods = ['GET'])                         #We will create a route to mine a new block, we will use the GET method 
def mine_block():                                           
    #we need proof of previous block to find the proof of work for the current block
    previous_block = blockchain.get_previous_block()                 #We will take the previous block and store it in previous_block
    previous_proof = previous_block['proof']                         #We will take the proof of the previous block and store it in previous_proof
    #now we can apply the proof of block function to find the proof of work for the current block
    proof = blockchain.proof_of_work(previous_proof)
    #we need to add the previous hash to the current block
    previous_hash = blockchain.hash(previous_block)                  #We will take the hash of the previous block and store it in previous_hash

    #We will add the transaction function. sender, receiver and the amount to the block in the form of a dictionary
    blockchain.add_transaction(sender = node_address, receiver = 'Jagjit', amount = 5)

    #now we can create the block
    block = blockchain.create_block(proof, previous_hash)            #We will create the block using the create_block function
    response = {'message': 'Congratulations, you just mined a block!', #We will create a response to show the user that the block was mined
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']} 
    return jsonify(response), 200                                    #We will return the response in the form of a json file, 200 is the status code for success

# We now want to add the transactions to the block using the post method
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()                                       #we will get the json file from the url
    transaction_keys = ['sender', 'receiver', 'amount']              #We will create a list of the keys to check if all the keys are present in the json file
    if not all (key in json for key in transaction_keys):            #We will check if all the keys are present in the json file
        return 'Some elements of the transaction are missing', 400   #If not then we will return a message and 400 is the status code for bad request
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount']) #We will get the index by calling our function in our blockchain object.
                                                                                         #The funct of transaction accepts values and not keys so we have to do the same.
    response = {'message': f'This transaction will be added to Block {index}'} #We will create a response to show the user that the transaction was added to the block
    return jsonify(response), 201                                    #We will return the response in the form of a json file, 201 is the status code for created

#We will now connect the different nodes in the network
@app.route('/connect_node', methods = ['POST'])                     #We will create a route to connect the nodes, we will use the POST method
def connect_node():
    json = request.get_json()                                      #we will get the json file from the url
    nodes = json.get('nodes')                                       #We will get the nodes from the json file
    if nodes is None:                                               #We want to check if the nodes have something in them
        return "No node", 400                                       #If not then we will return a message and 400 is the status code for bad request
    for node in nodes:                                              #We will iterate over all the nodes and add them using our class function
        blockchain.add_node(node)                                   #We will add the node to the blockchain object
    response = {'message': 'All the nodes are now connected. The coin now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}              #We will create a response to show the user that the nodes are connected
    return jsonify(response), 201                                    #We will return the response in the form of a json file, 201 is the status code for created

#We will now replace the chain with the longest chain if needed for a particular node
@app.route('/replace_chain', methods = ['GET'])                      #We will create a route to replace the chain, we will use the GET method
def replace_chain():
    is_chain_replaces = blockchain.replace_chain()                   #We will run our class function and it will give us a boolean value
    if is_chain_replaces:                                            #Using the boolean value we will check if the chain was replaced
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}                   #We will create a response to show the user that the chain was replaced'
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200                                     #We will return the response in the form of a json file, 200 is the status code for success

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])                          #We will create a route to get the full blockchain, we will use the GET method
def get_chain():
    response = {'chain': blockchain.chain,                           #We will create a response to show the user the full blockchain
                'length': len(blockchain.chain)}
    return jsonify(response), 200                                    #We will return the response in the form of a json file, 200 is the status code for success


# Last part is running the app
app.run(host = '0.0.0.0', port = 5002)                               #We will run the app on port 5000, we will use

>>>>>>> 517dc3c8e9f7ed8b7298153e90047033ab15ee34
#We will use postman to interact with the blockchain