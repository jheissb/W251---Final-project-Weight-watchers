import uuid
from datetime import datetime

class FaceImage(object):
    def __init__(self, raw_left_img, raw_right_img, left_face, right_face):
        self.raw_left_img = raw_left_img
        self.raw_right_img = raw_right_img
        self.left_face = left_face
        self.right_face = right_face
        self.image_id = uuid.uuid4()
        self.timestamp = datetime.now()
        #need to add timestamp