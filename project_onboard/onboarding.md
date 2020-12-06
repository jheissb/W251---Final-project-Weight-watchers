# WEIGHT WATCHER
Weight watcher is a system for long term monitoring of weight and obesity risk. It runs two local machine learning models to estimate Body Mass Index (MBI) from face images and detects anatomical points and hip to waist and waist to height ratios, which are relevant metrics to predict obesity risk. The system uses NVDIA Jeston Xavier NX and a USB camera at the edge and AWS cloud services. In adition to the local ML models, a third model for face recognition runs in the cloud to identify if a subject has been recorded previously and report historical data from a subject, wich is stored in a S3 bucket. A GUI allows acquisition of face and full body images which are sent to these 3 ML models as a message using MQTT protocol, and in turn each model returns also a message with the BMI estimation, identification of anatomical points and ratios and historical data of the subject, which are displayed by the GUI.

The system can be easily scalable as each edge device perform most of the work independently and the database manager that runs in the cloud can handle messages coming from different devices (for example to asses the eficacy of nutrition policies in all schools within a district or state). Other use case (with some modifications) is to anonimously determine BMI of clients in supermarkets and clothing stores to adjust inventory accordingly.

Topic:  
* for edge container communication: 
  * imagedetection/bodyextractor  
  * imagedetection/faceextractor
* for cloud container and edge to cloud communication: 
  * imagedetection/aggregator  
  * imagedetection/historicaldata

## Image Capture & Processor
There are 3 containers running on edge.  
One container runs the GUI and acquire images from the webcam  
One container would be the mosquitto broker that control the topic and communication to and from client  
One container would consume the images from webcam and process and send over to the cloud

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

follow this article to install trt_pose on your jeston: [install jetson](https://spyjetson.blogspot.com/2019/12/jetsonnano-human-pose-estimation-using.html)  

Or follow these instructions:
```sh
#Install pytorch
wget https://nvidia.box.com/shared/static/wa34qwrwtk9njtyarwt5nvo6imenfy26.whl -O torch-1.7.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev 
pip3 install Cython
pip3 install numpy torch-1.7.0-cp36-cp36m-linux_aarch64.whl

#install pillow  
apt install libjpeg8-dev zlib1g-dev libtiff-dev libfreetype6 libfreetype6-dev libwebp-dev libopenjp2-7-dev libopenjp2-7-dev -y
pip3 install pillow --global-option="build_ext" \
--global-option="--enable-zlib" \
--global-option="--enable-jpeg" \
--global-option="--enable-tiff" \
--global-option="--enable-freetype" \
--global-option="--enable-webp" \
--global-option="--enable-webpmux" \
--global-option="--enable-jpeg2000"

#Install torchvision
pip3 install torchvision 

#Install torch2trt
cd /usr/local/src
sudo git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
sudo python3 setup.py install

#Install program 
pip3 install tqdm cython pycocotools
sudo apt-get install python3-matplotlib
cd /usr/local/src
sudo git clone https://github.com/NVIDIA-AI-IOT/trt_pose
cd trt_pose
sudo python3 setup.py install

#Model file is already in the body_processor folder

```

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

## Image Aggregator on the cloud

#### Step 0 -  start remote broker
```
#in ec2-container
docker pull eclipse-mosquitto (https://hub.docker.com/_/eclipse-mosquitto?tab=description)
docker run -it -p 1883:1883 eclipse-mosquitto
```
#### Step 1 -  start aggregator
```
#in ec2-container
docker build -t aggregator -f Dockerfile .
```

#### Step 2 - Start aggregator
```sh
docker run --name aggregator -ti aggregator sh
```

after get into the shell:
```sh
python3 aggregator.py
```

Note:  
for testing purpose, you can use two other terminal locally and run the following command:  
terminal 1:   
```sh
#in aggregator/src/test_input.py
python3 test_input.py
```
terminal 2:  
```sh
#in aggregator/src/test_output.py
python3 test_output.py
```
