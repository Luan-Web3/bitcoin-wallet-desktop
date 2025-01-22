from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QMessageBox,
)
from wallet_manager import WalletManager
from decimal import Decimal

# address("bcrt1qxa9uhfyw885z7ce7z3hxj9fn62cq45e73fkj7q")


class CryptoWalletUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Wallet")
        self.setGeometry(100, 100, 800, 600)

        self.wallet_manager = WalletManager()

        # Main
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        self.setCentralWidget(self.tabs)

        # WALLET
        self.wallet_tab = QWidget()
        self.wallet_tab.setObjectName("walletTab")
        self.wallet_layout = QVBoxLayout()
        self.wallet_layout.setObjectName("walletLayout")
        self.wallet_tab.setLayout(self.wallet_layout)
        self.tabs.addTab(self.wallet_tab, "Wallet")

        self.select_address_label = QLabel("Select Wallet Address:")
        self.select_address_label.setObjectName("selectAddressLabel")
        self.wallet_layout.addWidget(self.select_address_label)

        self.address_select = QComboBox()
        self.address_select.setObjectName("addressSelect")
        self.update_addresses()
        self.wallet_layout.addWidget(self.address_select)

        self.new_address_button = QPushButton("Generate New Address")
        self.new_address_button.setObjectName("newAddressButton")
        self.new_address_button.clicked.connect(self.generate_new_address)
        self.wallet_layout.addWidget(self.new_address_button)

        # Saldo
        self.balance_label = QLabel("")
        self.balance_label.setObjectName("balanceLabel")
        self.wallet_layout.addWidget(self.balance_label)
        self.address_select.currentTextChanged.connect(self.update_balance)
        self.update_balance()

        # ENVIAR
        self.send_tab = QWidget()
        self.send_tab.setObjectName("sendTab")
        self.send_layout = QVBoxLayout()
        self.send_layout.setObjectName("sendLayout")
        self.send_tab.setLayout(self.send_layout)
        self.tabs.addTab(self.send_tab, "Send")

        self.recipient_label = QLabel("Recipient Address:")
        self.recipient_label.setObjectName("recipientLabel")
        self.send_layout.addWidget(self.recipient_label)

        self.recipient_input = QLineEdit()
        self.recipient_input.setObjectName("recipientInput")
        self.send_layout.addWidget(self.recipient_input)

        self.amount_label = QLabel("Amount (BTC):")
        self.amount_label.setObjectName("amountLabel")
        self.send_layout.addWidget(self.amount_label)

        self.amount_input = QLineEdit()
        self.amount_input.setObjectName("amountInput")
        self.send_layout.addWidget(self.amount_input)

        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("sendButton")
        self.send_button.clicked.connect(self.handle_send)
        self.send_layout.addWidget(self.send_button)

        # ESTILO
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color:rgb(22, 22, 22);
                color: #ffffff;
            }

            #selectAddressLabel, #recipientLabel, #amountLabel {
                font-weight: bold;
                color: #ffffff;
                padding: 8px;
            }
            #selectAddressLabel{
                font-size: 28px;
            }
            #recipientLabel,#amountLabel{
                font-size:22px;
            }

            #newAddressButton, #sendButton {
                background-color: #5a5a5a;
                color: #ffffff;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 16px;
                margin-top: 10px;
            }

            #newAddressButton:hover, #sendButton:hover {
                background-color: #4a4a4a;
            }

         #recipientInput, #amountInput {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                padding: 6px;
                border-radius: 4px;
                 font-size: 18px;
                font-weight:bold;
            }
            #addressSelect{
                font-size: 16px;
                font-weight:bold;
            }
            
            
            #addressSelect::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #5a5a5a;
                border-left-style: solid;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }

           
            #addressSelect QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #5a5a5a;
                padding: 6px;
            }

            #addressSelect QAbstractItemView::item {
                padding: 6px;
                background-color: #ffffff;
            }

            #addressSelect QAbstractItemView::item:selected {
                background-color: #2d2d2d;
                color: #ffffff;
            }

            #addressSelect QAbstractItemView::item:hover {
                background-color: #5a5a5a !important;
                color: #ffffff;
            }
         
           
            #balanceLabel {
                font-size: 18px;
                padding: 10px;
                margin-bottom: 10px;
                color: #ffffff;
            }

            #transactionLabel {
                font-size: 14px;
                color: #ffffff;
                padding: 8px;
            }

            /* Tabs */
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
        """
        )

    def update_addresses(self):
        try:
            addresses = self.wallet_manager.rpc_connection.getaddressesbylabel("")
            self.address_select.clear()
            self.address_select.addItems(list(addresses.keys()))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao obter endereços: {e}")

    def generate_new_address(self):
        try:
            new_address = self.wallet_manager.create_new_address()
            self.address_select.addItem(new_address)
            self.address_select.setCurrentText(new_address)
            self.update_balance()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar novo endereço: {e}")

    def handle_send(self):
        sender_address = self.address_select.currentText()
        recipient_address = self.recipient_input.text()
        amount = Decimal(self.amount_input.text())

        try:
            txid = self.wallet_manager.rpc_connection.sendtoaddress(
                recipient_address, amount
            )
            self.transaction_label.setText(
                f"Transação enviada com sucesso! ID da transação: {txid}"
            )
            self.update_balance()

        except Exception as e:
            error_message = str(e)

            if "Insufficient funds" in error_message:
                start_index = error_message.find("Insufficient funds")
                end_index = error_message.find("\n", start_index)
                if end_index == -1:
                    end_index = len(error_message)
                error_message = error_message[start_index:end_index]

            QMessageBox.critical(
                self, "Erro", f"Erro ao enviar a transação: {error_message}"
            )

    def update_balance(self):
        selected_address = self.address_select.currentText()
        if selected_address:
            try:
                balance = Decimal(
                    self.wallet_manager.get_balance_for_address(selected_address)
                )
                if balance == 0:
                    self.balance_label.setText(f"Balance: 0.00000000 BTC")
                elif balance >= 0.00000001:
                    self.balance_label.setText(
                        f"Balance: {balance.quantize(Decimal('0.00000000'))} BTC"
                    )
                else:
                    self.balance_label.setText(f"Balance: {balance} BTC")

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar o saldo: {e}")
