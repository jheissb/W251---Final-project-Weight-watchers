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

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

credentials = json.load(open('aws_cred.json'))

# s3_client = boto3.client('s3')
s3_client = boto3.resource('s3',
         aws_access_key_id=credentials['ACCESS_KEY_ID'],
         aws_secret_access_key=credentials['SECRET_ACCESS_KEY'])

S3_BUCKET_NAME='wait-watcher'
S3_USER_HISTORICAL_FOLDER_NAME='user-historical-data'
S3_FACE_ID_FOLDER_NAME='face-id'
S3_FACE_ID_KEY_FORMAT=S3_BUCKET_NAME+"/"+ S3_FACE_ID_FOLDER_NAME+"/{id}"
S3_USER_DATA_KEY_FORMAT=S3_BUCKET_NAME+"/"+ S3_USER_HISTORICAL_FOLDER_NAME+"/{id}/{year}/{month}/{day}"

def get_and_insurpt_body(body_object, face_id):
    now = datetime.now() # current date and time
    s3_key = S3_USER_DATA_KEY_FORMAT.format(id=face_id, year=now.year, month=now.month, day=now.day)
    user_object = retrive_user_historical_data_by_date_and_face_id(s3_key)
    logger.info("getting user object, user bmi :{}".format(user_object['bmi']))
    user_object['keypoints']=body_object['keypoints']
    user_object['wait-height-ratio']=body_object['wait-height-ratio']
    user_object['body-imag']=body_object['body-imag']
    s3_client.Bucket(S3_BUCKET_NAME).put_object(Key=s3_key, Body=str(json.dumps(user_object)), ACL='public-read')

def get_and_insurpt_face(face_object, face_id):
    now = datetime.now() # current date and time
    s3_key = S3_USER_DATA_KEY_FORMAT.format(id=face_id, year=now.year, month=now.month, day=now.day)
    user_object = retrive_user_historical_data_by_date_and_face_id(s3_key)
    logger.info("getting user object, user ratio :{}".format(user_object['ratio']))
    user_object['bmi']=face_object['bmi']
    user_object['face-img']=face_object['face-img']
    s3_client.Bucket(S3_BUCKET_NAME).put_object(Key=s3_key, Body=str(json.dumps(user_object)), ACL='public-read')

def retrive_files_by_folder():
    return None

#TODO: deal with truncated file
def retrive_user_hitstorical_data_by_face_id(face_id):
    prefix = "{}/{}".format(S3_USER_HISTORICAL_FOLDER_NAME, face_id)
    objects = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME,Prefix=prefix)

    user_historical_data = []
    for key_object in objects['Contents']:
        key_split = key_object.split("/")
        historical_object = {}
        historical_data = retrive_user_historical_data_by_date_and_face_id(key_object['Key'])
        historical_object['date']="{year}-{month}-{day}".format(year=key_split[-3],month=key_split[-2],day=key_split[-1])
        historical_object['bmi']=historical_data['bmi']
        historical_object['ratio']=historical_data['ratio']
        user_historical_data.append(historical_object)
    return user_historical_data

def retrive_user_historical_data_by_date_and_face_id(key):
    s3_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key) 
    return s3_object["Body"].read().decode()

