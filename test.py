import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QStackedWidget,QHBoxLayout
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QStackedWidget,QHBoxLayout

# Mock user data (you should replace this with a real database)
users = {'username': 'password'}

class LoginPage(QWidget):
    def _init_(self, stacked_widget):
        super()._init_()

        self.stacked_widget = stacked_widget

        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 400, 200)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label_username = QLabel("Username:")
        self.entry_username = QLineEdit()
        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.entry_username)

        self.label_password = QLabel("Password:")
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.entry_password)

        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.login)
        self.layout.addWidget(self.btn_login)

        self.setLayout(self.layout)

    def login(self):
        username = self.entry_username.text()
        password = self.entry_password.text()

        if username in users and users[username] == password:
            QMessageBox.information(self, "Login Successful", "Welcome, " + username)
            self.stacked_widget.setCurrentIndex(1)  # Switch to the homepage view
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password")

class HomePage(QWidget):
    def _init_(self):
        super()._init_()

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

def main():
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    login_page = LoginPage(stacked_widget)
    homepage = HomePage()

    stacked_widget.addWidget(login_page)
    stacked_widget.addWidget(homepage)

    # Set the initial page to the login page
    stacked_widget.setCurrentIndex(0)

    stacked_widget.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()