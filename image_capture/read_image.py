import cv2
import paho.mqtt.client as mqtt
import os
import face_constructor
import body_constructor
import face_recognition
import face_image as fimg
import face_serde
import numpy as np


LOCAL_MQTT_HOST="172.18.0.2"
LOCAL_MQTT_PORT=1883
LOCAL_FACE_MQTT_TOPIC="imagedetection/faceextractor"
LOCAL_BODY_MQTT_TOPIC="imagedetection/bodyextractor"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(LOCAL_FACE_MQTT_TOPIC)
    client.subscribe(LOCAL_BODY_MQTT_TOPIC)

def publish_face(payload):
    client.publish(LOCAL_FACE_MQTT_TOPIC, payload, qos=1, retain=False)

def publish_body(payload):
    client.publish(LOCAL_BODY_MQTT_TOPIC, payload, qos=1, retain=False)

# filelist=os.listdir('image')
# for imagepath in filelist[:]:
#     imagepath = 'image/' + imagepath
#     print(imagepath)
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
            # face_image = face_recognition.load_image_file(face_image_path)
        except RuntimeError:
            print("Could not open the image")
            exit
        face = face_constructor.face_main(face_image)
        if face: 
            print(face.image_id)
            face_str = face.serializer()
            reverted_face_image = fimg.deserializer(face_str)
            print(type(reverted_face_image))
            print(type(np.asarray(reverted_face_image.raw_left_img)))
            left_image_encoding = face_recognition.face_encodings(np.asarray(reverted_face_image.raw_left_img))
            if left_image_encoding:
                print("find new face")
            publish_face(face_str)
            print("Sent detected face image to mosquitto")

    #Test body
    # body_image_path = input("Body image path: ")
    # body_image = None
    # try: 
    #     body_image = cv2.imread(body_image_path)
    # except RuntimeError:
    #     print("Could not open the image")
    #     exit
    # body = body_constructor.body_main(body_image)
    # if body:
    #     publish_body(body)
    #     print("Sent detected body image to mosquitto")

if __name__ == "__main__":
    main()


