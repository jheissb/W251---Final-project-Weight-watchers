import paho.mqtt.client as mqtt
import os
import json
import uuid
import base64
import numpy as np
import cv2

LOCAL_MQTT_HOST="172.18.0.2"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_RESULT_TOPIC="imagedetection/bodyprocessor/result"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(LOCAL_MQTT_RESULT_TOPIC, qos=0)

def on_message(client,userdata,msg):
  try:
    print("message received!")	
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    payload=json.loads(m_decode)
    display_image(payload)
    print(payload)
  except Exception as e:
    print("error in on_message")
    print(str(e))

def display_image(payload):
  print("start process image")
  face_img_string = payload['body-img']
  img_original = base64.b64decode(face_img_string)
  img_as_np = np.frombuffer(img_original, dtype=np.uint8)
  new_img = cv2.imdecode(img_as_np, cv2.COLOR_BGR2RGB)  
  print("finished decode")
  cv2.imshow('frame', new_img)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

# go into a loop
client.loop_forever()