# this is from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import numpy as np
import cv2
import paho.mqtt.client as mqtt

# the index depends on your camera setup and which one is your USB camera.
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')

LOCAL_MQTT_HOST="imageprocessorbroker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="imageprocessor/captured"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)

def publish(payload):
    client.publish(LOCAL_MQTT_TOPIC, payload, qos=1, retain=False)

client = mqtt.Client()
client.on_connect = on_connect
client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

#client.loop_forever()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
	# your logic goes here; for instance
	# cut out face from the frame.. 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        rc,png = cv2.imencode('.png', frame)
        msg = png.tobytes()
        publish(msg)
        print("Sent detected face to mosquitto")
	# ...
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
