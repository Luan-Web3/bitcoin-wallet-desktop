from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os
from dotenv import load_dotenv

class WalletManager:
    def __init__(self, rpc_wallet: str):
        try:
            load_dotenv()
            
            rpc_user = os.getenv("RPC_USER")
            rpc_password = os.getenv("RPC_PASSWORD")
            rpc_host = os.getenv("RPC_HOST")
            rpc_port = os.getenv("RPC_PORT")
            rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{rpc_wallet}"
            self.__rpc_connection = AuthServiceProxy(rpc_url)
            self.__selected_address = None

            blockchain_info = self.__rpc_connection.getblockchaininfo()
            print(f"Connected to Bitcoin Core")
            print(f"Blockchain info: {blockchain_info}")
            print("--------")

        except JSONRPCException as e:
            print(f"Error connecting to RPC: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_balance_for_address(self, address: str) -> float:
        try:
            self.__selected_address = address
            utxos = self.__get_utxos()
            total_balance = sum(float(utxo["amount"]) for utxo in utxos)
            return total_balance

        except JSONRPCException as e:
            print(f"Error getting balance for address {address}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def create_new_address(self) -> str:
        try:
            return self.__rpc_connection.getnewaddress()

        except JSONRPCException as e:
            print(f"Error creating new address: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_addresses_by_label(self) -> dict:
        try:
            return self.__rpc_connection.getaddressesbylabel("")
        except JSONRPCException as e:
            print(f"Error getting addresses: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_raw_mempool(self) -> list:
        try:
            return self.__rpc_connection.getrawmempool(False)
        except JSONRPCException as e:
            print(f"Error getting mempool: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def generate_to_address(self) -> list:
        try:
            mining_address = os.getenv("MINING_ADDRESS")
            blocks_to_generate = int(os.getenv("BLOCKS_TO_GENERATE"))
            return self.__rpc_connection.generatetoaddress(blocks_to_generate, mining_address)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_transaction_by_txid(self, txid: str) -> dict:
        try:
            return self.__rpc_connection.gettransaction(txid)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def send_to_address(self, recipient_address: str, amount: float, tax: float) -> str:
        try:
            utxos = self.__get_utxos()
            inputs, total_utxos = self.__select_utxos(utxos, amount, tax)
            outputs = self.__create_outputs(recipient_address, amount, total_utxos, tax)
            raw_tx = self.__create_raw_transaction(inputs, outputs)
            signed_tx = self.__sign_transaction(raw_tx)
            txid = self.__broadcast_transaction(signed_tx)
            return txid
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def __get_utxos(self) -> list:
        utxos = self.__rpc_connection.listunspent(0, 9999999, [self.__selected_address])
        return utxos

    def __select_utxos(self, utxos: list, amount: float, tax: float) -> tuple:
        total_utxos = 0.0
        inputs = []
        for utxo in utxos:
            inputs.append({"txid": utxo["txid"], "vout": utxo["vout"]})
            total_utxos += float(utxo["amount"])
            if total_utxos >= (amount + tax):
                break

        if total_utxos < (amount + tax):
            raise ValueError(f"Insufficient balance. Total available: {total_utxos} BTC.")

        return inputs, total_utxos

    def __create_outputs(self, recipient_address: str, amount: float, total_utxos: float, tax: float) -> dict:
        change = total_utxos - (amount + tax)
        outputs = {recipient_address: amount}
        if change > 0:
            outputs[self.__selected_address] = round(change, 8)
        return outputs

    def __create_raw_transaction(self, inputs: list, outputs: dict) -> str:
        return self.__rpc_connection.createrawtransaction(inputs, outputs)

    def __sign_transaction(self, raw_tx: str) -> dict:
        signed_tx = self.__rpc_connection.signrawtransactionwithwallet(raw_tx)
        if not signed_tx.get("complete", False):
            raise ValueError("Error signing transaction.")
        return signed_tx

    def __broadcast_transaction(self, signed_tx: dict) -> str:
        return self.__rpc_connection.sendrawtransaction(signed_tx["hex"])
