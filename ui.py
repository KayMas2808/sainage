import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon

class SignLanguageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("sAInage")
        self.setWindowIcon(QIcon("/record.png"))
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        # Left side for text output
        self.left_layout = QVBoxLayout()

        # Top navigation bar with icons for chat history, user account, and logout
        self.nav_layout = QHBoxLayout()
        self.chat_history_button = QPushButton()
        self.chat_history_button.setIcon(QIcon("/history.png"))
        self.chat_history_button.setFixedSize(40, 40)
        self.user_account_button = QPushButton()
        self.user_account_button.setIcon(QIcon.fromTheme("user-identity"))
        self.user_account_button.setFixedSize(40, 40)
        self.logout_button = QPushButton()
        self.logout_button.setIcon(QIcon("/logout.png"))
        self.logout_button.setFixedSize(40, 40)
        self.nav_layout.addWidget(self.chat_history_button)
        self.nav_layout.addWidget(self.user_account_button)
        self.nav_layout.addWidget(self.logout_button)
        self.left_layout.addLayout(self.nav_layout)

        # Text output area (dynamic height)
        self.text_box = QFrame()
        self.text_box.setStyleSheet("background-color: #292929; border-radius:15px;")
        self.text_heading = QLabel("Output")
        self.text_heading.setFont(QFont("Roboto Flex", 12, QFont.Bold))
        self.text_output = QTextEdit(self.text_box)
        self.text_output.setStyleSheet("background-color: #3c3c3c; color: white; padding: 10px;")
        self.text_output.setReadOnly(True)
        self.text_output.setAlignment(Qt.AlignLeft)
        self.left_layout.addWidget(self.text_heading)
        self.left_layout.addWidget(self.text_box, 1)  # Dynamic height

        # Add the left side layout to the main layout
        self.layout.addLayout(self.left_layout, 40)  # 40% of width

        # Right side for camera input
        self.right_layout = QVBoxLayout()

        # Camera input area
        self.camera_box = QFrame()
        self.camera_box.setStyleSheet("background-color: #3c3c3c; border-radius:15px;")
        self.camera_heading = QLabel("Camera")
        self.camera_heading.setFont(QFont("Roboto Flex", 12, QFont.Bold))
        self.camera_label = QLabel(self.camera_box)
        self.camera_label.setAlignment(Qt.AlignRight)
        self.right_layout.addWidget(self.camera_heading)
        self.right_layout.addWidget(self.camera_box, 60)  # 60% of width

        # Button to start interpreter
        self.recognition_button = QPushButton("Start Interpreter")
        self.recognition_button.setStyleSheet("background-color: #19c37d; color: white; padding: 10px; font-size: 23px;border-radius:15px;")
        self.recognition_button.setIcon(QIcon.fromTheme("media-record"))
        self.recognition_button.setFont(QFont("Roboto Flex", 12))
        self.right_layout.addWidget(self.recognition_button)

        # Add the right side layout to the main layout
        self.layout.addLayout(self.right_layout, 60)  # 60% of width

    def recognize_sign_language(self):
        # Function for sign language recognition
        recognized_text = "This is a placeholder for recognized sign language."
        self.text_output.append(recognized_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignLanguageApp()

    # Set application color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#121212"))  # Set the background to black
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)

    window.showMaximized()
    sys.exit(app.exec_())
