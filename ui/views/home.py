from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt
from packaging import version
from passguard.version import get_last_version, get_version
from passguard.config import APP_NAME
from passguard.settings import load_config
from ui.components.buttons import StandardButton

class PrincipalView(QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.initUI()
        if self.config['APP_AUTO_UPDATE']:
            print("Starting update searching...")
            self.check_for_update()
        else:
            self.show_usage_instructions()

    def initUI(self):
        self.layout = QVBoxLayout(self)

    def check_for_update(self):
        latest_version = get_last_version()
        current_version = get_version()

        if "error" not in latest_version.lower() and latest_version != "No tags found.":
            if version.parse(latest_version) > version.parse(current_version):
                self.show_update_message(latest_version)
            else:
                self.show_usage_instructions()
        else:
            self.show_usage_instructions()

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

    def show_usage_instructions(self):
        instruction_frame = QFrame(self)
        instruction_frame.setStyleSheet("""
            QFrame {
                background-color: #2E2E2E;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        instruction_layout = QVBoxLayout(instruction_frame)

        instruction_label = QLabel(f"How to use {APP_NAME}", self)
        instruction_label.setStyleSheet("color: white; font-size: 24px;")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_layout.addWidget(instruction_label)

        steps = [
            "1. Go to passwords.",
            "2. Enter a label to identify your password.",
            "3. Click 'Generate Password'.",
            "4. Use the 'Copy' button to use it, no need to view it.",
            f"5. No save buttons needed, {APP_NAME} will remember next time you open the program."
        ]

        for step in steps:
            step_label = QLabel(step, self)
            step_label.setStyleSheet("color: white; font-size: 18px;")
            step_label.setAlignment(Qt.AlignLeft)
            instruction_layout.addWidget(step_label)

        self.layout.addWidget(instruction_frame)