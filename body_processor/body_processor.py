import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import numpy as np
import cv2
from pose_detector import detect_pose
from math import pi
import json
import uuid
from datetime import datetime
import os 

class BodyImage(object):
    def __init__(self, raw_img, processed_img, ratio):
        self.raw_img = raw_img
        self.processed_img = processed_img
        self.image_id = str(uuid.uuid4())
        self.timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        self.ratio = ratio
        #need to add timestamp

    def serializer(self):
        print("get called")
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

LOCAL_MQTT_HOST=os.getenv('local_broker_ip', "172.18.0.2")
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="imagedetection/bodyextractor"
LOCAL_MQTT_RESULT_TOPIC="imagedetection/bodyprocessor/result"

def on_connect(client, userdata, flags, rc):
  print("connected to  broker with rc: " + str(rc))
  client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata, msg):
  print("message received!")	
  process_message(msg)
    

def publish_result(payload):
  mqttclient.publish(LOCAL_MQTT_RESULT_TOPIC, payload, qos=1, retain=False)
  print("Sent body position result to mosquitto")

def calculate_ratio(img, keypoints):
  w, h = img.size
  if all(keypoints[1]) and all(keypoints[2]) and all(keypoints[15]) and all(keypoints[16]):
    left_eye_points = np.asarray([round(keypoints[1][2] * w), round(keypoints[1][1] * h)])
    right_eye_points = np.asarray([round(keypoints[2][2] * w), round(keypoints[2][1] * h)])
    left_ankle_points = np.asarray([round(keypoints[15][2] * w), round(keypoints[15][1] * h)])
    right_ankle_points = np.asarray([round(keypoints[16][2] * w), round(keypoints[16][1] * h)])
    left_height = np.linalg.norm(left_ankle_points-left_eye_points)
    right_height = np.linalg.norm(right_ankle_points-right_eye_points)
    avg_height = 1.1*(left_height + right_height) / 2 #add 10% to compensate for eyes and ankles not been at the top and bottom.
    left_hip_points = np.asarray([round(keypoints[11][2] * w), round(keypoints[11][1] * h)])
    right_hip_points = np.asarray([round(keypoints[12][2] * w), round(keypoints[12][1] * h)])  
    left_shoulder_points = np.asarray([round(keypoints[5][2] * w), round(keypoints[5][1] * h)])
    right_shoulder_points = np.asarray([round(keypoints[6][2] * w), round(keypoints[6][1] * h)])
    #estimating waist as midpoint between hip and shoulder
    left_waist_points =(2*left_hip_points+left_shoulder_points)/3
    right_waist_points =(2*right_hip_points+right_shoulder_points)/3
    #avg_shoulder = np.linalg.norm(right_shoulder_points-left_shoulder_points)
    avg_hip = np.linalg.norm(right_hip_points-left_hip_points)
    avg_waist = np.linalg.norm(right_hip_points-left_hip_points)
    waist_height_ratio = round((pi*avg_waist/avg_height),4)
    waist_hip_ratio = round((avg_waist/avg_hip),4)
    return (waist_height_ratio,waist_hip_ratio,list(left_eye_points),list(right_eye_points),list(left_ankle_points),
        list(right_ankle_points),list(left_hip_points),list(right_hip_points),list(left_waist_points),list(right_waist_points))
  else:
    return None

def process_message(message):
  buff = np.fromstring(message.payload, np.uint8)
  buff = buff.reshape(1, -1)
  img = cv2.imdecode(buff, cv2.COLOR_BGR2RGB)
  orgimg, keypoints, processed_img = detect_pose(img)
  if keypoints:
    ratios_and_points  = calculate_ratio(orgimg, keypoints[0])
  body_image = {}
  #print('calculations:',ratios_and_points)
  #_,png = cv2.imencode('.png', processed_img)
  body_image['waist-hip-ratio'] = ratios_and_points[0]
  body_image['waist-height-ratio'] = ratios_and_points[1]
  body_image['keypoints'] = ratios_and_points[2:]
  
  #print('output:',body_image)
  publish_result(json.dumps(body_image, cls=NpEncoder))

mqttclient = mqtt.Client()
mqttclient.on_connect = on_connect
mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
mqttclient.on_message = on_message

# go into a loop
mqttclient.loop_forever()
