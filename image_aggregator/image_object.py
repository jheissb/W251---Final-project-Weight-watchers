class UserImage(object):
    def __init__(self, session_id, face_image, body_image):
        self.session_id = session_id
        self.face_image = face_image
        self.body_image = body_image
        #need to add timestamp