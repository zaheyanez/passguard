import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt5.QtGui import QIcon
from pyguard.config import APP_NAME, APP_VERSION, APP_ICON

from ui.views.home import PrincipalView
from ui.views.passwords import PasswordsView
from ui.views.settings import SettingsView

from ui.components.buttons import SidebarButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.setWindowIcon(QIcon(f"{APP_ICON}"))
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
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
        button_names = ['Home', 'Passwords', 'Settings']
        for name in button_names:
            button = SidebarButton(name)
            button.clicked.connect(lambda _, text=name: self.change_content(text))
            self.sidebar_layout.addWidget(button)
            self.buttons[name] = button

        close_button = SidebarButton('Close')
        close_button.clicked.connect(self.close)
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(close_button)
        self.buttons['Close'] = close_button

        h_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget()
        h_layout.addWidget(self.stacked_widget)

        self.principal_view = PrincipalView()
        self.stacked_widget.addWidget(self.principal_view)

        self.password_view = PasswordsView()
        self.stacked_widget.addWidget(self.password_view)

        self.settings_view = SettingsView()
        self.stacked_widget.addWidget(self.settings_view)

        self.change_content('Home')

    def change_content(self, view_name):
        if view_name == 'Home':
            self.stacked_widget.setCurrentWidget(self.principal_view)
        elif view_name == 'Passwords':
            self.stacked_widget.setCurrentWidget(self.password_view)
        elif view_name == 'Settings':
            self.stacked_widget.setCurrentWidget(self.settings_view)

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