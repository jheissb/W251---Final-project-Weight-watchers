import paho.mqtt.client as mqtt
import os
import json
import uuid
import base64

REMOTE_MQTT_HOST="44.233.34.126"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_HITORICAL_DATA="imagedetection/historicaldata"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(REMOTE_MQTT_HITORICAL_DATA)

def on_message(client,userdata,msg):
  try:
    print("message received!")	
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    payload=json.loads(m_decode)
    print(payload)
  except Exception as e:
    print("error in on_message")
    print(str(e))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)

# go into a loop
client.loop_forever()