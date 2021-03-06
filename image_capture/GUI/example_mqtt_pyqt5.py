#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Test Bulb thermometer drawn with pyqt 5.

Temperature received by MQTT from remote sensor

Author: Barry Hay

Last edited: June 2018
"""

from PyQt5 import QtGui, QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import QWidget, QApplication

from PyQt5.QtGui import QPainter, QColor # , QBrush, QPen

from PyQt5.QtCore import Qt

import paho.mqtt.client as mqtt  #import the client1

#import time
import datetime
import uuid
import sys

#global client
degc = ''
topl=200
topr=200
highl=10
highr=10
lefttemp = 20
righttemp = 25

channel = ['AQUAP/AIR', 'AQUAP/WATER']
mqttNode = "Surface" + hex(uuid.getnode())[-6:]
print(mqttNode)

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


class AQUAMONITOR(QWidget):
    client_message = QtCore.pyqtSignal(object)
    
    def __init__(self, mqtt_client):
        super(AQUAMONITOR, self).__init__()
        self._client = mqtt_client

        self.initUI()
        
        
    def initUI(self):      

        self.setGeometry(100, 100, 320, 240)
        self.setWindowTitle('Brushes')
        self._client.on_connect = self.on_connect
        self._client.on_message = lambda c, d, msg: self.client_message.emit(msg)
        self.client_message.connect(self.on_client_message)

    def paintEvent(self, e):

        global qp
        qp = QPainter(self)
        qp.begin(self)

        self.drawTherm(qp)
        qp.end()

    def drawTherm(self,qp):
        
        col = QColor(0, 0, 0)
#        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        qp.setBrush(QColor(200, 0, 0))
        qp.drawEllipse(145, 200, 40, 40)
        qp.drawLine(155, 80, 155, 202)
        qp.drawLine(175, 80, 175, 202)
        qp.setPen(Qt.NoPen)
        
        print("finish bulb")

#        self.leftbulb( lcel)
        self.rightbulb( 12)
#
    def leftbulb(self,  lcel):
        print("start leftbulb")
        topl = 80 + (40-lcel)*3
        highl = lcel*3 + 5
        qp.setBrush(QColor(200, 0, 0))
        qp.save()
        qp.drawRect(156,topl,10,highl)
        qp.restore()
        print("topl", topl)
        print("highl",highl)
        qp.repaint()

    def rightbulb(self, rcel):
        print("start rightbulb")
        topr = 80 + (40-rcel)*3
        highr = rcel*3 + 5   
        qp.setBrush(QColor(200, 0, 0))
        qp.save()
        qp.drawRect(166,topr,9,highr)
        qp.restore()

    def on_client_message(self, message):
        print("message received")
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)
        print(datetime.datetime.now().strftime("%H:%M:%S"))
        yy = channel.index(message.topic)
        print("index = ", yy)

        print(message.payload)
        #        payld = message.payload + 1
        payld = int(message.payload)
        print(payld)

        if yy == 0:
            print("left temp", payld)
            self.leftbulb( payld)


        if yy == 1:
            topr = 100 + (40 - payld) * 3
            highr = payld * 3 + 5

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        #        client.subscribe("INSIDE/TEMP")
        for z in range(2):
            client.subscribe(channel[z])
        print("subscribed")

        
if __name__ == "__main__":

    client = mqtt.Client(mqttNode)
    print("Start Setup")
        # hook events
    app = QApplication(sys.argv)
    mainWindow = AQUAMONITOR(client)
    mainWindow.show()

    print("Print  start connect")
    client.connect("192.168.1.113")
    client.loop_start()

    try:
        sys.exit(app.exec_())
    finally:
        client.loop_stop()
