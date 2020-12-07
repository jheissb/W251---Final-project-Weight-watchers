import cv2
import paho.mqtt.client as mqtt
import os
import numpy as np
import json
import uuid
import base64
from sys import getsizeof



REMOTE_MQTT_HOST="44.233.34.126"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC="imagedetection/aggregator"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(REMOTE_MQTT_TOPIC, qos=0)

def on_message(client,userdata,msg):
  try:
    print("message received!")	
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    payload=json.loads(m_decode)
    print(payload)
  except Exception as e:
    print("error in on_message")
    print(str(e))

def publish(payload):
    f = open("output.txt", "a")
    f.write(payload)
    f.close()
    client.publish(REMOTE_MQTT_TOPIC, payload, qos=0, retain=False)
    print("Sent message to mosquitto")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)

def main():
    #Test
    while True:
        face_image_path = input("Face image path: ")
        try: 
            img = cv2.imread(face_image_path)
        except RuntimeError:
            print("Could not open the image")
            exit
        _,png = cv2.imencode('.png', img)
        user_object = {}
        png_as_text = base64.b64encode(png).decode()
        print(type(png_as_text))
        user_object['face-img'] = png_as_text
        user_object['bmi'] = 23.0
        user_object['waist-height-ratio'] = 0.47
        user_object['waist-hip-ratio'] = 0.8
        user_object['keypoints'] = [1,2,3,4,5]
        user_object['body-img'] = png_as_text
        user_object['session-id'] =str(uuid.uuid4())
        print(type(user_object))
        publish(json.dumps(user_object, ensure_ascii=False, indent=4))
            

if __name__ == "__main__":
    main()


