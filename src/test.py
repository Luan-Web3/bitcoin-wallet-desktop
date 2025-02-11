from wallet_manager import WalletManager
import os
from dotenv import load_dotenv

load_dotenv()

rpc_wallet = os.getenv("RPC_WALLET")

wallet_manager = WalletManager(rpc_wallet)

def get_mempool_entry():
    new_txids = wallet_manager.get_raw_mempool()

    print(new_txids)

def generate_block():
    wallet_manager.generate_to_address()

get_mempool_entry()

# generate_block()