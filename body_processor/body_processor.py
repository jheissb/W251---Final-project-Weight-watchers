import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import numpy as np
import cv2
from pose_detector import detect_pose
from body_image import BodyImage
from math import pi
import json

LOCAL_MQTT_HOST="172.18.0.2" 
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
  print("Sent bmi result to mosquitto")

def calculate_ratio(img, keypoints):
  w, h = img.size
  if all(keypoints[1]) and all(keypoints[2]) and all(keypoints[15]) and all(keypoints[16]):
    left_eye_points = np.asarray([round(keypoints[1][2] * w), round(keypoints[1][1] * h)])
    right_eye_points = np.asarray([round(keypoints[2][2] * w), round(keypoints[2][1] * h)])
    left_ankle_points = np.asarray([round(keypoints[15][2] * w), round(keypoints[15][1] * h)])
    right_ankle_points = np.asarray([round(keypoints[16][2] * w), round(keypoints[16][1] * h)])
    left_height = np.linalg.norm(left_ankle_points-left_eye_points)
    right_height = np.linalg.norm(right_ankle_points-right_eye_points)
    avg_height = (left_height + right_height) / 2

    left_hip_points = np.asarray([round(keypoints[11][2] * w), round(keypoints[11][1] * h)])
    right_hip_points = np.asarray([round(keypoints[12][2] * w), round(keypoints[12][1] * h)])
    left_shoulder_points = np.asarray([round(keypoints[5][2] * w), round(keypoints[5][1] * h)])
    right_shoulder_points = np.asarray([round(keypoints[6][2] * w), round(keypoints[6][1] * h)])
    avg_shoulder = np.linalg.norm(right_shoulder_points-left_shoulder_points)
    avg_hip = np.linalg.norm(right_hip_points-left_hip_points)

    avg_waist = pi * (avg_hip+avg_shoulder) / 2
    waist_height_ratio = round((avg_waist/avg_height),4)
    waist_hip_ratio = round((avg_waist/avg_hip),4)
    return (waist_height_ratio,waist_hip_ratio)
  else:
    return (0,0)

def process_message(message):
  buff = np.fromstring(message.payload, np.uint8)
  buff = buff.reshape(1, -1)
  img = cv2.imdecode(buff, cv2.COLOR_BGR2RGB)
  orgimg, keypoints, processed_img = detect_pose(img)
  if keypoints:
    waist_height_ratio,waist_hip_ratio  = calculate_ratio(orgimg, keypoints[0])
  body_image = {}
  _,png = cv2.imencode('.png', processed_img)
  body_image['waist-hip-ratio'] = waist_hip_ratio
  body_image['waist-height-ratio'] = waist_height_ratio
  body_image['keypoints'] = keypoints
  print(body_image['keypoints'])
  publish_result(json.dumps(body_image, ensure_ascii=False, indent=4))

mqttclient = mqtt.Client()
mqttclient.on_connect = on_connect
mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
mqttclient.on_message = on_message

# go into a loop
mqttclient.loop_forever()