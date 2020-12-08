#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" wwtchers.py opens a GUI to interact with user. 
Face and body pictures are taken and messages are sent to the respective containers for BMI and pose estimation. If detection is OK, data is sent to the cloud for face recognition and historic data is returned. The new data is appended to the database in S3. Program loops every 20 ms cheking if new frames need to be displayed and messages need to be sent"""

from mplwidget import MplWidget
from wwgui import *
import sys
import cv2
import numpy as np
import threading
import time
import queue
import paho.mqtt.client as mqtt
import os
import json
import PIL.Image, PIL.ImageDraw

from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
#set this to the right camera input
CAM_INPUT=0
#Constants
LOCAL_MQTT_HOST="imageprocessorbroker"
LOCAL_MQTT_PORT=1883
#Face and Body images
LOCAL_FACE_MQTT_TOPIC="imagedetection/faceextractor"
LOCAL_BODY_MQTT_TOPIC="imagedetection/bodyextractor"
#BMI and ratios
LOCAL_MQTT_FACE_RESULT_TOPIC="imagedetection/faceprocessor/result"
LOCAL_MQTT_BODY_RESULT_TOPIC="imagedetection/bodyprocessor/result"

#Cloud
REMOTE_MQTT_HOST="44.233.34.126"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC="imagedetection/aggregator"
REMOTE_MQTT_HITORICAL_DATA="imagedetection/historicaldata"
def draw_point(x,y,img):
    thickness = 5
    height, width, channel = img.shape
    #draw = PIL.ImageDraw.Draw(img)
    #draw.line([ int(x)-1,int(y),int(x)+1,int(y)],width = thickness,fill=(51,51,204))
    for xi in range (thickness):
        for yi in range (thickness):
            img[int(x)-xi+2,int(y)-yi+2]=200
    img[int(x)-1,int(y)]=0
    img[int(x)+1,int(y)]=0
    img[int(x),int(y)]=0
    img[int(x),int(y)-1]=0
    img[int(x),int(y)+1]=0    
    return(img)
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
        self.ui.quit_btn.clicked.connect(self.quitf)
        self.face_size=self.ui.face.size()
        self.stream_face=True
        self.stream_body=False
        self.image_face=[]
        self.image_body=[]
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
        self.client.on_message = self.on_message
        self.BMI=0        
        self.client.loop_start()
        
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.show_cam)
        # set control_bt callback clicked  function
        self.controlTimer()

    def quitf(self):
        self.client.loop_stop()
        #self.timer.stop()
        self.controlTimer()
        self.close()

    




    def on_connect(self,client, userdata, flags, rc):
        #subscribe to topics 
        print("Connected with result code "+str(rc))
        self.client.subscribe(LOCAL_MQTT_FACE_RESULT_TOPIC)
        self.client.subscribe(LOCAL_MQTT_BODY_RESULT_TOPIC)
        self.client.subscribe(REMOTE_MQTT_HITORICAL_DATA)

    def on_disconnect(self,client, userdata,rc=0):
        self.client.loop_stop()
    def publish_face(self,payload):
        self.client.publish(LOCAL_FACE_MQTT_TOPIC, payload, qos=1, retain=False)
    def publish_body(self,payload):
        self.client.publish(LOCAL_BODY_MQTT_TOPIC, payload, qos=1, retain=False)

    def on_message(self,client,userdata, msg):
        if msg.topic == REMOTE_MQTT_HITORICAL_DATA: 
            self.process_historical_data(msg.payload)
        if msg.topic == LOCAL_MQTT_FACE_RESULT_TOPIC: 
            BMI=msg.payload.decode("utf-8") #.decode("ascii")
            BMI=BMI[0:5]            
            #print('bmi message=',BMI)
            self.ui.bmi_tag.setText('BMI= '+BMI)
            self.BMI=float(BMI)
        if msg.topic == LOCAL_MQTT_BODY_RESULT_TOPIC: 
            #try:
            m_decode=str(msg.payload.decode("utf-8"))
            pose=json.loads(m_decode)
            print(pose)
            self.process_body_results(pose)
            #except Exception as e:
            #    print("error in on_message")
            #    print(str(e))                    
           
    def process_body_results(self,msg):
        self.w2height_ratio=float(msg['waist-height-ratio'])
        self.w2hip_ratio=float(msg['waist-hip-ratio'])
        self.ui.w2height_label.setText('Waist-to-height ratio:'+str(self.w2height_ratio))
        self.ui.w2hip_label.setText('Waist-to-hip ratio:'+str(self.w2hip_ratio))
        for p in msg['keypoints']:
            self.image_body=draw_point(p[1],p[0],self.image_body)
        height, width, channel = self.image_body.shape
        ratio=self.ui.label_3.geometry().height()/height
        image = cv2.resize(self.image_body, (int(width*ratio), self.ui.face.geometry().height()))
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create and store QImage from image
        self.qImgb = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.label_3.setPixmap(QPixmap.fromImage(self.qImgb))
        self.ui.text_output.setText("Press submit data/n or retake pictures ")

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(CAM_INPUT)
            ret, image = self.cap.read()
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
            self.ui.text_output.setText("Good bye")
    def show_cam(self):
        if self.stream_face:
            self.show_face_cam()
        elif self.stream_body:
            self.show_body_cam()
    
    def take_body_picture(self):
        if self.ui.delay.isChecked():
            for i in range(150):
                self.show_body_cam()
                time.sleep(0.01)
                QtWidgets.QApplication.processEvents() 
        self.image_body=self.imagebo
        self.ui.text_output.setText('Sending body image')
        self.image_face=self.imageo
        #send message to ratio estimator and read incoming ratios
        rc,png = cv2.imencode('.png', self.image_body)
        msg = png.tostring()
        self.publish_body(msg)
        print("Sent detected body to mosquitto")
        self.client.on_message = self.on_message
        self.stream_body=False
 

    def retake_body_picture(self):
        self.stream_body=True
        self.image_body=[]
        self.stream_face=False
        self.ui.text_output.setText("Take body picture")

    #def on_message(self,client,userdata, msg):
    #    self.BMI=msg

    def submit_data(self):
        #send messages to cloud
        self.client.loop_stop()   

    def take_face_picture(self):
        """takes picture of face from webcam:
        fixes the frame in current and stop streaming on the face canvas"""
        self.stream_face=False
        if len(self.image_body)<1:
            self.stream_body=True
        self.ui.text_output.setText('body:'+str(self.stream_body))
        self.image_face=self.imageo
        #send message to BMI estimator and read BMI
        rc,png = cv2.imencode('.png', self.image_face)
        msg = png.tostring()
        self.publish_face(msg)
        print("Sent detected face to mosquitto")
        self.client.on_message = self.on_message

    def retake_face_picture(self):
        self.stream_face=True
        self.image_face=None
        self.ui.text_output.setText("Take face picture")
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
        print(type(image))
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
        imagec = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #store current image object
        self.imagebo=imagec
        height, width, channel = imagec.shape
        ratio=self.ui.label_3.geometry().height()/height
        image = cv2.resize(imagec, (int(width*ratio), self.ui.face.geometry().height()))
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create and store QImage from image
        self.qImgb = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.label_3.setPixmap(QPixmap.fromImage(self.qImgb))
        self.ui.text_output.setText("Take face and body picture then submit data ")
            
            
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
