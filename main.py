import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,  # Add QLabel import
    QFrame,
    QDialog
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon, QPixmap
import pickle
from PIL import Image as im
import cv2
import mediapipe as mp
import numpy as np
from collections import Counter
import sqlite3
import pyttsx3

def most_common_value(lst):
    counter = Counter(lst)
    most_common_elements = counter.most_common()
    if most_common_elements:
        ttsFunction(most_common_elements[0][0])
        return most_common_elements[0][0]
    else:
        return None

cameraStart = False

class SignLanguageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("sAInage")
        self.setWindowIcon(QIcon("images/logo.png"))
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_ui()

        self.recognizing = False
        self.chat_history = []

        self.conn=sqlite3.connect('chat_history.db')
        self.create_table()

    def create_table(self):
        cursor=self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,message TEXT)""")
        self.conn.commit()

    def save_to_database(self, message):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO chat_history (message) VALUES (?)", (message,))
        self.conn.commit()

    def retrieve_chat_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT message FROM chat_history")
        history = cursor.fetchall()
        return [item[0] for item in history]

    def setup_ui(self):
        self.layout = QHBoxLayout(self.central_widget)

        self.left_layout = QVBoxLayout()

        self.nav_layout = QHBoxLayout()
        self.copy_button = QPushButton("  Copy")
        self.copy_button.setIcon(QIcon("images/copy.png"))
        self.copy_button.setStyleSheet(
            "background-color: #19c37d; color: white; padding: 10px; font-size: 16px; border-radius: 15px;"
        )
        self.copy_button.clicked.connect(self.copy_text)
        self.history_button = QPushButton("  History")
        self.history_button.setIcon(QIcon("images/history.png"))
        self.history_button.setStyleSheet(
            "background-color: #19c37d; color: white; padding: 10px; font-size: 16px; border-radius: 15px;"
        )
        self.history_button.clicked.connect(self.show_chat_history)

        self.logout_button = QPushButton("  Exit")
        self.logout_button.setIcon(QIcon("images/exit.png"))
        self.logout_button.setStyleSheet(
            "background-color: #fe0000; color: white; padding: 10px; font-size: 16px; border-radius: 15px;"
        )
        self.logout_button.clicked.connect(self.close)  # Exit the program
        self.nav_layout.addWidget(self.copy_button)
        self.nav_layout.addWidget(self.history_button)
        self.nav_layout.addWidget(self.logout_button)
        self.left_layout.addLayout(self.nav_layout)

        self.text_box = QFrame()
        self.text_box.setStyleSheet("background-color: #3c3c3c; border-radius:15px;")
        self.text_heading = QLabel("Output")
        self.text_heading.setFont(QFont("Roboto Flex", 12, QFont.Bold))
        self.text_output = QTextEdit(self.text_box)
        self.text_output.setStyleSheet(
            "background-color: #3c3c3c; color: white; padding: 10px; font-size: 20px;"
        )
        self.text_output.setReadOnly(True)
        self.text_output.setAlignment(Qt.AlignLeft)
        self.left_layout.addWidget(self.text_heading)
        self.left_layout.addWidget(self.text_output, 2)  # Increased size

        self.layout.addLayout(self.left_layout, 40)

        self.right_layout = QVBoxLayout()

        self.camera_box = QFrame()
        self.camera_box.setStyleSheet("background-color: #3c3c3c; border-radius:15px;")
        self.camera_heading = QLabel("Camera")
        self.camera_heading.setFont(QFont("Roboto Flex", 12, QFont.Bold))
        self.camera_label = QLabel(self.camera_box)
        self.camera_label.setAlignment(Qt.AlignCenter)  # Center camera output
        self.right_layout.addWidget(self.camera_heading)
        self.right_layout.addWidget(self.camera_label, 5)  # Increased size

        # Add a QLabel for displaying text when the interpreter is off
        self.interpreter_status_label = QLabel("Interpreter is OFF")
        self.interpreter_status_label.setFont(QFont("Roboto Flex", 12, QFont.Bold))
        self.interpreter_status_label.setStyleSheet(
            "background-color: #3c3c3c; color: white; padding: 10px; font-size: 20px;"
        )
        self.interpreter_status_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.interpreter_status_label)

        self.recognition_button = QPushButton("Start Interpreter")
        self.recognition_button.setStyleSheet(
            "background-color: #19c37d; color: white; padding: 10px; font-size: 23px; border-radius: 15px;"
        )
        self.recognition_button.setIcon(QIcon("images/record.png"))
        self.recognition_button.setFont(QFont("Roboto Flex", 12))
        self.right_layout.addWidget(self.recognition_button)
        self.recognition_button.clicked.connect(self.toggle_recognition)

        self.layout.addLayout(self.right_layout, 60)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_output.toPlainText())

    def toggle_recognition(self):
        global cameraStart
        self.recognizing = not self.recognizing
        cameraStart = self.recognizing
        if self.recognizing:
            self.recognition_button.setText("Stop Interpreter")
            self.interpreter_status_label.setText("Interpreter is ON")
        else:
            self.recognition_button.setText("Start Interpreter")
            self.interpreter_status_label.setText("Interpreter is OFF")

    def show_chat_history(self):
        history_dialog = ChatHistoryDialog(self.retrieve_chat_history())
        history_dialog.exec_()

    @pyqtSlot()
    def closeEvent(self, event):
        global cap
        cap.release()
        cv2.destroyAllWindows()
        self.conn.close()  # Close the database connection
        event.accept()

class ChatHistoryDialog(QDialog):
    def __init__(self, chat_history):
        super().__init__()

        self.setWindowTitle("Chat History")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)

        layout.addWidget(self.history_text)

        self.chat_history = chat_history

        self.load_history()

        self.setLayout(layout)

    def load_history(self):
        self.history_text.setPlainText("\n".join(self.chat_history))

def ttsFunction(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignLanguageApp()

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#121212"))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)

    model_dict = pickle.load(open("./model.p", "rb"))
    model = model_dict["model"]

    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
    buffer = []
    labels_dict = {0: "Hello", 1: "How are you", 2: "I am fine", 3: "Thank you",4:"what is your name",5:"test"}
    while True:
        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()

        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        predicted_character = ""
        results = hands.process(frame_rgb)
        try:
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,  # image to draw
                        hand_landmarks,  # model output
                        mp_hands.HAND_CONNECTIONS,  # hand connections
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                    )

                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10

                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                prediction = model.predict([np.asarray(data_aux)])

                predicted_character = labels_dict[int(prediction[0])]
                print(predicted_character)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(
                    frame,
                    predicted_character,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.3,
                    (0, 0, 0),
                    3,
                    cv2.LINE_AA,
                )
        except:
            print("error")

        data = im.fromarray(frame)
        data.save("image.png")
        if cameraStart:
            window.camera_label.setPixmap(QPixmap("image.png"))
            if predicted_character != "":
                if len(buffer) < 10:
                    buffer.append(predicted_character)
                else:
                    window.text_output.append(most_common_value(buffer))
                    buffer = []

        window.showMaximized()
        cv2.waitKey(1)

    sys.exit(app.exec_())
