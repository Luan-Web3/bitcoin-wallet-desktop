import flet as ft
from wallet_manager import WalletManager

def create_mempool_view(wallet_manager: WalletManager):
    txids = [
    ]

    txid_list = ft.ListView(
        controls=[ft.Text(txid, text_align=ft.TextAlign.CENTER) for txid in txids],
        expand=True
    )
    def get_mempool_entry(e):
        new_txids = wallet_manager.get_raw_mempool()

        if len(new_txids) == 0:
            txid_list.controls = [ft.Text("No transaction yet", text_align=ft.TextAlign.CENTER)]
        else:
            txid_list.controls = [
                ft.Text(txid, text_align=ft.TextAlign.CENTER) for txid in new_txids
            ]

        txid_list.update()

    def generate_block(e):
        wallet_manager.generate_to_address()


    return ft.Column(
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[txid_list],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.FilledButton(
                        "Get Mempool Entry",
                        height=50,
                        width=540,
                        on_click=get_mempool_entry
                    ),
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.FilledButton(
                        "Generate Block",
                        height=50,
                        width=540,
                        on_click=generate_block
                    ),
                ]
            ),
        ]
    )