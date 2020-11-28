import cv2
import paho.mqtt.client as mqtt
import os
import numpy as np


LOCAL_MQTT_HOST="processorbroker"
LOCAL_MQTT_PORT=1883
LOCAL_FACE_MQTT_TOPIC="imagedetection/faceextractor"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(LOCAL_FACE_MQTT_TOPIC)

def publish_face(payload):
    client.publish(LOCAL_FACE_MQTT_TOPIC, payload, qos=1, retain=False)
    print("Sent detected face image to mosquitto")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)


def main():
    #Test face

    while True:
        face_image_path = input("Face image path: ")
        face_image = None
        try: 
            img = cv2.imread(face_image_path)
            face_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except RuntimeError:
            print("Could not open the image")
            exit
        _,png = cv2.imencode('.png', face_image)
        face_msg = png.tostring()
        publish_face(face_msg)
        # if face: 
        #     print(face.image_id)
        #     face_str = face.serializer()
        #     publish_face(face_str)
            

if __name__ == "__main__":
    main()


