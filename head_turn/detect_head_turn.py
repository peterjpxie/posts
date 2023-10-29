#!/usr/bin/env python
"""
Detect head turn
"""
from PIL import Image, ImageDraw, ImageFont
import face_recognition
import argparse

argparser = argparse.ArgumentParser("Find facial landmarks")
argparser.add_argument(
    "-i",
    "--image_file",
    default="obama.jpg",
    help="Image file to find facial landmarks",
)
args = argparser.parse_args()

image_file = args.image_file
# image_file = 'obama.jpg'

# Load the jpg file into a numpy array
image = face_recognition.load_image_file(image_file)

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)
num_faces = len(face_landmarks_list)
print(f"I found {num_faces} face(s) in this photograph.")
# Get locations of all the faces in the image
face_locations = face_recognition.face_locations(image)

pil_image = Image.fromarray(image)
d = ImageDraw.Draw(pil_image)

facial_features = [
    "chin",
    "left_eyebrow",
    "right_eyebrow",
    "nose_bridge",
    "nose_tip",
    "left_eye",
    "right_eye",
    "top_lip",
    "bottom_lip",
]

def point_distance(p1,p2):
    """get distance of two points"""
    return math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )

# get landmarks of first face
face_landmarks = face_landmarks_list[0]
# Let's trace out each facial feature in the image with a line!
for facial_feature in facial_features:
    print(
        f"{facial_feature} has {len(face_landmarks[facial_feature])} points: {face_landmarks[facial_feature]}"
    )
    d.line(face_landmarks[facial_feature], width=5)

# draw left chin to nose top in green
d.line(face_landmarks["chin"][-1:] + face_landmarks["nose_bridge"][:1], width=5, fill=(0, 255, 0))
# draw right chin to nose top in red
d.line(face_landmarks["chin"][:1] + face_landmarks["nose_bridge"][:1], width=5, fill=(255, 0, 0))

# 


## Add the text to the image
top, right, bottom, left = face_locations[0]
position = (left, top)
font_size = (right - left) // 6 # relative to face size
font = ImageFont.truetype("arial.ttf", size=font_size)
text_color = (0, 0, 255)  # RGB color
d.text(position, 'hello', fill=text_color, font=font)

# Save drawed image
out_file = "out_" + image_file
print("saved to " + out_file)
pil_image.save(out_file)
# pil_image.show()