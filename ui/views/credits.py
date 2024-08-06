from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from passguard.config import APP_NAME, APP_AUTHOR, APP_REPOSITORY, APP_VERSION, APP_LICENSE
from ui.components.buttons import StandardButton
import webbrowser

class CreditsView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                color: #FFFFFF;
                font-family: Arial;
                background-color: #2E2E2E;
                border-radius: 5px;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            QLabel#section-title {
                font-size: 20px;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            QLabel#content {
                font-size: 16px;
                margin-top: 5px;
                margin-bottom: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("Credits 🏆")
        title.setObjectName("title")
        layout.addWidget(title)

        version_label = QLabel(f"{APP_NAME} {APP_VERSION}")
        version_label.setObjectName("content")
        layout.addWidget(version_label)

        author_label = QLabel(f"Author: {APP_AUTHOR}")
        author_label.setObjectName("content")
        layout.addWidget(author_label)

        repo_label = QLabel(f"Repository: {APP_REPOSITORY}")
        repo_label.setObjectName("content")
        layout.addWidget(repo_label)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        repo_button = QPushButton("Repository")
        repo_button.setStyleSheet(StandardButton.primary_button_style())
        repo_button.clicked.connect(self.open_repository)
        button_layout.addWidget(repo_button)
        
        other_button = QPushButton("Placeholder button")
        other_button.setStyleSheet(StandardButton.button_style())
        other_button.clicked.connect(self.open_repository)
        button_layout.addWidget(other_button)

        layout.addLayout(button_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
    def open_repository(self):
        webbrowser.open(APP_REPOSITORY)
