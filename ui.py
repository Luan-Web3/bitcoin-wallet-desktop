import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtCore import Qt
import wallet_manager_mock


class CryptoWalletUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Wallet")
        self.initUI()

    def initUI(self):
        # Labels e LineEdits para Endereço e Saldo
        self.addressLabel = QLabel("Endereço:")
        self.addressValueLabel = QLabel("N/A")
        self.balanceLabel = QLabel("Saldo:")
        self.balanceValueLabel = QLabel("0.00 BTC")

        # Botões
        self.refreshButton = QPushButton("Atualizar Saldo")
        self.sendButton = QPushButton("Enviar")
        self.receiveButton = QPushButton("Receber")

        # Layouts
        vbox = QVBoxLayout()
        hboxAddress = QHBoxLayout()
        hboxBalance = QHBoxLayout()
        hboxButtons = QHBoxLayout()

        hboxAddress.addWidget(self.addressLabel)
        hboxAddress.addWidget(self.addressValueLabel)
        hboxBalance.addWidget(self.balanceLabel)
        hboxBalance.addWidget(self.balanceValueLabel)
        hboxButtons.addWidget(self.refreshButton)
        hboxButtons.addWidget(self.sendButton)
        hboxButtons.addWidget(self.receiveButton)

        vbox.addLayout(hboxAddress)
        vbox.addLayout(hboxBalance)
        vbox.addLayout(hboxButtons)
        vbox.setAlignment(Qt.AlignTop)

        self.setLayout(vbox)

        self.refreshButton.clicked.connect(self.updateBalance)
        self.sendButton.clicked.connect(self.showSendDialog)
        self.receiveButton.clicked.connect(self.showReceiveDialog)

        self.getInitialData()

    def getInitialData(self):
        try:
            address = wallet_manager_mock.get_address()
            balance = wallet_manager_mock.get_balance()
            self.addressValueLabel.setText(address)
            self.balanceValueLabel.setText(f"{balance:.8f} BTC")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar dados iniciais: {e}")

    def updateBalance(self):
        try:
            balance = wallet_manager_mock.get_balance()
            self.balanceValueLabel.setText(f"{balance:.8f} BTC")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar saldo: {e}")

    def showSendDialog(self):
        QMessageBox.information(self, "Enviar", "Funcionalidade de envio em desenvolvimento.")

    def showReceiveDialog(self):
        QMessageBox.information(self, "Receber", "Funcionalidade de recebimento em desenvolvimento.")


def main():
    app = QApplication(sys.argv)
    ex = CryptoWalletUI()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()