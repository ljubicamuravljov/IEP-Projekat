import os
from web3 import Web3, HTTPProvider


# def read_file ( path ):
#     with open ( path, "r" ) as file:
#         return file.read ( )

BLOCKCHAIN_URL = os.environ["BLOCKCHAIN_URL"]
web3 = Web3(HTTPProvider(f"http://{BLOCKCHAIN_URL}:8545"))

with open("Order.bin", "r") as file:
    bytecode= file.read()

with open("Order.abi", "r") as file:
    abi= file.read()


ownerAccountBC = web3.eth.accounts[0]