from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFrame
from ui.components.buttons import StandardButton
from PyQt5.QtCore import Qt
from packaging import version
from pyguard.version import get_last_version, get_version
from pyguard.config import APP_AUTO_UPDATE
from pyguard.log import logger

class PrincipalView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        if APP_AUTO_UPDATE:
            self.check_for_update()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        

    def check_for_update(self):
        latest_version = get_last_version()
        current_version = get_version()

        if "error" not in latest_version.lower() and latest_version != "No tags found.":
            if version.parse(latest_version) > version.parse(current_version):
                self.show_update_message(latest_version)
                
    def show_update_message(self, latest_version):
        update_frame = QFrame(self)
        update_frame.setStyleSheet("""
            QFrame {
                background-color: #2E2E2E;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        update_layout = QVBoxLayout(update_frame)

        update_label = QLabel(f"A new version ({latest_version}) is available!", self)
        update_label.setStyleSheet("color: white; font-size: 28px;")
        update_label.setAlignment(Qt.AlignCenter)
        update_layout.addWidget(update_label)


        download_button = QPushButton("Download", self)
        download_button.setStyleSheet(StandardButton.primary_button_style())
        update_layout.addWidget(download_button)

        self.layout.addWidget(update_frame)