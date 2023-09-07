import os
from web3 import Web3, HTTPProvider

BLOCKCHAIN_URL = os.environ["BLOCKCHAIN_URL"]
web3 = Web3(HTTPProvider(f"http://{BLOCKCHAIN_URL}:8545"))
def read_file ( path ):
    with open ( path, "r" ) as file:
        return file.read ( )

bytecode = read_file ( "Order.bin" )
abi      = read_file ( "Order.abi" )


ownerAccountBC = web3.eth.accounts[0]