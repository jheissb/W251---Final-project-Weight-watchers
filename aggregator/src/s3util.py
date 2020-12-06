#THE CURD method for s3

import paho.mqtt.client as mqtt
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import uuid
import os
import io
from PIL import Image as Image
from array import array
import json
import sys
import logging
import traceback
import base64
import cv2

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

credentials = json.load(open('aws_cred.json'))

session = boto3.Session(
         aws_access_key_id=credentials['ACCESS_KEY_ID'],
         aws_secret_access_key=credentials['SECRET_ACCESS_KEY'])
  
s3_client = session.client('s3')

S3_BUCKET_NAME='wait-watcher'
S3_USER_HISTORICAL_FOLDER_NAME='user-historical-data'
S3_FACE_ID_FOLDER_NAME='face-id'
S3_FACE_ID_KEY_FORMAT=S3_FACE_ID_FOLDER_NAME+"/{id}.png"
S3_USER_DATA_KEY_FORMAT=S3_USER_HISTORICAL_FOLDER_NAME+"/{id}/{year}-{month}-{day}.json"

def save_face_data(face_img, face_id):
    try:
        _,png = cv2.imencode('.png', face_img)
        png_as_text = base64.b64encode(png).decode()
        key = S3_FACE_ID_KEY_FORMAT.format(id=face_id)
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=png_as_text)
    except Exception as e: 
        logger.error("save_face_data")
        traceback.print_exc() 

def get_and_insurpt_user_data(update_user_object, face_id):
    try:
        now = datetime.now() # current date and time
        s3_key = S3_USER_DATA_KEY_FORMAT.format(id=face_id, year=now.year, month=now.month, day=now.day)
        logger.info("getting user object, user bmi :{}".format(update_user_object['bmi']))
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key, Body=str(json.dumps(update_user_object)), ACL='public-read')
    except Exception as e:
        logger.error("get_and_insurpt_user_data")
        traceback.print_exc()

def retrive_all_face_keys():
    try:
        # prefix = "{}/{}".format(S3_BUCKET_NAME, S3_FACE_ID_FOLDER_NAME)
        objects = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME,Prefix=S3_FACE_ID_FOLDER_NAME)

        user_historical_data = []
        for key_object in objects['Contents']:
            user_historical_data.append(key_object['Key'])
        return user_historical_data[1:]
    except Exception as e:
        logger.error("retrive_all_face_keys")
        traceback.print_exc()

#TODO: deal with truncated file
def retrive_user_hitstorical_data_by_face_id(face_id):
    try:
        prefix = "{}/{}".format(S3_USER_HISTORICAL_FOLDER_NAME, face_id)
        objects = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME,Prefix=prefix)

        user_historical_data = []
        for key_object in objects['Contents']:
            key_split = key_object['Key'].split("/")
            historical_object = {}
            historical_data = retrive_user_historical_data_by_date_and_face_id(key_object['Key'])
            historical_data = json.loads(historical_data)
            user_file_name = key_split[-1]
            historical_object['date']=user_file_name.split(".")[0]
            historical_object['bmi']=historical_data['bmi']
            historical_object['waist-height-ratio']=historical_data['waist-height-ratio']
            historical_object['waist-hip-ratio']=historical_data['waist-hip-ratio']
            user_historical_data.append(historical_object)
        return user_historical_data
    except Exception as e:
        logger.error("retrive_user_hitstorical_data_by_face_id")
        traceback.print_exc()

def retrive_user_historical_data_by_date_and_face_id(key):
    try:
        s3_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key) 
        return s3_object["Body"].read().decode()
    except Exception as e:
        logger.error("retrive_user_historical_data_by_date_and_face_id")
        traceback.print_exc()
