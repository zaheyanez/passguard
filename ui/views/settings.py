from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QColorDialog
from PyQt5.QtCore import Qt
import pyguard.config as config

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        
