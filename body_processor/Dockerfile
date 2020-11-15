FROM alpine:latest
LABEL name="imageprocessor"

RUN apk update
RUN apk add py3-setuptools python3-dev py3-pip
RUN pip3 install paho-mqtt
COPY image_processor.py image_processor.py