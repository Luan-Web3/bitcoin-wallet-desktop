from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os
from dotenv import load_dotenv
from decimal import Decimal

class WalletManager:
    def __init__(self, rpc_wallet: str):
        try:
            load_dotenv()
            
            rpc_user = os.getenv("RPC_USER")
            rpc_password = os.getenv("RPC_PASSWORD")
            rpc_host = os.getenv("RPC_HOST")
            rpc_port = os.getenv("RPC_PORT")
            # rpc_wallet = os.getenv("RPC_WALLET")
            rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{rpc_wallet}"
            self.__rpc_connection = AuthServiceProxy(rpc_url)
            self.__selected_address = None

            blockchain_info = self.__rpc_connection.getblockchaininfo()
            print("Conexão bem-sucedida ao Bitcoin Core")
            print("Informações do blockchain:", blockchain_info)
            print("--------")

        except JSONRPCException as e:
            print(f"Erro na conexão RPC: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise

    def get_balance_for_address(self, address: str) -> float:
        try:
            self.__selected_address = address
            return self.__rpc_connection.getreceivedbyaddress(address)

        except JSONRPCException as e:
            print(f"Erro ao obter o saldo do endereço {address}: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise

    def create_new_address(self) -> str:
        try:
            return self.__rpc_connection.getnewaddress()

        except JSONRPCException as e:
            print(f"Erro ao criar novo endereço: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise

    def get_addresses_by_label(self) -> dict:
        try:
            return self.__rpc_connection.getaddressesbylabel("")
        except JSONRPCException as e:
            print(f"Erro ao obter endereços: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise

    def get_raw_mempool(self) -> list:
        try:
            return self.__rpc_connection.getrawmempool(False)
        except JSONRPCException as e:
            print(f"Erro ao obter o mempool: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise

    def generate_to_address(self, mining_address: str) -> list:
        try:
            return self.__rpc_connection.generatetoaddress(1, mining_address)
        except Exception as e:
            print(f"Erro ao minerar bloco: {e}")
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
            print(f"Erro na transação: {e}")
            return None

    def __get_utxos(self) -> list:
        utxos = self.__rpc_connection.listunspent(0, 9999999, [self.__selected_address])
        if not utxos:
            raise ValueError(f"Não há UTXOs disponíveis para o endereço: {self.__selected_address}")
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
            raise ValueError(f"Saldo insuficiente. Total disponível: {total_utxos} BTC.")

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
            raise ValueError("Erro ao assinar a transação.")
        return signed_tx

    def __broadcast_transaction(self, signed_tx: dict) -> str:
        return self.__rpc_connection.sendrawtransaction(signed_tx["hex"])
