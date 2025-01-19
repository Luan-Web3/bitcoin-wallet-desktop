import random

wallet_data = {
    "1ExampleAddress123456789": 1.23456789,
    "1AnotherAddress987654321": 0.98765432,
    "1ThirdAddress654987321": 2.34567891
}

def get_addresses():
    """Retorna todos os endereços de exemplo."""
    return list(wallet_data.keys())

def get_balance(address):
    """Retorna o saldo associado a um endereço."""
    return wallet_data.get(address, 0.0)

def send_crypto(address, amount):
    """Simula o envio de criptomoedas."""
    amount = float(amount)
    if address in wallet_data and wallet_data[address] >= amount:
        wallet_data[address] -= amount
        print(f"Enviando {amount} BTC para {address}...")
        return True
    else:
        print("Saldo insuficiente ou endereço inválido.")
        return False

def create_new_address():
    """Simula a geração de um novo endereço."""
    new_address = f"1NewAddress{random.randint(100000, 999999)}"
    wallet_data[new_address] = 0.0
    print(f"Novo endereço gerado: {new_address}")
    return new_address