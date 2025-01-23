import flet as ft
from wallet_manager import WalletManager

def create_send_view(wallet_manager: WalletManager):
    def send_do_address(e):
        if not recipent_address.value or not amount.value:
            print("Both recipient address and amount must be filled.")
            return
        
        wallet_manager.send_to_address(recipent_address.value, float(amount.value), 0.0005)
        
        recipent_address.value = None
        recipent_address.update()

        amount.value = None
        amount.update()

    recipent_address = ft.TextField(label="Recipient Address", width=540)
    amount = ft.TextField(label="Amount", width=540)

    return ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    recipent_address
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    amount
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.FilledButton(
                        "Send",
                        height=50,
                        width=540,
                        on_click=send_do_address
                    ),
                ]
            ),
        ]
    )