from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from passguard.config import APP_THEME_COLOR
from passguard.settings import save_config, load_config
from ui.components.buttons import StandardButton

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Checkbox for APP_AUTO_UPDATE
        self.auto_update_checkbox = QCheckBox('Enable Auto Update', self)
        self.auto_update_checkbox.setChecked(self.config.get('APP_AUTO_UPDATE', True))
        self.auto_update_checkbox.setStyleSheet(f"""
            QWidget {{
                background-color: #2E2E2E;
                color: #E0E0E0;
                border-radius:5px;
                padding: 10px 0;
            }}
            QCheckBox {{
                color: white;
                font-size:16px;
                padding: 14px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
            }}
            QCheckBox::indicator:unchecked {{
                background-color: #555;
                border: 1px solid #777;
            }}
            QCheckBox::indicator:checked {{
                background-color: {APP_THEME_COLOR};
                border: 1px solid {APP_THEME_COLOR};
            }}
        """)
        layout.addWidget(self.auto_update_checkbox)

        # Save Button
        self.save_button = StandardButton('Save Settings', self)
        self.save_button.setStyleSheet(StandardButton.primary_button_style())
        self.save_button.clicked.connect(self.save_settings)
        
        # Create a layout for the button and align it to the right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_settings(self):
        self.config['APP_AUTO_UPDATE'] = self.auto_update_checkbox.isChecked()
        save_config(self.config)
        QMessageBox.information(self, 'Settings', 'Settings have been saved.')
