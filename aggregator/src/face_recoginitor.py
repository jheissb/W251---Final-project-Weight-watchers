import face_recognition
from PIL import Image
import os
import glob
import traceback
from s3util import retrive_all_face_keys, retrive_user_historical_data_by_date_and_face_id, save_face_data
import cv2
import uuid
import base64
import numpy as np


def recognit_face(new_img):
    print("start finding face")
    try:
        encoding_list = []
        existed_face__key_list = retrive_all_face_keys()
        new_img = cv2.imdecode(new_img, cv2.COLOR_BGR2RGB)
        new_face_encoding = face_recognition.face_encodings(new_img)
        for face_img_key in existed_face__key_list:
            face_img = retrive_user_historical_data_by_date_and_face_id(face_img_key)
            img_original = base64.b64decode(face_img)
            img_as_np = np.frombuffer(img_original, dtype=np.uint8)
            face_img = cv2.imdecode(img_as_np, cv2.COLOR_BGR2RGB)
            face_img_encoding = face_recognition.face_encodings(face_img)
            encoding_list.append(face_img_encoding[0])
        result_list = face_recognition.compare_faces(encoding_list, new_face_encoding[0])
        find_face = [i for i, x in enumerate(result_list) if x]
        face_id = str(uuid.uuid4())
        print("result_list ")
        print(result_list)
        print("find_face ")
        print(find_face)
        if len(find_face) == 0: ## new face
            print("new face" + face_id)
            save_face_data(new_img, face_id)
        else:
            index = find_face[0]
            face_id = existed_face__key_list[index]
            face_id = face_id.split('/')[1].split('.')[0]
            save_face_data(new_img, face_id)
            print("existed face " + face_id)
        print("face id " + face_id)
        return face_id
    except Exception as e:
        print("recognit_face")
        traceback.print_exc() 
