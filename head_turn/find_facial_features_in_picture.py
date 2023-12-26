#!/usr/bin/env python
from PIL import Image, ImageDraw
import face_recognition
import argparse

argparser = argparse.ArgumentParser(description="Find facial landmarks")
argparser.add_argument(
    "image_file",
    # nargs="?",
    # default="left.jpg",
    help="Image file to detect head turn",
)
args = argparser.parse_args()

image_file = args.image_file

# image_file = 'obama.jpg'

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

    # Let's trace out each facial feature in the image with a line!
    for facial_feature in facial_features:
        # note: left_eye here is the eye on the left side of the image when you look at it, not the person's left eye,
        # depends on whether the image is flipped(mobile front camera) or not
        if facial_feature in ['left_eye']:
            d.line(face_landmarks[facial_feature], width=5)
        

    # all_landmarks_points = [(485, 560), (491, 647), (499, 736), (517, 823), (547, 907), (595, 983), (656, 1050), (728, 1101), (815, 1112), (904, 1092), (975, 1035), (1037, 964), (1085, 887), (1111, 806), (1125, 722), (1130, 639), (1131, 560), (554, 528), (593, 480), (651, 459), (714, 460), (776, 475), (868, 475), (926, 457), (989, 455), (1048, 478), (1083, 524), (821, 531), (821, 587), (821, 643), (821, 703), (738, 734), (778, 744), (820, 754), (862, 742), (903, 730), (628, 551), (662, 533), (698, 530), (735, 550), (698, 554), (662, 556), (907, 548), (943, 528), (980, 530), (1016, 549), (980, 554), (943, 552), (656, 832), (708, 810), (773, 804), (819, 811), (863, 801), (926, 805), (981, 823), (930, 891), (868, 926), (821, 932), (772, 928), (709, 899), (671, 835), (773, 824), (819, 830), (864, 822), (964, 827), (866, 884), (820, 892), (773, 886)]        
    # d.line(all_landmarks_points, width=5, fill=(255, 0, 0))

# Display drawed image
out_file = 'out_' + image_file
print('saved to ' + out_file)
pil_image.save(out_file)
# pil_image.show()
