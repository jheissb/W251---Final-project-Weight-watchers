import cv2
import paho.mqtt.client as mqtt
import os

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

filelist=os.listdir('image')
for imagepath in filelist[:]:
    imagepath = 'image/' + imagepath
    print(imagepath)
    image = cv2.imread(imagepath)
    imagetype = '.' + imagepath.split('.')[-1]
    rc, imgbinary = cv2.imencode(imagetype, image)
    msg = imgbinary.tobytes()
    publish(msg)
    print("Sent detected image to mosquitto")


