import joblib
import face_recognition
from pathlib import Path
import numpy as np
import os


def save_model(model, model_path, model_name):
    joblib.dump(model, os.path.join(model_path, model_name))
    print(f"model saved at: {os.path.join(model_path, model_name)}")
    print("-" * 20)


def load_model(model_path, model_name):
    print("model loaded")
    print("-" * 20)
    return joblib.load(os.path.join(model_path, model_name))


def get_face_encoding(image_path):
    print(image_path)
    picture_of_me = face_recognition.load_image_file(image_path)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)
    if not my_face_encoding:
        print("no face found !!!")
        return np.zeros(128).tolist()
    return my_face_encoding[0].tolist()


def get_index_of_digit(string):
    import re
    match = re.search("\d", Path(string).stem)
    return match.start(0)

