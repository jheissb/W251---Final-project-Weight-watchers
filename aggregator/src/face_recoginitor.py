import face_recognition
from PIL import Image
import os
import glob
from s3util import retrive_all_face_keys, retrive_user_historical_data_by_date_and_face_id, save_face_data
import cv2
import uuid


def recognit_face(new_img):
    encoding_list = []
    existed_face__key_list = retrive_all_face_keys()
    new_img = cv2.imdecode(new_img, cv2.COLOR_BGR2RGB)
    new_face_encoding = face_recognition.face_encodings(new_img)
    for face_img_key in existed_face__key_list:
        face_img = retrive_user_historical_data_by_date_and_face_id(face_img_key)
        face_img = cv2.imdecode(face_img, cv2.COLOR_BGR2RGB)
        face_img_encoding = face_recognition.face_encodings(face_img)
        encoding_list.append(face_img_encoding)
    
    result_list = face_recognition.compare_faces(encoding_list, new_face_encoding[0])
    find_face = [i for i, x in enumerate(result_list) if x]
    face_id = str(uuid.uuid4())
    if len(find_face) == 0: ## new face
        save_face_data(new_img, face_id)
    elif len(find_face) == 1:
        index = find_face[0]
        face_id = existed_face__key_list[index]
        save_face_data(new_img, face_id)
    return face_id
