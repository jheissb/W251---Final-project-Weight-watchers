import face_recognition
from PIL import Image
import os
import glob

FACE_ID_FILE_PATH = ""

def face_main(new_img):
    encoding_list = []
    for image_file in os.listdir(FACE_ID_FILE_PATH):
        new_img = face_recognition.load_image_file( os.path.join(FACE_ID_FILE_PATH, image_file))
        new_face_encoding = face_recognition.face_encodings(new_img)
        if new_face_encoding:  ## if is a face
            ## only check the first onegit 
            result_list = face_recognition.compare_faces(encoding_list, new_face_encoding[0])
            find_face = [i for i, x in enumerate(result_list) if x]
            if len(find_face) == 0: ## new face
                cut_face_and_save( FACE_ID_FILE_PATH, new_img, num_files )
            elif len(find_face) == 1:
                #TODO:
                #replace the face database with the new face
                #get_face_id()
                #return face id


def cut_face_and_save( output_path, image, num_files ):
    face_locations = face_recognition.face_locations( image )
    
    for i in range( len( face_locations ) ):
        top, right, bottom, left = face_locations[i]
        faceImage = image[top:bottom, left:right]
        final = Image.fromarray( faceImage )
        file_name = os.path.join( output_path, "face%s.png" % (str(num_files) ) )
        print ("added: ", file_name)
        final.save( file_name, "PNG" )
        num_files += 1

face_main("input", "output")