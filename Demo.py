import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def initUI(self):
        self.setWindowTitle('Camera Interface')

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_camera)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_camera)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close_application)

        self.video_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def start_camera(self):
        if not self.timer.isActive():
            self.timer.start(20)  # Update the frame every 20 ms

    def stop_camera(self):
        if self.timer.isActive():
            self.timer.stop()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def close_application(self):
        self.stop_camera()
        self.cap.release()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraApp()
    ex.show()
    sys.exit(app.exec_())
