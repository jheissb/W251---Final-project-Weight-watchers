import cv2
import paho.mqtt.client as mqtt
import os
import numpy as np
import json
import uuid


REMOTE_MQTT_HOST="44.233.34.126"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC="imagedetection/aggregator"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(REMOTE_MQTT_TOPIC)

def publish(payload):
    client.publish(REMOTE_MQTT_TOPIC, payload, qos=1, retain=False)
    print("Sent message to mosquitto")

client = mqtt.Client()
client.on_connect = on_connect
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
        face_msg = png.tostring()
        user_object['bmi'] = 23.0
        user_object['face-img'] = face_msg
        user_object['wait-height-ratio'] = 0.47
        user_object['keypoints'] = [1,2,3,4,5]
        user_object['body-img'] = face_msg
        user_object['session-id'] =str(uuid.uuid4())
        publish(json.dumps(user_object))
            

if __name__ == "__main__":
    main()


