import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import numpy as np
import cv2
from pose_detector import detect_pose
from body_image import BodyImage

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
    avg_hip = np.linalg.norm(right_hip_points-left_hip_points)

    return round((avg_hip/avg_height),4)



def process_message(message):
  buff = np.fromstring(message.payload, np.uint8)
  buff = buff.reshape(1, -1)
  img = cv2.imdecode(buff, cv2.COLOR_BGR2RGB)
  orgimg, keypoints = detect_pose(img)
  ratio = calculate_ratio(orgimg, keypoints[0])
  body_image = BodyImage(orgimg, ratio)
  print(body_image.ratio)
  publish_result(keypoints)

mqttclient = mqtt.Client()
mqttclient.on_connect = on_connect
mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
mqttclient.on_message = on_message

# go into a loop
mqttclient.loop_forever()