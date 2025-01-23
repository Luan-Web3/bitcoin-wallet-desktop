import flet as ft
from tabs.wallet import create_wallet_view
from tabs.send import create_send_view
from tabs.mempool import create_mempool_view
from wallet_manager import WalletManager
import os
from dotenv import load_dotenv

def main(page: ft.Page):

    load_dotenv()

    rpc_wallet = os.getenv("RPC_WALLET")

    wallet_manager = WalletManager(rpc_wallet)

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Wallet",
                content=create_wallet_view(wallet_manager, page),
            ),
            ft.Tab(
                text="Send",
                content=create_send_view(wallet_manager),
            ),
            ft.Tab(
                text="Mempool",
                content=create_mempool_view(wallet_manager),
            ),
        ],
        expand=1,
    )

    page.add(t)

ft.app(main)