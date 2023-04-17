<<<<<<< HEAD
#First we wil create the chain class.
#This class will contain all the functions that will be used to create the blockchain. 
#The first function we will create is the init function. This function will be used to initialize the blockchain.

#We should use nonce instead of proof but we will use proof for simplicity

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class blockchain:
    def __init__(self):
        self.chain = []                                     #This will contain all the blocks in the chain
        self.create_block(proof = 1 , previous_hash = '0')  #This is the genesis block #proof = 1, 1 is arbitrary we can use any number but usually 1 is used. 
                                                            #same with previous_hash

    
    def create_block(self, proof, previous_hash):           #A block contains the proof of work, the previous hash, index of the block, data, timestamp
        block = {'index': len(self.chain) + 1,              #This will be the index of the block, we just took the length of the chain and added 1
                 'timestamp': str(datetime.datetime.now()), #This will be the time the block was created, used str so that no problems occur in json format 
                 'proof': proof,                            #This will be the proof of work, which shows that the block was mined work was done
                 'previous_hash': previous_hash}            #This will be the hash of the previous block, to keep the chain intact
        self.chain.append(block)                            #Our function created the block and now we will append it to the chain
        return block                                        #We will return the block so we can use it later
    
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
    

#We have built architecture of the blockchain, now we will create a web app to interact with the blockchain

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)                                               #We will create a web app using flask, check flask documentation for more info

# Creating a Blockchain

Blockchain = blockchain()                                           #We will create a blockchain object

# Mining a new block
@app.route('/mine_block', methods = ['GET'])                         #We will create a route to mine a new block, we will use the GET method 
def mine_block():                                           
    #we need proof of previous block to find the proof of work for the current block
    previous_block = Blockchain.get_previous_block()                 #We will take the previous block and store it in previous_block
    previous_proof = previous_block['proof']                         #We will take the proof of the previous block and store it in previous_proof
    #now we can apply the proof of block function to find the proof of work for the current block
    proof = Blockchain.proof_of_work(previous_proof)
    #we need to add the previous hash to the current block
    previous_hash = Blockchain.hash(previous_block)                  #We will take the hash of the previous block and store it in previous_hash
    #now we can create the block
    block = Blockchain.create_block(proof, previous_hash)            #We will create the block using the create_block function
    response = {'message': 'Congratulations, you just mined a block!', #We will create a response to show the user that the block was mined
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']} 
    return jsonify(response), 200                                    #We will return the response in the form of a json file, 200 is the status code for success


# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])                          #We will create a route to get the full blockchain, we will use the GET method
def get_chain():
    response = {'chain': Blockchain.chain,                           #We will create a response to show the user the full blockchain
                'length': len(Blockchain.chain)}
    return jsonify(response), 200                                    #We will return the response in the form of a json file, 200 is the status code for success


# Last part is running the app
app.run(host = '0.0.0.0', port = 5000)                               #We will run the app on port 5000, we will use

=======
#First we wil create the chain class.
#This class will contain all the functions that will be used to create the blockchain. 
#The first function we will create is the init function. This function will be used to initialize the blockchain.

#We should use nonce instead of proof but we will use proof for simplicity

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class blockchain:
    def __init__(self):
        self.chain = []                                     #This will contain all the blocks in the chain
        self.create_block(proof = 1 , previous_hash = '0')  #This is the genesis block #proof = 1, 1 is arbitrary we can use any number but usually 1 is used. 
                                                            #same with previous_hash

    
    def create_block(self, proof, previous_hash):           #A block contains the proof of work, the previous hash, index of the block, data, timestamp
        block = {'index': len(self.chain) + 1,              #This will be the index of the block, we just took the length of the chain and added 1
                 'timestamp': str(datetime.datetime.now()), #This will be the time the block was created, used str so that no problems occur in json format 
                 'proof': proof,                            #This will be the proof of work, which shows that the block was mined work was done
                 'previous_hash': previous_hash}            #This will be the hash of the previous block, to keep the chain intact
        self.chain.append(block)                            #Our function created the block and now we will append it to the chain
        return block                                        #We will return the block so we can use it later
    
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
    

#We have built architecture of the blockchain, now we will create a web app to interact with the blockchain

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)                                               #We will create a web app using flask, check flask documentation for more info

# Creating a Blockchain

Blockchain = blockchain()                                           #We will create a blockchain object

# Mining a new block
@app.route('/mine_block', methods = ['GET'])                         #We will create a route to mine a new block, we will use the GET method 
def mine_block():                                           
    #we need proof of previous block to find the proof of work for the current block
    previous_block = Blockchain.get_previous_block()                 #We will take the previous block and store it in previous_block
    previous_proof = previous_block['proof']                         #We will take the proof of the previous block and store it in previous_proof
    #now we can apply the proof of block function to find the proof of work for the current block
    proof = Blockchain.proof_of_work(previous_proof)
    #we need to add the previous hash to the current block
    previous_hash = Blockchain.hash(previous_block)                  #We will take the hash of the previous block and store it in previous_hash
    #now we can create the block
    block = Blockchain.create_block(proof, previous_hash)            #We will create the block using the create_block function
    response = {'message': 'Congratulations, you just mined a block!', #We will create a response to show the user that the block was mined
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']} 
    return jsonify(response), 200                                    #We will return the response in the form of a json file, 200 is the status code for success


# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])                          #We will create a route to get the full blockchain, we will use the GET method
def get_chain():
    response = {'chain': Blockchain.chain,                           #We will create a response to show the user the full blockchain
                'length': len(Blockchain.chain)}
    return jsonify(response), 200                                    #We will return the response in the form of a json file, 200 is the status code for success


# Last part is running the app
app.run(host = '0.0.0.0', port = 5000)                               #We will run the app on port 5000, we will use

>>>>>>> 517dc3c8e9f7ed8b7298153e90047033ab15ee34
#We will use postman to interact with the blockchain