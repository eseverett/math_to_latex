import sys
import os
import time

import cv2

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap

class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Mathematica to Latex Conversion")
        self.setGeometry(100, 100, 800, 600)

        # Set the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Setup the camera
        self.capture = cv2.VideoCapture(0)
        self.current_frame = None

        # Create a label to display the camera feed
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # setup timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()

        # create button layout
        self.button_layout = QHBoxLayout()

        self.button_take_image = QPushButton("Take Image")
        self.button_import_image = QPushButton("Import Image")
        self.button_save_image = QPushButton("Save Image")
        self.button_convert_image = QPushButton("Convert Image")
        self.button_retry = QPushButton("Take New Image")

        self.addToLayout()
        self.setupButtonMethods()

    def update_frame(self):
        """
        This function captures a frame from the camera and updates the label with the new image.
        """

        # Capture a frame from the camera
        ret, frame = self.capture.read()
        if not ret: return

        # Store the current frame
        self.current_frame = frame.copy()

        # Convert the frame to RGB format
        rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb.shape


        # Create a QImage from the frame
        bytes_per_line = channel * width
        q_image = QImage(rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

        self.label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        """
        This function is called when the window is closed. It releases the camera and stops the timer.
        """
        self.capture.release()
        self.timer.stop()
        super().closeEvent(event)

    def addToLayout(self):
        """
        This function adds elements to the layout.
        """
        # Add the label to the layout
        self.layout.addWidget(self.label)
        
        # Add the buttons to the layout
        self.button_layout.addWidget(self.button_take_image)
        self.button_layout.addWidget(self.button_retry)
        self.button_layout.addWidget(self.button_save_image)
        self.button_layout.addWidget(self.button_import_image)
        self.button_layout.addWidget(self.button_convert_image)
        self.layout.addLayout(self.button_layout)


    def setupButtonMethods(self):
        """
        This function sets up the button methods for the UI.
        """

        # Connect the buttons to their respective methods
        self.button_take_image.clicked.connect(self.take_image)
        self.button_import_image.clicked.connect(self.import_image)
        self.button_save_image.clicked.connect(self.save_image)
        self.button_convert_image.clicked.connect(self.convert_image)
        self.button_retry.clicked.connect(self.take_new_image)

    def take_image(self):
        """
        This function captures an image by freezing the current frame from the camera.
        """

        # Capture a frame from the camera
        if self.current_frame is None: return

        self.timer.stop()

    def import_image(self):
        """
        This function imports an image from the file system.
        """
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not path: return
        frame = cv2.imread(path)

        if frame is None: return
        self.current_frame = frame.copy()
        
                # Store the current frame
        self.current_frame = frame.copy()

        # Convert the frame to RGB format
        rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb.shape


        # Create a QImage from the frame
        bytes_per_line = channel * width
        q_image = QImage(rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

        self.label.setPixmap(QPixmap.fromImage(q_image))

        self.timer.stop()

    def save_image(self):
        """
        Save the currently displayed frame.
        """

        if self.current_frame is None: return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG (*.png);;JPEG (*.jpg)"
        )

        if not path: return
        cv2.imwrite(path, self.current_frame)

    def take_new_image(self):
        """
        This function resets the camera and starts capturing again.
        """

        self.timer.start()

    def convert_image(self):
        """
        Placeholder for OCR -> LaTeX routine.
        """

        if self.current_frame is None: return
        # TODO: plug in your conversion pipeline here
        print("Running LaTeX conversion on current image...")