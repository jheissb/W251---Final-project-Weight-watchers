FROM ubuntu
LABEL name="imagecapture"

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install Cython
RUN pip3 install numpy
RUN pip3 install paho-mqtt
RUN apt-get -y install python3-matplotlib
RUN apt-get -y install python3-pyqt5
RUN apt-get -y install nano
# example from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
COPY read_image.py read_image.py
COPY cam.py cam.py
COPY cam_body.py cam_body.py
ADD GUI GUI
#ADD images images 
# CMD ["python3","GUI/wwatchers2.py"]
#ENTRYPOINT ["python3", "-u", "GUI/wwatchers2.py"]
