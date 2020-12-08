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

### Install the prerequests:
Run the below command to install the prerequest:
```
#if the file is unexcutable, run the below command first
#chmod +x install_prerequest.sh 
./install_prerequest.sh
```

### Start scripts
Run the below command to start the applications on jeston. 
```
#if the file is unexcutable, run the below command first
#chmod +x start.sh 
./start.sh
```
What it would do is: 
* running command to prepared the environment for the application 
* running docker compose up to get dockerize component up 
* running trt_pose detection on jetson directly for body_processor

### Debugging issue
If you running into camera cannot open issue, make sure you mapped the correct camera to the index 0. 
```
imagecapture.devices: "/dev/video{replace_with_the_correct_index}:/dev/video0"
```

To check the logs for docker containers:
```
#in the project root directory
docker-compose logs
```

To bring down the docker containers"
```
#in the project root directory
docker-compose down 
```



