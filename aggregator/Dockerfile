FROM ubuntu
LABEL name="aggregator"

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
RUN pip3 install Cython
RUN pip3 install numpy pandas
RUN pip3 install paho-mqtt
RUN pip3 install sklearn
RUN pip3 install scikit-learn
RUN pip3 install boto3
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS
RUN pip3 install face_recognition

ADD src .
ADD images images 
COPY aws_cred.json aws_cred.json
CMD ["aggregator.py"]
ENTRYPOINT ["python3"]