## Please download test image files in the following folder and put them in an "input"  directory. Also please create an "output" directory.
#  https://github.com/abhaymise/Face-to-height-weight-BMI-estimation-/tree/master/height_weight

import face_recognition
import numpy as np
import os
import glob
import face_image
import uuid

#face_processor/src/prediction_images
def face_main(left_image, right_image):
    left_image = face_recognition.load_image_file("face_processor/src/prediction_images")
    right_image = face_recognition.load_image_file("face_processor/src/prediction_images")
    related_id = uuid.uuid4()
    left_face_locations = face_recognition.face_locations(left_image)
    left_image_encoding = face_recognition.face_encodings(left_image, left_face_locations)
    right_face_locations = face_recognition.face_locations(right_image)
    right_image_encoding = face_recognition.face_encodings(right_image, right_face_locations)
    if left_image_encoding and right_image_encoding:  ## if is a face
        ## only check the first one
        for i in range(len(left_image_encoding)):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(right_image_encoding, left_image_encoding[i])
            matched_face_indices = [i for i, x in enumerate(matches) if x]
            if len(matched_face_indices) == 1: ## new face
                matched_index = matched_face_indices[0]
                left_face = cut_face(left_face_locations[i], left_image_encoding[i])
                right_face = cut_face(right_face_locations[matched_index], right_image_encoding[matched_index])
                return face_image.FaceImage(related_id, left_image_encoding[i], right_image_encoding[matched_index], left_face, right_face)
            else:
                return None

def cut_face(location, face_encoding):
    top, right, bottom, left = location
    return face_encoding[top:bottom, left:right]

def convert_to_binary(imagetype, image):
    rc, imgbinary = cv2.imencode(imagetype, image)
    return imgbinary.tobytes()