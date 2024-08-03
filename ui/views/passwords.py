import sys
import json
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLineEdit, QApplication, QMessageBox, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QClipboard, QPixmap
from pyguard.config import APP_THEME_COLOR, APP_FONT, DATA_FILE
from ui.components.buttons import StandardButton
from pyguard.password import generate_secure_password # Add more complexity to the password creation later
from pyguard.encryption import encrypt_password, decrypt_password

class ToastNotification(QWidget):
    def __init__(self, message, duration=3000):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(250, 50)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        label = QLabel(message, self)
        label.setStyleSheet(f"color: white; background-color: {APP_THEME_COLOR}; padding: 10px; border-radius: 5px;")
        layout.addWidget(label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        self.timer.start(duration)

    def show_notification(self, parent=None):
        if parent:
            geom = parent.geometry()
            x = geom.right() - self.width() - 10
            y = geom.bottom() - self.height() - 10
            self.move(x, y)
        self.show()

class PasswordsView(QWidget):
    def __init__(self):
        super().__init__()
        self.passwords = {}
        self.initUI()
        self.load_passwords()

    def initUI(self):
        self.setWindowTitle('Password Manager')
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #2E2E2E;
                color: #E0E0E0;
                border-radius:5px;
                font-family: {APP_FONT}
            }}
            QLineEdit {{
                background-color: #2E2E2E;
                border: 1px solid #666;
                border-radius: 5px;
                font-size: 20px;
                padding: 7px;
                color: #E0E0E0;
            }}
            {StandardButton.button_style()}
            QLabel {{
                color: #E0E0E0;
                font-size: 14px;
                margin: 5px 10px;
            }}
            QFrame {{
                border: none;
            }}
            QScrollArea {{
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)

        input_layout = QHBoxLayout()
        
        self.label_input = QLineEdit(self)
        self.label_input.setPlaceholderText('Enter label (e.g., YouTube)')
        input_layout.addWidget(self.label_input)

        self.generate_button = QPushButton('Generate Password', self)
        self.generate_button.setStyleSheet(StandardButton.generate_button_style())
        self.generate_button.clicked.connect(self.generate_password)
        input_layout.addWidget(self.generate_button)

        layout.addLayout(input_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

    def load_passwords(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                try:
                    self.passwords = json.load(file)
                    self.load_displayed_passwords()
                except json.JSONDecodeError:
                    print("Error reading JSON file.")
        else:
            print("Password file does not exist.")

    def load_displayed_passwords(self):
        for label, encrypted_password in self.passwords.items():
            password = decrypt_password(encrypted_password)
            self.display_password(label, password)

    def generate_password(self):
        label_text = self.label_input.text().strip()
        if not label_text:
            QMessageBox.warning(self, 'Input Error', 'Please enter a label.')
            return

        if label_text in self.passwords:
            QMessageBox.warning(self, 'Duplicate Label', 'A password with this label already exists.')
            return

        password = generate_secure_password()
        encrypted_password = encrypt_password(password)
        self.passwords[label_text] = encrypted_password

        self.display_password(label_text, password)
        self.label_input.clear()
        self.save_passwords()

    def confirm_regenerate(self, label_display, label_text):
        reply = QMessageBox.question(self, 'Confirm Regenerate', 'Are you sure you want to regenerate the password?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("Regenerate password")
            
    def update_password_display(self, label_display, label_text, new_password):
        label_display.setText(f'{label_text}: {self.censored_password(new_password)}')
        self.copy_to_clipboard(new_password)

    def copy_to_clipboard(self, text):
        if not isinstance(text, str):
            print("Error: Expected a string for text, but got:", type(text))
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        display_text = text[:4] + '...' if len(text) > 4 else text
        toast = ToastNotification(f'Copied to clipboard: {display_text}')
        toast.show_notification(self)


    def create_button(self, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        button.setStyleSheet(StandardButton.button_style())
        return button

    def save_passwords(self):
        with open(DATA_FILE, 'w') as file:
            json.dump(self.passwords, file)

    def display_password(self, label, password):
        container = QFrame()
        h_layout = QHBoxLayout(container)

        # Icon (Placeholder)
        icon_label = QLabel(self)
        icon_label.setFixedSize(24, 24)
        icon_label.setPixmap(QPixmap("path/to/icon.png").scaled(24, 24, Qt.KeepAspectRatio))
        h_layout.addWidget(icon_label, alignment=Qt.AlignLeft)

        label_display = QLabel(f'{label}: {self.censored_password(password)}', self)
        label_display.setObjectName("label_display")
        label_display.setAlignment(Qt.AlignCenter)

        show_button = self.create_button('Show Password', lambda: self.toggle_password_display(label_display, label, password))
        copy_button = self.create_button('Copy Password', lambda: self.copy_to_clipboard(password))
        delete_button = self.create_button('Delete', lambda: self.delete_row(label_display, label, password))

        button_layout = QHBoxLayout()
        button_layout.addWidget(show_button)
        button_layout.addWidget(copy_button)
        button_layout.addWidget(delete_button)
        button_layout.setAlignment(Qt.AlignCenter)

        v_layout = QVBoxLayout()
        v_layout.addWidget(label_display, alignment=Qt.AlignCenter)
        v_layout.addLayout(button_layout)

        h_layout.addLayout(v_layout)
        h_layout.setAlignment(Qt.AlignCenter)

        container.setLayout(h_layout)
        container.setStyleSheet("QFrame { border: none; }")

        label_display.show_button = show_button
        self.scroll_layout.addWidget(container)


    def toggle_password_display(self, label_display, label, password):
        current_text = label_display.text()
        if 'Show Password' in label_display.show_button.text():
            label_display.setText(f'{label}: {password}')
            label_display.show_button.setText('Hide Password')
        else:
            label_display.setText(f'{label}: {self.censored_password(password)}')
            label_display.show_button.setText('Show Password')
            
    def delete_row(self, label_display, label, password):
        """
        Delete the password entry from the UI and the JSON file.

        Args:
            label_display (QLabel): The QLabel widget displaying the password label.
            label (str): The label of the password entry.
            password (str): The password to be deleted.
        """
        reply = QMessageBox.question(self, 'Confirm Delete', 
                                    f'Are you sure you want to delete the password for "{label}"?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            container = label_display.parentWidget()
            self.scroll_layout.removeWidget(container)
            container.setParent(None)
            container.deleteLater()

            if label in self.passwords:
                del self.passwords[label]

            self.save_passwords()

            toast = ToastNotification(f'Deleted: {label}')
            toast.show_notification(self)


    def censored_password(self, password):
        return '*' * len(password)