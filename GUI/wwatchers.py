from mplwidget import MplWidget
from wwgui import *
import sys
import cv2
import numpy as np
import threading
import time
import queue

from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

class MyForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        self.title='Weight Watchers console'
        # #Load the UI Page
        # uic.loadUi('acquire_images_gui.ui', self)
        self.ui.take_face_picture_btn.clicked.connect(self.take_face_picture)
        self.ui.retake_face_picture_btn.clicked.connect(self.retake_face_picture)
        self.ui.take_body_picture_btn.clicked.connect(self.take_body_picture)
        self.ui.retake_body_picture_btn.clicked.connect(self.retake_body_picture)
        self.ui.submit_btn.clicked.connect(self.submit_data)
        self.face_size=self.ui.face.size()
        self.stream_face=True
        self.stream_body=False
        self.image_face=[]
        self.image_body=[]
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.show_cam)
        # set control_bt callback clicked  function
        self.controlTimer()

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(2)
            # start timer
            self.timer.start(20)
            # update text
            self.ui.text_output.setText("press Take Picture")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update text
            self.ui.text_output.setText("Start")
    def show_cam(self):
        if self.stream_face:
            self.show_face_cam()
        elif self.stream_body:
            self.show_body_cam()

    def take_body_picture(self):
        self.stream_body=False
        self.image_body=self.imagebo

    def retake_body_picture(self):
        self.stream_body=True
        self.image_body=[]
        self.stream_face=False

    def submit_data(self):
        self.cap.release()

    def take_face_picture(self):
        """takes picture of face from webcam:
        fixes the frame in current and stop steaming on the face canvas"""
        self.stream_face=False
        if len(self.image_body)<1:
            self.stream_body=True
        self.ui.text_output.setText('body:'+str(self.stream_body))
        self.image_face=self.imageo

    def retake_face_picture(self):
        self.stream_face=True
        self.image_face=None
        self.show_face_cam()

    def show_face_cam(self):
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #store current image object
        self.imageo=image
        height, width, channel = image.shape
        ratio=self.ui.face.geometry().width()/width
        image = cv2.resize(image, (self.ui.face.geometry().width(), int(height*ratio)))
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create and store QImage from image
        self.qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.face.setPixmap(QPixmap.fromImage(self.qImg))
            
            
    def show_body_cam(self):
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #store current image object
        self.imagebo=image
        height, width, channel = image.shape
        ratio=self.ui.label_3.geometry().height()/height
        image = cv2.resize(image, (int(width*ratio), self.ui.face.geometry().height()))
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create and store QImage from image
        self.qImgb = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.label_3.setPixmap(QPixmap.fromImage(self.qImgb))
            
            
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()