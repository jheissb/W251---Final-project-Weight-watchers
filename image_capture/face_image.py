import uuid
from datetime import datetime
import json
import face_serde
import face_constructor
import face_image as fimg

class FaceImage(object):
    def __init__(self, raw_left_img, raw_right_img, left_face, right_face):
        self.raw_left_img = raw_left_img
        self.raw_right_img = raw_right_img
        self.left_face = left_face
        self.right_face = right_face
        self.image_id = str(uuid.uuid4())
        self.timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        self.bmi = None
    
    def serializer(self):
        print("get called")
        jsonStr = json.dumps(self.__dict__, cls=face_serde.FaceEncoder)
        return jsonStr

    def deserializer(self, jsonStr):
        jsonObject = json.loads(jsonStr, object_hook=face_serde.faceDecoder)
        return jsonObject