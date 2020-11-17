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
import face_validator
import pose_detector
import paho.mqtt.client as mqtt
from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
d4 = now.strftime("%d_%m_%H_%M_%S")
# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of each camera pane in the window on the screen

left_camera = None
right_camera = None


LOCAL_MQTT_HOST="processorbroker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="imagedetection/extractor"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)

def publish(payload):
    client.publish(LOCAL_MQTT_TOPIC, payload, qos=1, retain=False)

client = mqtt.Client()
client.on_connect = on_connect
client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

class CSI_Camera:

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


    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(
                gstreamer_pipeline_string, cv2.CAP_GSTREAMER
            )
            
        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)
            return
        # Grab the first frame to start the video capturing
        self.grabbed, self.frame = self.video_capture.read()

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


# Currently there are setting frame rate on CSI Camera on Nano through gstreamer
# Here we directly select sensor_mode 3 (1280x720, 59.9999 fps)
def gstreamer_pipeline(
    sensor_id=0,
    sensor_mode=3,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=15,
    flip_method=2,
):
    return (
        "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            sensor_mode,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def start_cameras():
    left_camera = CSI_Camera()
    left_camera.open(
        gstreamer_pipeline(
            sensor_id=0,
            sensor_mode=3,
            flip_method=2,
            display_height=720,
            display_width=1280,
        )
    )
    left_camera.start()

    right_camera = CSI_Camera()
    right_camera.open(
        gstreamer_pipeline(
            sensor_id=1,
            sensor_mode=3,
            flip_method=2,
            display_height=720,
            display_width=1280,
        )
    )
    right_camera.start()

    cv2.namedWindow("CSI Cameras", cv2.WINDOW_AUTOSIZE)

    if (
        not left_camera.video_capture.isOpened()
        or not right_camera.video_capture.isOpened()
    ):
        # Cameras did not open, or no camera attached

        print("Unable to open any cameras")
        # TODO: Proper Cleanup
        SystemExit(0)
    i=0	
    #frame_width = int(2*960)
    #frame_height = 540
    #size = (frame_width, frame_height) 
   
    # Below VideoWriter object will create 
    # a frame of above defined The output  
    # is stored in 'filename.avi' file. 
    #result = cv2.VideoWriter('stereo_test.avi',  
    #                     cv2.VideoWriter_fourcc(*'MJPG'), 
    #                     10, size) 
    while cv2.getWindowProperty("CSI Cameras", 0) >= 0 :
        _ , left_image=left_camera.read()
        _ , right_image=right_camera.read()
        camera_images = np.hstack((left_image, right_image))
        #cv2.imshow("CSI Cameras", camera_images)
        #saving:
        #result.write(camera_images)
        filename = 'training_set/'+d4+'train_img'+str(i)+'.png'
        #filename ='maya'+str(i)+'.png'
        # Using cv2.imwrite() method 
        # Saving the image 
        #output = np.clip(camera_images * 255, 0, 255) # proper [0..255] range
        cv2.imshow("CSI Cameras", camera_images)
        #output = output.astype('uint8')  # safe conversion
        cv2.waitKey(0) & 0xFF
        r=cv2.imwrite(filename,camera_images)
        print(filename,'\n',r)
        i+=1  
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

def convert_to_binary():
        image = cv2.imread(imagepath)
        imagetype = '.' + imagepath.split('.')[-1]
        rc, imgbinary = cv2.imencode(imagetype, image)
        msg = imgbinary.tobytes()

if __name__ == "__main__":
    start_cameras()