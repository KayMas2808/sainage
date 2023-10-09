import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QFrame,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon, QPixmap
import pickle
from PIL import Image as im
from collections import Counter
import cv2
import mediapipe as mp
import numpy as np


cameraStart = False

def most_common_value(lst):
    # Use Counter to count occurrences of each element
    counter = Counter(lst)

    # Use the most_common() method to get a list of (element, count) tuples
    most_common_elements = counter.most_common()

    # Check if the list is not empty
    if most_common_elements:
        # Return the most common element (first element of the first tuple)
        return most_common_elements[0][0]
    else:
        # If the list is empty, return None or handle the case as needed
        return None


# ...

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
        self.text_output.setStyleSheet(
            "background-color: #3c3c3c; color: white; padding: 10px;"
        )
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
        self.camera_label.setAlignment(Qt.AlignLeft)
        self.camera_label.setMinimumSize(1131, 839)
        self.right_layout.addWidget(self.camera_heading)
        self.right_layout.addWidget(self.camera_box, 60)  # 60% of width

        # Button to start/stop interpreter
        self.recognition_button = QPushButton("Start Interpreter")
        self.recognition_button.setStyleSheet(
            "background-color: #19c37d; color: white; padding: 10px; font-size: 23px;border-radius:15px;"
        )
        self.recognition_button.setIcon(QIcon.fromTheme("media-record"))
        self.recognition_button.setFont(QFont("Roboto Flex", 12))
        self.right_layout.addWidget(self.recognition_button)
        self.recognition_button.clicked.connect(self.toggle_recognition)

        # Add the right side layout to the main layout
        self.layout.addLayout(self.right_layout, 60)  # 60% of width

        # Initialize the recognition flag
        self.recognizing = False

    def toggle_recognition(self):
        # Toggle recognition on/off
        global cameraStart
        self.recognizing = not self.recognizing
        cameraStart = self.recognizing
        if self.recognizing:
            self.recognition_button.setText("Stop Interpreter")
            self.recognition_button.setIcon(QIcon.fromTheme("media-playback-stop"))
        else:
            self.recognition_button.setText("Start Interpreter")
            self.recognition_button.setIcon(QIcon.fromTheme("media-record"))

# ...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignLanguageApp()

    # Set application color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#121212"))  # Set the background to black
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
    labels_dict = {0: "A", 1: "B", 2: "C"}
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

    cap.release()
    cv2.destroyAllWindows()