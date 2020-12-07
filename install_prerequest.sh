#!/bin/bash

#Install pytorch
echo "Install pytorch"
wget https://nvidia.box.com/shared/static/wa34qwrwtk9njtyarwt5nvo6imenfy26.whl -O torch-1.7.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev 
pip3 install Cython
pip3 install numpy torch-1.7.0-cp36-cp36m-linux_aarch64.whl
echo "Finished pytorch installation"

#install pillow  
echo "Install pillow"
apt install libjpeg8-dev zlib1g-dev libtiff-dev libfreetype6 libfreetype6-dev libwebp-dev libopenjp2-7-dev libopenjp2-7-dev -y
pip3 install pillow --global-option="build_ext" \
--global-option="--enable-zlib" \
--global-option="--enable-jpeg" \
--global-option="--enable-tiff" \
--global-option="--enable-freetype" \
--global-option="--enable-webp" \
--global-option="--enable-webpmux" \
--global-option="--enable-jpeg2000"
echo "Finished pillow installation"

#Install torchvision
echo "Install torchvision"
pip3 install torchvision 
echo "Finished torchvision installation"

#Install torch2trt
echo "Install torch2trt"
cd /usr/local/src
sudo git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
sudo python3 setup.py install
echo "Finished torch2trt installation"

#Install trt_pose 
echo "Install trt_pose"
pip3 install tqdm cython pycocotools
sudo apt-get install python3-matplotlib
cd /usr/local/src
sudo git clone https://github.com/NVIDIA-AI-IOT/trt_pose
cd trt_pose
sudo python3 setup.py install
echo "Finished trt_pose installation"
#Model file is already in the body_processor folder



#Install docker-compose
echo "Install docker-compose"
sudo apt-get install -y python-openssl
export DOCKER_COMPOSE_VERSION=1.27.4
sudo pip3 install docker-compose=="${DOCKER_COMPOSE_VERSION}"
echo "Finished docker-compose installation"