import pose_detector
import cv2
import body_image


def body_main(left_image, right_image=None):
    if right_image:
        if validate_whole_body_exist(left_image) and validate_whole_body_exist(right_image):
            left_processed_image, left_kpoint = identify_pose(left_image)
            right_processed_image, right_kpoint = identify_pose(right_image)
            if vaidate_keypoint(left_kpoint[0]) and vaidate_keypoint(right_kpoint[0]):
                left_encoded_image = convert_to_binary(left_image)
                left_endoced_processed_image = convert_to_binary(left_processed_image)
                right_encoded_image = convert_to_binary(right_image)
                right_endoced_processed_image = convert_to_binary(right_processed_image)
                metadata = (left_kpoint[0], right_kpoint[0])
                return body_image.BodyImage(left_encoded_image, left_endoced_processed_image,right_encoded_image, right_endoced_processed_image, metadata)
            else:
                return None
    else:
        if validate_whole_body_exist(left_image):
            left_processed_image, left_kpoint = identify_pose(left_image)
            if vaidate_keypoint(left_kpoint[0]):
                left_encoded_image = convert_to_binary(left_image)
                left_endoced_processed_image = convert_to_binary(left_processed_image)
                return body_image.BodyImage(left_encoded_image, left_endoced_processed_image,None,None, metadata)
            else:
                return None



def validate_whole_body_exist(sth):
    return None

def identify_pose(image):
    return pose_detector.detect_pose(image)

def vaidate_keypoint(kpoints):
    validat_indices = [i for i, x in enumerate(kpoints) if x]
    return len(validat_indices) > 14

def convert_to_binary(image):
    _, imgbinary = cv2.imencode('png', image)
    return imgbinary.tobytes()