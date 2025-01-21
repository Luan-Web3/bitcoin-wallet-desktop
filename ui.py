from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel, QPushButton, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from wallet_manager_mock import get_addresses, get_balance, send_crypto, create_new_address
from wallet_manager import WalletManager

class CryptoWalletUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Wallet")
        self.setGeometry(100, 100, 800, 600)

        # client = WalletManager()
        # balance = client.get_balance_for_address("bcrt1qxa9uhfyw885z7ce7z3hxj9fn62cq45e73fkj7q")
        # new_address = client.create_new_address()

        # Main 
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # WALLET
        self.wallet_tab = QWidget()
        self.wallet_layout = QVBoxLayout()
        self.wallet_tab.setLayout(self.wallet_layout)
        self.tabs.addTab(self.wallet_tab, "Wallet")

        self.address_select = QComboBox()
        # Endereços
        addresses = get_addresses()
        self.address_select.addItems(addresses)
        default_address = addresses[0] if addresses else ""

        self.wallet_layout.addWidget(QLabel("Select Wallet Address:"))
        self.wallet_layout.addWidget(self.address_select)

        self.new_address_button = QPushButton("Generate New Address")
        self.new_address_button.clicked.connect(self.generate_new_address)
        self.wallet_layout.addWidget(self.new_address_button)

        # Saldo
        self.balance_label = QLabel(f"Balance: {get_balance(default_address)} BTC")
        self.wallet_layout.addWidget(self.balance_label)
        self.address_select.currentTextChanged.connect(self.update_balance)

        # TRANSAÇÃO 
        self.transaction_tab = QWidget()
        self.transaction_layout = QVBoxLayout()
        self.transaction_tab.setLayout(self.transaction_layout)
        self.tabs.addTab(self.transaction_tab, "Transactions")

        self.transaction_label = QLabel("Transaction details will appear here.")
        self.transaction_layout.addWidget(self.transaction_label)

        # ENVIAR
        self.send_tab = QWidget()
        self.send_layout = QVBoxLayout()
        self.send_tab.setLayout(self.send_layout)
        self.tabs.addTab(self.send_tab, "Send")

        self.recipient_label = QLabel("Recipient Address:")
        self.recipient_input = QLineEdit()
        self.amount_label = QLabel("Amount (BTC):")
        self.amount_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send)

        self.send_layout.addWidget(self.recipient_label)
        self.send_layout.addWidget(self.recipient_input)
        self.send_layout.addWidget(self.amount_label)
        self.send_layout.addWidget(self.amount_input)
        self.send_layout.addWidget(self.send_button)

        # ESTILO
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLabel {
                font-size: 16px;
                color: #ffffff;
                padding: 8px;
            }
            QPushButton {
                background-color: #5a5a5a;
                color: #ffffff;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QLineEdit, QComboBox {
                background-color: #333333;
                color: gray;
                border: 1px solid #5a5a5a;
                padding: 6px;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #5a5a5a;
                border-left-style: solid;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png); /* Replace with your own arrow image */
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff; /* Light background for the dropdown */
                color: #000000; /* Black text for the dropdown */
                selection-background-color: #5a5a5a;
                border: 1px solid #5a5a5a;
            }
            QTabWidget::pane {
                border: 1px solid #5a5a5a;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #ffffff;
                padding: 12px;
            }
            QTabBar::tab:selected {
                background: #5a5a5a;
            }
        """)

    def generate_new_address(self):
        new_address = create_new_address()
        self.address_select.addItem(new_address)
        self.address_select.setCurrentText(new_address)
        self.update_balance()

    def handle_send(self):
        sender_address = self.address_select.currentText()
        recipient_address = self.recipient_input.text()
        amount = self.amount_input.text()

        if send_crypto(sender_address, amount):
            if recipient_address in get_addresses():
                wallet_data[recipient_address] += float(amount)
            else:
                wallet_data[recipient_address] = float(amount)

            self.transaction_label.setText(f"Sent {amount} BTC from {sender_address} to {recipient_address}.")
            self.update_balance()  
        else:
            self.transaction_label.setText("Transaction failed.")

    def update_balance(self):
        selected_address = self.address_select.currentText()
        balance = get_balance(selected_address)
        self.balance_label.setText(f"Balance: {balance} BTC")