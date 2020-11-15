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

## Image Processor
There are 3 containers running on edge.  
One container would consume image from our webcam  
One container would be the mosquitto broker that control the topic and communication to and from client  
One container would consume the image from webcam and process and send over to our cloud
### Build Docker Image
```sh
#in directory /imageCapture
docker build -t imagecapture -f Dockerfile .

#in directory /imageprocessorbroker
docker build -t imageprocessorbroker -f Dockerfile .

#in directory /imageprocessor
docker build -t bodyprocessor -f Dockerfile .

#in directory /bmi_from_face
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
* for body
```sh
docker run --name processor --network imgProcessor -ti imageprocessor sh
```
after get into the shell:
```sh
python3 image_processor.py
```

* for face
```sh
docker run --name faceprocessor --network imgProcessor -ti faceprocessor sh
```
after get into the shell:
```sh
pytho
```

#### Step 3 - Start image capture with network
```sh
#xhost +
#docker run --name capture --network hw3 --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -ti imagecapture bash
#python3 single_cam.py

docker run --name capture --network imgProcessor -ti imagecapture bash
python3 detect_image.py --model=resnet --image /home/lindayang/Desktop/mids/W251---Final-project-Weight-watchers/imageCapture/image/people_2.jpg
```

## Image Data Saver
There are 2 containers running on cloud.  
One container would consume image message from our remote broker and store the image in our s3 bucket  
One container would be the mosquitto broker that control the topic and communication to and from client  

### Start Image Data Saver 

#### Step 0 -  Create two aws ec2 instance with inbound rule open to all traffic

#### Step 1 - Start broker
```sh
ssh -A ec2-user@PUBLICDNS
```
after get into the shell, start the mosquitto broker:
```sh
docker pull eclipse-mosquitto #(https://hub.docker.com/_/eclipse-mosquitto?tab=description)
docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto
docker exec -it 78f058cc0768 sh # for debug purpose
```

#### Step 2 - Start saver