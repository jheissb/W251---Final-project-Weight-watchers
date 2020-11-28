## Please download test image files in the following folder and put them in an "input"  directory. Also please create an "output" directory.
#  https://github.com/abhaymise/Face-to-height-weight-BMI-estimation-/tree/master/height_weight



import face_recognition
from PIL import Image
import os
import glob

def face_main( input_path, output_path ):
   
    encoding_list = []
    num_files = 0
    for image_file in os.listdir( input_path ):
        new_img = face_recognition.load_image_file( os.path.join( input_path, image_file ) )
        new_face_encoding = face_recognition.face_encodings( new_img )
        if new_face_encoding:  ## if is a face
            ## only check the first one
            result_list = face_recognition.compare_faces(encoding_list, new_face_encoding[0] )
            if len([i for i, x in enumerate(result_list) if x]) == 0: ## new face
                encoding_list.append( new_face_encoding[0] )
                cut_face_and_save( output_path, new_img, num_files )
                num_files += 1

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