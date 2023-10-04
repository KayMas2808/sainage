import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont

class SignLanguageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("sAInage")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()

        # sidebar
        self.sidebar = QTextEdit()
        self.sidebar.setReadOnly(True)
        self.sidebar.setStyleSheet("background-color: #202123; color: white;")
        self.layout.addWidget(self.sidebar, 15) #15% width

        #main area
        self.main_area = QWidget()
        self.main_layout = QVBoxLayout(self.main_area)

       #camera input area
        self.camera_heading = QLabel("Camera")
        self.camera_heading.setFont(QFont("Arial", 12, QFont.Bold))
        self.main_layout.addWidget(self.camera_heading)
        self.camera_label = QLabel(self.main_area)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: #444654;")
        self.main_layout.addWidget(self.camera_label, 60)  # 60% of height

        # text output area
        self.text_heading = QLabel("Output")
        self.text_heading.setFont(QFont("Arial", 12, QFont.Bold))
        self.main_layout.addWidget(self.text_heading)
        self.text_output = QTextEdit(self.main_area)
        self.text_output.setStyleSheet("background-color: #343541; color: white; padding: 10px;")
        self.main_layout.addWidget(self.text_output, 40)  # 40% of height

        self.layout.addWidget(self.main_area, 85)  # 85% of width

        self.central_widget.setLayout(self.layout)

        # Placeholder to simulate camera input
        self.camera_label.setText("Camera Input")

        # Recognition button (on the camera input area)
        self.recognition_button = QPushButton("Text Output")
        self.recognition_button.setStyleSheet("background-color: #444654; color: white; padding: 10px; font-size: 16px;")
        self.recognition_button.setFixedSize(200, 50)  # size
        self.main_layout.addWidget(self.recognition_button, 1, alignment=Qt.AlignTop | Qt.AlignHCenter)

    def recognize_sign_language(self):
        # function for sign language recognition
        recognized_text = "This is a placeholder for recognized sign language."
        self.text_output.append(recognized_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignLanguageApp()
    
    # set application color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#202123"))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)
    
    window.show()
    sys.exit(app.exec_())
