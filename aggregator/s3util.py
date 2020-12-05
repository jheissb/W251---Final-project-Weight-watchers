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

ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY')

# s3_client = boto3.client('s3')
s3_client = boto3.resource('s3',
         aws_access_key_id=ACCESS_KEY_ID,
         aws_secret_access_key= SECRET_ACCESS_KEY)

S3_BUCKET_NAME='wait-watcher'

def get_and_insurpt_body():
    s3_client.Bucket(S3_BUCKET_NAME).put_object(Key=key, Body=img, ACL='public-read')

def get_and_insurpt_face():
    return None

def retrive_files_by_folder():
    return None

def retrive_user_hitstorical_data_by_face_id():
    return None

def retrive_user_historical_data_by_date():
    return None
