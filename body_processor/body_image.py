import uuid
from datetime import datetime
import json

class BodyImage(object):
    def __init__(self, processed_img, ratio):
        self.processed-image = processed_img
        self.waist-height-ratio = str(uuid.uuid4())
        self.hip-waist-ratio = ratio

    def serializer(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr