import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont,QPixmap
import pickle
from PIL import Image as im

import cv2
import mediapipe as mp
import numpy as np


cameraStart = False


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
        self.recognition_button = QPushButton("Start Interpreter")
        self.recognition_button.setStyleSheet("background-color: #444654; color: white; padding: 10px; font-size: 16px;")
        self.recognition_button.setFixedSize(200, 50)  # size
        self.recognition_button.clicked.connect(self.recognize_sign_language)
        self.main_layout.addWidget(self.recognition_button, 1, alignment=Qt.AlignTop | Qt.AlignHCenter)

    def recognize_sign_language(self):
        # function for sign language recognition

        
        
        recognized_text = predicted_character        
        self.text_output.append(recognized_text)
        
        global cameraStart 
        cameraStart = True

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignLanguageApp()
    
    # set application color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#202123"))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)
    

    model_dict = pickle.load(open('./model.p', 'rb'))
    model = model_dict['model']

    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    labels_dict = {0: 'A', 1: 'B', 2: 'C'}
    while True:

        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()

        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,  # image to draw
                    hand_landmarks,  # model output
                    mp_hands.HAND_CONNECTIONS,  # hand connections
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

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

            predicted_character = "a"
            predicted_character = labels_dict[int(prediction[0])]
            print(predicted_character)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

        # cv2.imshow('frame', frame)
        data = im.fromarray(frame)
        data.save('image.png')
        if cameraStart:
            window.camera_label.setPixmap(QPixmap("image.png"))
        window.show()
        cv2.waitKey(1)
        


    cap.release()
    cv2.destroyAllWindows()
