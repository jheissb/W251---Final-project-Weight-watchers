import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

LOCAL_MQTT_HOST="forwarderbroker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="facedetection/extractor"

REMOTE_MQTT_HOST="REPLACE_ME" # e.g: ec2-34-221-136-56.us-west-2.compute.amazonaws.com
REMOTE_MQTT_TOPIC="facedetection/processor"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  try:
    print("message received!")	
    # if we wanted to re-publish this message, something like this should work
    msg = msg.payload 
    # publish.single(REMOTE_MQTT_TOPIC, payload=msg, qos=1, retain=False, hostname=REMOTE_MQTT_HOST)
  except:
    print("Unexpected error:", sys.exc_info()[0])

#Local Broker Set Up
local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()