import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont

class SignLanguageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sign Language Recognition App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()

        # Sidebar for chat history (15% of the screen width)
        self.sidebar = QTextEdit()
        self.sidebar.setReadOnly(True)
        self.sidebar.setStyleSheet("background-color: #202123; color: white;")
        self.layout.addWidget(self.sidebar, 15)  # Set to 15% of the width

        # Main area divided into upper 60% for camera input and lower 40% for text output
        self.main_area = QWidget()
        self.main_layout = QVBoxLayout(self.main_area)

        # Camera input area (upper 60%)
        self.camera_heading = QLabel("Camera")
        self.camera_heading.setFont(QFont("Arial", 12, QFont.Bold))
        self.main_layout.addWidget(self.camera_heading)
        self.camera_label = QLabel(self.main_area)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: #444654;")
        self.main_layout.addWidget(self.camera_label, 60)  # Set to 60% of the height

        # Text output area (lower 40%)
        self.text_heading = QLabel("Output")
        self.text_heading.setFont(QFont("Arial", 12, QFont.Bold))
        self.main_layout.addWidget(self.text_heading)
        self.text_output = QTextEdit(self.main_area)
        self.text_output.setStyleSheet("background-color: #343541; color: white; padding: 10px;")
        self.main_layout.addWidget(self.text_output, 40)  # Set to 40% of the height

        self.layout.addWidget(self.main_area, 85)  # Set to 85% of the width

        self.central_widget.setLayout(self.layout)

        # Placeholder to simulate camera input
        self.camera_label.setText("Camera Input")

        # Recognition button (on the camera input area)
        self.recognition_button = QPushButton("Recognize Sign Language")
        self.recognition_button.setStyleSheet("background-color: #444654; color: white; padding: 10px; font-size: 16px;")
        self.recognition_button.setFixedSize(200, 50)  # Increased size
        self.main_layout.addWidget(self.recognition_button, 1, alignment=Qt.AlignTop | Qt.AlignHCenter)

    def recognize_sign_language(self):
        # Placeholder function for sign language recognition
        recognized_text = "This is a placeholder for recognized sign language."
        self.text_output.append(recognized_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignLanguageApp()
    
    # Set the application's color palette for consistent styling
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#202123"))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)
    
    window.show()
    sys.exit(app.exec_())
