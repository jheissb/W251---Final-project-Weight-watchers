import uuid
from datetime import datetime
import json
import face_serde

class FaceImage(object):
    def __init__(self, raw_img, bmi):
        self.raw_img = raw_img
        self.image_id = str(uuid.uuid4())
        self.timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        self.bmi = bmi
        #need to add timestamp

    def serializer(self):
        print("get called")
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

def deserializer(jsonStr):
    jsonObject = json.loads(jsonStr, object_hook=face_serde.faceDecoder)
    return jsonObject