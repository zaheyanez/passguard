import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt5.QtGui import QIcon
from pyguard.config import APP_NAME, APP_VERSION, APP_ICON

from ui.views.home import PrincipalView
from ui.views.passwords import PasswordsView
from ui.views.settings import SettingsView
from ui.views.credits import CreditsView

from ui.components.buttons import SidebarButton

HOME_BUTTON_NAME="Home 🛡️"
PASSWORD_BUTTON_NAME="Passwords 🔒"
SETTINGS_BUTTON_NAME="Settings ⚙️"
CREDITS_BUTTON_NAME="Credits ✨"
QUIT_BUTTON_NAME="Quit 👋"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.setWindowIcon(QIcon(f"{APP_ICON}"))
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #222222;")
        self.setCentralWidget(central_widget)
        

        h_layout = QHBoxLayout(central_widget)
        h_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #1E1E1E;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setSpacing(0)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        self.buttons = {}
        button_names = [HOME_BUTTON_NAME, PASSWORD_BUTTON_NAME, SETTINGS_BUTTON_NAME, CREDITS_BUTTON_NAME]
        for name in button_names:
            button = SidebarButton(name)
            button.clicked.connect(lambda _, text=name: self.change_content(text))
            self.sidebar_layout.addWidget(button)
            self.buttons[name] = button

        close_button = SidebarButton(QUIT_BUTTON_NAME)
        close_button.clicked.connect(self.close)
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(close_button)
        self.buttons[QUIT_BUTTON_NAME] = close_button

        h_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget()
        h_layout.addWidget(self.stacked_widget)

        self.principal_view = PrincipalView()
        self.stacked_widget.addWidget(self.principal_view)

        self.password_view = PasswordsView()
        self.stacked_widget.addWidget(self.password_view)

        self.settings_view = SettingsView()
        self.stacked_widget.addWidget(self.settings_view)
        
        self.credits_view = CreditsView()
        self.stacked_widget.addWidget(self.credits_view)

        self.change_content(HOME_BUTTON_NAME)

    def change_content(self, view_name):
        if view_name == HOME_BUTTON_NAME:
            self.stacked_widget.setCurrentWidget(self.principal_view)
        elif view_name == PASSWORD_BUTTON_NAME:
            self.stacked_widget.setCurrentWidget(self.password_view)
        elif view_name == SETTINGS_BUTTON_NAME:
            self.stacked_widget.setCurrentWidget(self.settings_view)
        elif view_name == CREDITS_BUTTON_NAME:
            self.stacked_widget.setCurrentWidget(self.credits_view)

        for name, button in self.buttons.items():
            button.set_active(name == view_name)

def start_gui():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())


def close_gui():
    """
    Properly close the GUI application by terminating any background threads
    or processes and then exiting the application.
    """
    import os
    # Exit the application.
    os._exit(1)