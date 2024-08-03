from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class PrincipalView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        label = QLabel('Home')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)