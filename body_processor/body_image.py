import uuid
from datetime import datetime
import json

class BodyImage(object):
    def __init__(self, raw_img, ratio):
        self.raw_img = raw_img
        self.image_id = str(uuid.uuid4())
        self.timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        self.ratio = ratio
        #need to add timestamp

    def serializer(self):
        print("get called")
        jsonStr = json.dumps(self.__dict__)
        return jsonStr