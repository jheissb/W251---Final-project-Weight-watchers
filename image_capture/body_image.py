import uuid
from datetime import datetime

class BodyImage(object):
    def __init__(self, raw_left_img, raw_right_img, left_bodies, right_bodies, body_keypoints):
        self.raw_left_img = raw_left_img
        self.raw_right_img = raw_right_img
        self.left_bodies = left_bodies
        self.right_bodies = right_bodies
        self.body_keypoints = body_keypoints
        self.image_id = uuid.uuid4()
        self.timestamp = datetime.now()
        #need to add timestamp