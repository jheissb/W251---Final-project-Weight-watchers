# MIT License
# Copyright (c) 2019,2020 JetsonHacks
# See license
# A very simple code snippet
# Using two  CSI cameras (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit (Rev B01) using OpenCV
# Drivers for the camera and OpenCV are included in the base image in JetPack 4.3+

# This script will open a window and place the camera stream from each camera in a window
# arranged horizontally.
# The camera streams are each read in their own thread, as when done sequentially there
# is a noticeable lag
# For better performance, the next step would be to experiment with having the window display
# in a separate thread

import cv2
import threading
import numpy as np
import paho.mqtt.client as mqtt

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of each camera pane in the window on the screen

left_camera = None
right_camera = None
mqtt_client = None
LOCAL_MQTT_HOST="ImageProcessorBroker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="imageProcessor/captured"


class STEREO_Camera:

    def __init__ (self) :
        # Initialize instance variables
        # OpenCV video capture element
        self.video_capture = None
        # The last captured image from the camera
        self.frame = None
        self.grabbed = False
        # The thread where the video capture runs
        self.read_thread = None
        self.read_lock = threading.Lock()
        self.running = False

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        # create a thread to read the camera image
        if self.video_capture != None:
            self.running=True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def open(self, camera_index):
        try:
            self.video_capture = cv2.VideoCapture(camera_index)
            
        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            return
        # Grab the first frame to start the video capturing
        self.grabbed, self.frame = self.video_capture.read()


    def stop(self):
        self.running=False
        self.read_thread.join()

    def updateCamera(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed=grabbed
                    self.frame=frame
            except RuntimeError:
                print("Could not read image from camera")
        # FIX ME - stop and cleanup thread
        # Something bad happened
        
    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed=self.grabbed
        return grabbed, frame

    def release(self):
        if self.video_capture != None:
            self.video_capture.release()
            self.video_capture = None
        # Now kill the thread
        if self.read_thread != None:
            self.read_thread.join()

class MQTT_Sender:
    client = None

    def __init__ (self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(LOCAL_MQTT_TOPIC)

    def publish(self, payload):
        self.client.publish(LOCAL_MQTT_TOPIC, payload, qos=1, retain=False)


def init_mqtt_client():
    mqtt_client = MQTT_Sender()

def start_cameras():
    left_camera = STEREO_Camera()

    left_camera.open(0)
    
    left_camera.start()

    right_camera = STEREO_Camera()

    right_camera.open(1)
    
    right_camera.start()

    cv2.namedWindow("STEREO Cameras", cv2.WINDOW_AUTOSIZE)

    if (
        not left_camera.video_capture.isOpened()
        or not right_camera.video_capture.isOpened()
    ):
        # Cameras did not open, or no camera attached

        print("Unable to open any cameras")
        # TODO: Proper Cleanup
        SystemExit(0)

    while cv2.getWindowProperty("STEREO Cameras", 0) >= 0 :
        
        _ , left_image=left_camera.read()
        _ , right_image=right_camera.read()
        camera_images = np.hstack((left_image, right_image))
        # _ ,png = cv2.imencode('.png', camera_images)
        # msg = png.tobytes()
        # mqtt_client.publish(msg)
        # print("Sent detected face to mosquitto")

        cv2.imshow("STEREO Cameras", right_image)

        # This also acts as
        keyCode = cv2.waitKey(30) & 0xFF
        # Stop the program on the ESC key
        if keyCode == 27:
            break

    left_camera.stop()
    left_camera.release()
    right_camera.stop()
    right_camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # init_mqtt_client()
    start_cameras()
