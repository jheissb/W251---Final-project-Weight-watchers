#TODO:
#deserialize the incoming message
#recognize the face 
#get the face id
#save and update the historical data from user historical database
#return the historical data
import paho.mqtt.client as mqtt
import os
import io
import json

REMOTE_MQTT_HOST="44.233.34.126"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_FACE_TOPIC="imagedetection/faceprocessor"
REMOTE_MQTT_BODY_TOPIC="imagedetection/bodyprocessor"


def on_connect_remote(client, userdata, flags, rc):
        print("connected to remote broker with rc: " + str(rc))
        client.subscribe(REMOTE_MQTT_FACE_TOPIC)
        client.subscribe(REMOTE_MQTT_BODY_TOPIC)
	
def on_message(client,userdata,msg):
  try:
    print("message received!")	
    try:
      m_decode=str(msg.payload.decode("utf-8","ignore"))
      payload=json.loads(m_decode)
      # buff = np.fromstring(message.payload, np.uint8)
      # buff = buff.reshape(1, -1)
      if msg.topic == REMOTE_MQTT_FACE_TOPIC:
          return aggregate_face(payload)
      if msg.topic == REMOTE_MQTT_BODY_TOPIC:
          return aggregate_body(payload)
      print('finish aggregator')
    except Exception as e:
      print(str(e))
  except Exception as e:
    print(str(e))

def aggregate_body(msg):
    return None

def aggregate_face(msg):
    return None

remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
remote_mqttclient.on_message = on_message


# go into a loop
remote_mqttclient.loop_forever()