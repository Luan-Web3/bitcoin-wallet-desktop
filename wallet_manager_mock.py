def get_address():
    """Retorna um endereço de exemplo."""
    return "1ExampleAddress123456789"


def get_balance():
    """Retorna um saldo de exemplo."""
    return 1.23456789


def send_crypto(address, amount):
    """Simula o envio de criptomoedas."""
    print(f"Enviando {amount} BTC para {address}...")
    return True  


def receive_crypto():
    """Simula o recebimento de criptomoedas."""
    print("Recebendo criptomoedas...")
    return "1NewAddressGenerated" 