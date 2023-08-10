from web3 import Web3

api_key = ""
is_ws = False
"""
setting up the HTTP providers or WS
"""
# web3 providers can be obtained via Infura, Alchemy or any other node providers. 
# In this example I`m using alchemy, but it can be whatever provider you want
web3 = Web3(Web3.HTTPProvider(f'https://eth-goerli.g.alchemy.com/v2/{api_key}')) if is_ws == False else Web3(Web3.HTTPProvider(f'wss://eth-goerli.g.alchemy.com/v2/{api_key}'))

"""
convert private key to wallet instance
"""
private_key = ""
wallet = web3.eth.account.from_key(private_key)
"""
get account balance
"""
balance_in_ether = web3.eth.get_balance(wallet.address)
# here I`m specifying 'ether' because I`m getting basic token and it`s decimals are 18, so it`s 'ether'
# if you need to convert to any custom decimals (but for 18) use or custom function or specify other variants

# noether: 0
# wei: 1
# kwei: 1000
# Kwei: 1000
# babbage: 1000
# femtoether: 1000
# mwei: 1000000
# Mwei: 1000000
# lovelace: 1000000
# picoether: 1000000
# gwei: 1000000000
# Gwei: 1000000000
# shannon: 1000000000
# nanoether: 1000000000
# nano: 1000000000
# szabo: 1000000000000
# microether: 1000000000000
# micro: 1000000000000
# finney: 1000000000000000
# milliether: 1000000000000000
# milli: 1000000000000000
# ether: 1000000000000000000
# kether: 1000000000000000000000
# grand: 1000000000000000000000
# mether: 1000000000000000000000000
# gether: 1000000000000000000000000000
# tether: 1000000000000000000000000000000

balance_normal = web3.from_wei(balance_in_ether, "ether")

"""
to get custom token 
"""
import json
# specify address
any_contract_address = ""
# load abi from string
abi = json.load('')

# create contract instance
contract = web3.eth.contract(address=any_contract_address, abi=abi)
# get balance
custom_token_balance = contract.functions.balanceOf(wallet.address).call()
# get token decimals
token_decimals = contract.functions.decimals().call()

# using custom function for calculating custom decimals
# we can use this method when we don`t want to create enumerator with all the decimals values
from decimal import Decimal
def pow_function(decimals, number):
    pow_value = Decimal(10) ** decimals
    normal_value = Decimal(number)
    normal_value = normal_value / pow_value
    
    return normal_value

# here we have normal balance
normal_balance = pow_function(token_decimals, custom_token_balance)

"""
work with gas price
"""

# get current gas price in the network
gas_price = web3.eth.gas_price
# if we need to estimate gas limit of a transaction we need to create transaction and then call function
transaction = {
    'from': "",
    'to': "",
    'value': "",
    'nonce': web3.eth.get_transaction_count(wallet.address),
    'gas': 0,
    'gasPrice': gas_price + 10 # just in case we need to speed 
}

# usually transactions with basic tokens requires 21000 gas limit
# so if we call this function estimate = 21000
estimate = web3.eth.estimateGas(transaction)
# set gas limit to estimated
transaction['gas'] = estimate

basic_signed = web3.eth.account.signTransaction(transaction, private_key=wallet._private_key)

# let`s have a look on how this method should work with custom tokens:
tx = contract.functions.transfer('address', 1).buildTransaction({ # build transaction for sign it latter. Because this method won`t 
     'chainId': 1,
     'gas': 0,
     'gasPrice': gas_price + 10, # just in case we need to speed ,
     'nonce': web3.eth.get_transaction_count(wallet.address),
})

custom_signed = web3.eth.account.signTransaction(tx, private_key=wallet._private_key)

tx_hash = web3.eth.sendRawTransaction(custom_signed.rawTransaction) # or put basic_signed.rawTransaction

hash = web3.toHex(tx_hash) # to get tx and view it on scan
# or you can view raw transaction hash
web3.toHex(web3.sha3(custom_signed.rawTransaction))
# the result will be the same. Because once transaction is signed, tx_hash will be generated. But can`t be viewed until transaction is pending

"""
some useful functions
"""

# get latest block number
latest_block = web3.eth.block_number 

# convert 0.05 to token decimals. We need to_wei to blockchain readable varian
web3.to_wei(Decimal('0.01'), 'ether')

# to convert from token decimal view to a normal (human readable varian)
web3.from_wei(100000000, 'gwei')

# here we can get all the transaction data
tx_data = web3.eth.get_transaction(tx_hash)
# this function will only work after transaction is done
receipt = web3.eth.get_transaction_receipt(tx_hash)

""""
event listener
"""

# well, in python event listeners are implemented quite bad because I can`t find WS variant like in web3.js. So that would be really expensive for our RPC providers
# but after all lets have a lock on how to listen for events
import time
# do whatever you need with that
def handler(event):
    print(event)

def event_listener(filter, interval):
    while True:
        for event in filter.get_new_entries():
            handler(event)
        # sleep to not overwhelm RPC
        time.sleep(interval)

def main():
    # create event listener
    filter = contract.events.transfer.createFilter(fromBlock='latest')
    # if you need, implement asyncio in case you need to wait
    event_listener(filter, 1)

# for more info read - https://web3py.readthedocs.io/en/stable/filters.html
