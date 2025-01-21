from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os
from dotenv import load_dotenv

class WalletManager:
    def __init__(self):
        try:
            load_dotenv()
            
            rpc_user = os.getenv("RPC_USER")
            rpc_password = os.getenv("RPC_PASSWORD")
            rpc_host = os.getenv("RPC_HOST")
            rpc_port = os.getenv("RPC_PORT")
            rpc_wallet = os.getenv("RPC_WALLET")
            rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{rpc_wallet}"
            self.rpc_connection = AuthServiceProxy(rpc_url)

            blockchain_info = self.rpc_connection.getblockchaininfo()
            print("Conexão bem-sucedida ao Bitcoin Core")
            print("Informações do blockchain:", blockchain_info)

        except JSONRPCException as e:
            print(f"Erro na conexão RPC: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise

    def get_balance_for_address(self, address: str) -> float:
        try:
            return self.rpc_connection.getreceivedbyaddress(address)

        except JSONRPCException as e:
            print(f"Erro ao obter o saldo do endereço {address}: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise

    def create_new_address(self) -> str:
        try:
            return self.rpc_connection.getnewaddress()

        except JSONRPCException as e:
            print(f"Erro ao criar novo endereço: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise
