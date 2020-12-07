#!/bin/bash
xhost+
docker-compose up -d
local_broker_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' w251---final-project-weight-watchers_imageprocessorbroker_1)
export local_broker_ip=$local_broker_ip
echo $local_broker_ip
cd body_processor
python3 body_processor.py

