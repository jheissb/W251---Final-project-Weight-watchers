# WAIT WATCHER
wait watcher is using NVDIA Jeston Xavier, USB camera, opencv computer vision library, aws cloud service to detect face and human body through edge, and using machine learning model and and upload to remote through mosquitto, finally the image would get saved in s3 bucket. 

Topic:  
* for edge container communication: 
  * imagedetection/bodyextractor  
  * imagedetection/faceextractor
* for cloud container and edge to cloud communication: 
  * imagedetection/bodyprocessor
  * imagedetection/faceprocessor

QoS:   
* Here, I choosed `at least once (1)`, I assume this is for business that does not worry about object duplication but want guarantee of delivery

## Image Capture & Processor
There are 3 containers running on edge.  
One container would consume image from our webcam  
One container would be the mosquitto broker that control the topic and communication to and from client  
One container would consume the image from webcam and process and send over to our cloud
### Build Docker Image
```sh
#in directory /image_capture
docker build -t imagecapture -f Dockerfile .

#in directory /image_processor_broker
docker build -t imageprocessorbroker -f Dockerfile .

#in directory /face_processor
docker build -t faceprocessor -f Dockerfile .

```
### Start Image Processor

#### Step 0 -  Create network
```sh
docker network create --driver bridge imgProcessor
```

#### Step 1 - Start broker with network
```sh
docker run --name processorbroker --network imgProcessor -p 1883:1883 -ti imageprocessorbroker sh
```
after get into the shell, start the mosquitto broker:
```sh
/usr/sbin/mosquitto
```

#### Step 2 - Start processor with network

* for face
```sh
docker run --name faceprocessor --network imgProcessor -ti faceprocessor sh
```
after get into the shell:
```sh
python3 main.py
```

* for body  

follow this articale to install trt_pose on your jeston: [install jetson](https://spyjetson.blogspot.com/2019/12/jetsonnano-human-pose-estimation-using.html)  

```sh
#in directory /body_processor
python3 body_processor.py
```

#### Step 3 - Start image capture with network
```sh
xhost +
docker run --name capture --network imgProcessor --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -ti imagecapture bash
python3 cam.py #for face
python3 cam_body.py #for body

#for testing purpose
#docker run --name capture --network imgProcessor -ti imagecapture bash
#python3 read_image.py 
```