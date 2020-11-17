class BodyImage(object):
    def __init__(self, raw_left_img, raw_right_img, left_bodies, right_bodies):
        self.raw_left_img = raw_left_img
        self.raw_right_img = raw_right_img
        self.left_bodies = left_bodies
        self.right_bodies = right_bodies
        #need to add timestamp