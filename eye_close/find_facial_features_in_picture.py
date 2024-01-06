#!/usr/bin/env python
from PIL import Image, ImageDraw
import face_recognition
import argparse
import math

argparser = argparse.ArgumentParser(description="Find facial landmarks")
argparser.add_argument(
    "image_file",
    # nargs="?",
    # default="left.jpg",
    help="Image file to detect head turn",
)
args = argparser.parse_args()

image_file = args.image_file

def get_eye_height(eye: list):
    """ eye open height
    
    eye: list of eye points (6)
    return: height

    Algorithm: average of distance of two near points up and down, points are 1, 5 and 2, 4
    """
    sum=0
    # distance of two near points up and down
    distance_1_5 = math.sqrt( (eye[1][0] - eye[5][0])**2 + (eye[1][1] - eye[5][1])**2)
    sum += distance_1_5
    distance_2_4 = math.sqrt( (eye[2][0] - eye[2][0])**2 + (eye[4][1] - eye[4][1])**2)
    sum += distance_2_4
    return sum / 2

def get_eye_width(eye: list):
    '''distance of point 0 and 3'''
    return math.sqrt( (eye[0][0] - eye[3][0])**2 + (eye[0][1] - eye[3][1])**2)

def is_eye_open(eye: list):
    """ Check if eye is open
    
    eye: list of eye points (6)
    """
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_num = len(face_landmarks_list)
    print("I found {} face(s) in this photograph.".format(face_num))

    if face_num != 1:
        return None

    # if there is only one face in the image
    face_landmarks = face_landmarks_list[0]
    # facial_features = [
    #     'top_lip',
    #     'bottom_lip'
    # ]
    top_lip = face_landmarks['top_lip']
    bottom_lip = face_landmarks['bottom_lip']
    top_lip_height = get_lip_height(top_lip)
    bottom_lip_height = get_lip_height(bottom_lip)
    mouth_height = get_mouth_height(top_lip, bottom_lip)
    # if mouth is open more than lip height, return true.
    if mouth_height > min(top_lip_height, bottom_lip_height) / 2:
        return True
    else:
        return False
    
# Load the jpg file into a numpy array
image = face_recognition.load_image_file(image_file)

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)

print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

pil_image = Image.fromarray(image)
d = ImageDraw.Draw(pil_image)

for face_landmarks in face_landmarks_list:

    # Print the location of each facial feature in this image
    facial_features = [
        'chin',
        'left_eyebrow',
        'right_eyebrow',
        'nose_bridge',
        'nose_tip',
        'left_eye',
        'right_eye',
        'top_lip',
        'bottom_lip'
    ]

    for facial_feature in facial_features:
        print("The {} in this face has the following {} points: {}".format(facial_feature, len(face_landmarks[facial_feature]), face_landmarks[facial_feature]))
    '''out example:
    The left_eye in this face has the following 6 points: [(332, 519), (355, 503), (383, 505), (410, 525), (383, 528), (354, 527)]
    The right_eye in this face has the following 6 points: [(524, 521), (548, 499), (576, 495), (599, 510), (580, 519), (551, 522)]
    '''

    # Let's trace out each facial feature in the image with a line!
    for facial_feature in facial_features:
        # note: left_eye here is the eye on the left side of the image when you look at it, not the person's left eye,
        # depends on whether the image is flipped(mobile front camera) or not
        if facial_feature in ['left_eye']:
            d.line(face_landmarks[facial_feature][:-1], width=5) # white
        if facial_feature in ['right_eye']:
            d.line(face_landmarks[facial_feature][:], width=5, fill=(0, 255, 0)) # green        
        

    # all_landmarks_points = [(485, 560), (491, 647), (499, 736), (517, 823), (547, 907), (595, 983), (656, 1050), (728, 1101), (815, 1112), (904, 1092), (975, 1035), (1037, 964), (1085, 887), (1111, 806), (1125, 722), (1130, 639), (1131, 560), (554, 528), (593, 480), (651, 459), (714, 460), (776, 475), (868, 475), (926, 457), (989, 455), (1048, 478), (1083, 524), (821, 531), (821, 587), (821, 643), (821, 703), (738, 734), (778, 744), (820, 754), (862, 742), (903, 730), (628, 551), (662, 533), (698, 530), (735, 550), (698, 554), (662, 556), (907, 548), (943, 528), (980, 530), (1016, 549), (980, 554), (943, 552), (656, 832), (708, 810), (773, 804), (819, 811), (863, 801), (926, 805), (981, 823), (930, 891), (868, 926), (821, 932), (772, 928), (709, 899), (671, 835), (773, 824), (819, 830), (864, 822), (964, 827), (866, 884), (820, 892), (773, 886)]        
    # d.line(all_landmarks_points, width=5, fill=(255, 0, 0))

# Display drawed image
out_file = 'out_' + image_file
print('saved to ' + out_file)
pil_image.save(out_file)
# pil_image.show()
