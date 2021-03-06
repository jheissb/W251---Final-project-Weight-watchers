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
import base64
import cv2
import numpy as np
from face_recoginitor import recognit_face
from s3util import get_and_insurpt_user_data, retrive_user_hitstorical_data_by_face_id

REMOTE_MQTT_HOST="44.233.34.126"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC="imagedetection/aggregator"
REMOTE_MQTT_HITORICAL_DATA="imagedetection/historicaldata"


def on_connect_remote(client, userdata, flags, rc):
  print("connected to remote broker with rc: " + str(rc))
  client.subscribe(REMOTE_MQTT_TOPIC, qos=0)
	
def on_message(client,userdata,msg):
  print("message received!")	
  try:
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    payload=json.loads(m_decode)
    aggregate_object(payload)
    print('finish aggregator')
  except Exception as e:
    print("error in on_message")
    print(str(e))
  
def publish_result(payload):
  remote_mqttclient.publish(REMOTE_MQTT_HITORICAL_DATA, payload, qos=0, retain=False)
  print("Sent historical result to mosquitto")

def aggregate_object(user_object):
  face_img_string = user_object['face-img']
  img_original = base64.b64decode(face_img_string)
  img_as_np = np.frombuffer(img_original, dtype=np.uint8)
  # img = cv2.imdecode(img_as_np, flags=1)
  face_id = recognit_face(img_as_np)
  print("got face id, start updating db")
  get_and_insurpt_user_data(user_object, face_id)
  historical_data = {}
  print("finished updating, start getting historical data")
  historical_data['history'] = retrive_user_hitstorical_data_by_face_id(face_id)
  historical_data['session-id'] = user_object['session-id']
  publish_result(json.dumps(historical_data, ensure_ascii=False, indent=4))


remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
remote_mqttclient.on_message = on_message


# go into a loop
remote_mqttclient.loop_forever()