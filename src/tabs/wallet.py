import flet as ft
from wallet_manager import WalletManager

def create_wallet_view(wallet_manager: WalletManager, page: ft.Page):
    items = wallet_manager.get_addresses_by_label()

    item_selected = next(iter(items.keys()))
    balance = wallet_manager.get_balance_for_address(item_selected)
    text_balance = ft.Text(
        f"Balance: {float(balance)} BTC",
        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM
    )

    def create_list_tiles(items):
        return [ft.dropdown.Option(item) for item in items]
    
    def generate_new_address(e):
        new_address = wallet_manager.create_new_address()
        dropdown.options.append(ft.dropdown.Option(new_address))
        dropdown.value = new_address
        dropdown.update()
        get_balance_for_address(new_address)

    def get_balance_for_address(address):
        balance = wallet_manager.get_balance_for_address(address)
        text_balance.value = f"Balance: {float(balance)} BTC"
        text_balance.update()

    def change_address(e):
        get_balance_for_address(e.data)

    def copy_address(e):
        page.set_clipboard(dropdown.value)
        
    dropdown = ft.Dropdown(
        value=item_selected,
        label="Address",
        hint_text="Choose your address?",
        width=540,
        options=create_list_tiles(items),
        on_change=change_address
    )

    return ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[dropdown]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[text_balance]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.FilledButton(
                        "Copy Address",
                        height=50,
                        width=200,
                        on_click=copy_address,
                    ),
                    ft.FilledButton(
                        "Generate New Wallet",
                        height=50,
                        width=200,
                        on_click=generate_new_address,
                    ),
                ]
            )
            
        ]
    )