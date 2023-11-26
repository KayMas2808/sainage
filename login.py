import sys
import sqlite3
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)

        # Create widgets
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        self.edit_password_button = QPushButton("Edit Password")  

        # QSS to style widgets
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                margin-bottom: 5px;
            }
            QLineEdit, QPushButton {
                font-size: 16px;
                padding: 10px;
                margin: 5px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        # Create layouts
        self.main_layout = QVBoxLayout()
        self.form_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        # Add widgets to layouts
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addWidget(self.password_input)
        self.button_layout.addWidget(self.login_button)
        self.button_layout.addWidget(self.signup_button)
        self.button_layout.addWidget(self.edit_password_button)  # Add the new button
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)

        # Set main layout
        self.setLayout(self.main_layout)

        # Connect signals and slots
        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.signup)
        self.edit_password_button.clicked.connect(self.edit_password)  # Connect the new button

        # Create database connection
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Check if user exists in the database
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            subprocess.Popen(["python", "main.py", username])  # Pass the username to main.py
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def signup(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Check if the username already exists in the database
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()

        if user:
            QMessageBox.warning(self, "Sign Up Failed", "Username already exists.")
        else:
            self.cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            self.conn.commit()
            QMessageBox.information(self, "Sign Up Successful", "You have successfully signed up.")

    def edit_password(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Check if user exists in the database
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            # Create a dialog to get the new password
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Password")
            dialog.setFixedSize(300, 150)

            new_password_label = QLabel("New Password:")
            new_password_input = QLineEdit()
            new_password_button = QPushButton("Save")

            new_password_layout = QVBoxLayout()
            new_password_layout.addWidget(new_password_label)
            new_password_layout.addWidget(new_password_input)
            new_password_layout.addWidget(new_password_button)

            dialog.setLayout(new_password_layout)

            # Define a function to save the new password
            def save_new_password():
                new_password = new_password_input.text()
                self.cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
                self.conn.commit()
                QMessageBox.information(self, "Password Updated", "Password has been updated.")
                dialog.accept()

            new_password_button.clicked.connect(save_new_password)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Edit Password Failed", "Invalid username or password.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
