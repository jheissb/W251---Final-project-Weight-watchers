import uuid

class FaceImage(object):
    def __init__(self, related_id, raw_left_img, raw_right_img, left_face, right_face):
        self.raw_left_img = raw_left_img
        self.raw_right_img = raw_right_img
        self.left_face = left_face
        self.right_face = right_face
        self.image_id = uuid.uuid4()
        self.related_id = related_id
        #need to add timestamp