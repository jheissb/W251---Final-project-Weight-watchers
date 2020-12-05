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
from face_recoginitor import recognit_face
from s3util import get_and_insurpt_user_data, retrive_user_hitstorical_data_by_face_id

REMOTE_MQTT_HOST="44.233.34.126"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC="imagedetection/aggregator"
REMOTE_MQTT_HITORICAL_DATA="imagedetection/historicaldata"


def on_connect_remote(client, userdata, flags, rc):
  print("connected to remote broker with rc: " + str(rc))
  client.subscribe(REMOTE_MQTT_TOPIC)
	
def on_message(client,userdata,msg):
  try:
    print("message received!")	
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    payload=json.loads(m_decode)
    # buff = np.fromstring(message.payload, np.uint8)
    # buff = buff.reshape(1, -1)
    aggregate_object(payload)
    print('finish aggregator')
  except Exception as e:
    print(str(e))
  
def publish_result(payload):
  remote_mqttclient.publish(REMOTE_MQTT_HITORICAL_DATA, payload, qos=1, retain=False)
  print("Sent historical result to mosquitto")

def aggregate_object(user_object):
  face_id = recognit_face(user_object['face-img'])
  get_and_insurpt_user_data(user_object, face_id)
  historical_data = {}
  historical_data['history'] = retrive_user_hitstorical_data_by_face_id(face_id)
  historical_data['session-id'] = user_object['session-id']
  print(historical_data)
  publish_result(historical_data)


remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
remote_mqttclient.on_message = on_message


# go into a loop
remote_mqttclient.loop_forever()