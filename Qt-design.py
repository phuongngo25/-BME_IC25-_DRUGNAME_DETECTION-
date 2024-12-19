import sys
import cv2
import requests
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CameraApp(QWidget):
    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def initUI(self):
        self.setWindowTitle('ESP32-CAM Stream')

        self.video_label = QLabel(self)
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_stream)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_stream)

        self.capture_button = QPushButton('Capture', self)
        self.capture_button.clicked.connect(self.capture_image)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close_application)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def start_stream(self):
        if not self.timer.isActive():
            self.timer.start(100)  # Update every 100 ms

    def stop_stream(self):
        if self.timer.isActive():
            self.timer.stop()

    def update_frame(self):
        url = f'http://{self.ip_address}/capture'
        response = requests.get(url)
        if response.status_code == 200:
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if frame is not None:
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
                self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def capture_image(self):
        url = f'http://{self.ip_address}/capture'
        response = requests.get(url)
        if response.status_code == 200:
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if frame is not None:
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG Files (*.jpg);;PNG Files (*.png)", options=options)
                if file_name:
                    cv2.imwrite(file_name, frame)
                    QMessageBox.information(self, "Image Saved", "Image has been saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to capture image.")

    def close_application(self):
        self.stop_stream()
        self.close()

if __name__ == '__main__':
    ip_address = '192.168.1.184'  # Replace with your ESP32-CAM's IP address
    app = QApplication(sys.argv)
    ex = CameraApp(ip_address)
    ex.show()
    sys.exit(app.exec_())
